#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Playground class to govern the 
parameters of current simulation

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.3 (2020-11-07) New logic based on Kessler and Levine (1993) paper
    - 0.2 (2020-11-04) Bugfixes
    - 0.1 (2020-11-02) Initial implementation
"""
import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

from cell import Cell

class Playground:

    # cell specific global variables:
    # $c_T$
    cell_threshold_concentration = 20.
    # $\delta c$
    cell_delta_concentration = 6000.
    # $\tau$
    cell_tau = 2.
    # $t_R$
    cell_recovery_time = 20.

    # environment specific global variables:
    # a
    lattice_size = 1.
    # $\Gamma$
    gamma = 0.5
    # $\rho$
    rho = 0.2
    # mesh size
    meshsize_x = 100
    meshsize_y = 100
    # mesh-lattice size factor
    lattice_size_factor = 1    


    def __init__(self, output, cell_threshold_concentration = 20., cell_delta_concentration = 6000., cell_tau = 2.,
                 cell_recovery_time = 20., lattice_size = 1.0, gamma = 0.01, rho = 0.2, meshsize_x = 100, meshsize_y = 100):
        Playground.cell_threshold_concentration = float(cell_threshold_concentration)
        Playground.cell_delta_concentration = float(cell_delta_concentration)
        Playground.cell_tau = float(cell_tau)
        Playground.cell_recovery_time = float(cell_recovery_time)
        Playground.lattice_size = float(lattice_size)
        Playground.gamma = float(gamma)
        Playground.rho = float(rho)
        Playground.meshsize_x = int(float(meshsize_x))
        Playground.meshsize_y = int(float(meshsize_y))
        Playground.lattice_size_factor = int(1/Playground.lattice_size)

        self.output = output

        self.setupPlayground()


    @classmethod
    def fromstring(cls, from_string):
        params = from_string.split()
        return cls(*params)


    def setupPlayground(self):
        # setup cAMP layer
        self.nx = int(self.meshsize_x / self.lattice_size)
        self.ny = int(self.meshsize_y / self.lattice_size)

        self.dx2 = self.lattice_size * self.lattice_size
        self.dy2 = self.lattice_size * self.lattice_size
        
        # lowering timestep by a factor of 1/2 to have it stable
        self.dt = 0.5 * (0.5 * self.dx2 * self.dy2 / (self.lattice_size * self.lattice_size * (self.dx2 + self.dy2)))

        self.c0 = np.zeros((self.nx, self.ny))
        self.c = self.c0.copy()

        # setup cell layer
        number_of_cells = int(self.rho * self.meshsize_x * self.meshsize_y)

        self.cells = []
        coordinates_in_use = set()

        # Create central beacon
        cell = Cell(id=0, threshold_concentration=self.cell_threshold_concentration,
                        delta_concentration = self.cell_delta_concentration, tau = self.cell_tau,
                        recovery_time=self.cell_recovery_time, lattice_size_factor=self.lattice_size_factor)
        cell.position = (int(self.nx / 2), int(self.ny / 2))
        coordinates_in_use.add((int(self.nx / 2), int(self.ny / 2)))
        cell.multiplier = 10
        cell.activate()
        cell.make_active_forever()
        self.cells.append(cell)

        for i in range(1,number_of_cells):
            # generate unique coordinates for cell
            while True:
                x = np.random.randint(low=0, high=self.meshsize_x) * self.lattice_size_factor
                y = np.random.randint(low=0, high=self.meshsize_y) * self.lattice_size_factor

                if (x, y) not in coordinates_in_use:
                    coordinates_in_use.add((x, y))
                    break
            
            cell = Cell(id=i, threshold_concentration=self.cell_threshold_concentration,
                        delta_concentration = self.cell_delta_concentration, tau = self.cell_tau,
                        recovery_time = self.cell_recovery_time, lattice_size_factor=self.lattice_size_factor)
            cell.position = (x,y)
            self.cells.append(cell)

        # ### ACTIVATE N CELLS RANDOMLY BEGINS

        # number_of_cells_active = 10
        # self.sources = np.zeros((self.nx, self.ny))
        # for i in np.random.randint(low=0, high=number_of_cells, size=number_of_cells_active):
        #     self.cells[i].activate()

        # ACTIVATE N CELLS RANDOMLY ENDS

        # ### CREATE A RANDOM BEACON BEGINS

        # number_of_cells_active = 1
        # for i in np.random.randint(low=0, high=number_of_cells, size=number_of_cells_active):
        #     self.cells[i].multiplier = 10
        #     self.cells[i].activate()
        #     self.cells[i].make_active_forever()

        # CREATE A RANDOM BEACON ENDS

        # create and update sources
        self.sources = np.zeros((self.nx, self.ny))
        for cell in self.cells:
            self.sources[cell.position] = cell.source

        # create shifted indices for vectorized PDE equation
        self.rows_center = [[i] for i in range(0, self.c.shape[0])]
        self.columns_from_left = [i for i in np.append(self.c.shape[1] - 1, range(0, self.c.shape[1] - 1))]
        self.columns_from_right = [i for i in np.append(range(1, self.c.shape[1]), 0)]

        self.rows_from_above = [[i] for i in np.append(self.c.shape[0] - 1, range(0, self.c.shape[0] - 1))]
        self.columns_center = [i for i in range(0, self.c.shape[1])]        
        self.rows_from_below = [[i] for i in np.append(range(1, self.c.shape[0]), 0)]


    # def __update_sources(self):
    #     self.sources.fill(0.)

    #     for cell in self.cells:
    #         #x, y = cell.position
    #         #c = cell.source

    #         self.sources[cell.position] = cell.source

    def __timestep(self):
        self.c = self.c0 + self.dt * (self.lattice_size * self.lattice_size * ( \
            (self.c0[self.rows_center, self.columns_from_right] - 2 * self.c0 + self.c0[self.rows_center, self.columns_from_left]) / self.dx2 \
            + (self.c0[self.rows_from_above, self.columns_center] - 2 * self.c0 + self.c0[self.rows_from_below, self.columns_center]) / self.dy2) \
            - self.gamma * self.c0 + self.sources * self.dt)
        
        # concentration is strictly positive number
        np.clip(self.c, 0, None, self.c)

        self.c0 = self.c.copy()

    def startSimulation(self, max_steps, sampling=10):
        # export initial state
        self.exportState("{}_{:04d}".format(self.output, 0))

        # do one timestep to incorporate sources into the cAMP concentration
        self.__timestep()
        # export state after first step
        self.exportState("{}_{:04d}".format(self.output, 1))

        # start simulation
        s0_sampling = 0
        for s in range(1, max_steps+1):
            self.__timestep()
            s0_sampling += 1

            if s0_sampling == sampling:
                s0_sampling = 0
                self.exportState("{}_{:04d}".format(self.output, s))

            coordinates_in_use = set()
            state_1_cells = []
            for cell in self.cells:
                if cell.position in coordinates_in_use:
                    print("WARNING: cells with same coordinates, this should never happen!")

                coordinates_in_use.add(cell.position)

                cell.update(self.dt, self.c)

                if cell.state == 1 and not cell.moved:
                    state_1_cells.append(cell.id)

            for cell_id in state_1_cells:
                # move cells
                for proposed_coord in self.cells[cell_id].propose_move(self.c):
                    if not proposed_coord in coordinates_in_use:
                        coordinates_in_use.remove(self.cells[cell_id].position)
                        #self.sources[self.cells[cell_id].position] = 0.

                        self.cells[cell_id].move(proposed_coord)

                        coordinates_in_use.add(self.cells[cell_id].position)
                        #self.sources[self.cells[cell_id].position] = self.cells[cell_id].source

                        break

            self.sources.fill(0.)
            for cell in self.cells:
                self.sources[cell.position] = cell.source
                     

    def exportState(self, base_path):
        with open("{}.cells".format(base_path), "w") as cellsfh:
            for cell in self.cells:
                cellsfh.write("{}\n".format(cell))
        
        with open("{}.playground".format(base_path), "w") as pgfh:
            pgfh.write("{}\n".format(self))

        np.savetxt("{}.camp".format(base_path), self.c)

    def importCells(self, base_path):
        del self.cells[:]

        with open("{}.cells".format(base_path), "r") as cellsfh:
            for line in cellsfh:
                cell = Cell.fromstring(line)
                self.cells.append(cell)

    def importCAMP(self, base_path):
        self.c = np.loadtxt("{}.camp".format(base_path))
        self.c0 = self.c.copy()

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {}".format(self.output, self.cell_threshold_concentration, self.cell_delta_concentration, self.cell_tau,
                                             self.cell_recovery_time, self.lattice_size, self.gamma, self.rho, self.meshsize_x, self.meshsize_y)


    def __repr__(self):
        return "{}(output={} c_threshold={} delta_c={} tau={} t_recovery={} lattice={} gamma={} rho={} meshsize_x={} meshsize_y={})".format(
                                             self.__class__.__name__,
                                             repr(self.output), repr(self.cell_threshold_concentration), repr(self.cell_delta_concentration), repr(self.cell_tau),
                                             repr(self.cell_recovery_time), repr(self.lattice_size), repr(self.gamma), repr(self.rho), repr(self.meshsize_x), repr(self.meshsize_y))
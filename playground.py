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
    - 0.1 (2020-11-02)
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
        self.nx, self.ny = int(self.meshsize_x/self.lattice_size), int(self.meshsize_y/self.lattice_size)

        self.dx2, self.dy2 = self.lattice_size**2, self.lattice_size**2
        self.dt = 0.5 * self.dx2 * self.dy2 / (2 * self.lattice_size**2 * (self.dx2 + self.dy2))

        self.c0 = np.zeros((self.nx, self.ny))
        self.c = self.c0.copy()

        # setup cell layer
        number_of_cells = int(self.rho * self.meshsize_x * self.meshsize_y)

        self.cells = []
        for i in range(number_of_cells):
            x = np.random.randint(low=0, high=self.meshsize_x) * self.lattice_size_factor
            y = np.random.randint(low=0, high=self.meshsize_y) * self.lattice_size_factor

            cell = Cell(id=i, threshold_concentration=self.cell_threshold_concentration,
                        delta_concentration = self.cell_delta_concentration, tau = self.cell_tau,
                        recovery_time = self.cell_recovery_time, lattice_size_factor=self.lattice_size_factor)
            cell.position = (x,y)
            self.cells.append(cell)

        number_of_cells_active = 10
        self.sources = np.zeros((self.nx, self.ny))
        for i in np.random.randint(low=0, high=number_of_cells, size=number_of_cells_active):
            self.cells[i].activate()

            x, y = self.cells[i].position
            c = self.cells[i].source
            self.sources[x, y] = c

        # create central source 
        # as if there were the same amount of cells as there are on the mesh 
        # already in the center
        cell = Cell(id=number_of_cells, threshold_concentration=self.cell_threshold_concentration,
                        delta_concentration = self.cell_delta_concentration, tau = self.cell_tau,
                        recovery_time = self.cell_recovery_time, lattice_size_factor=self.lattice_size_factor)
        cell.position = (int(self.c.shape[0] / 2), int(self.c.shape[0] / 2))
        # make beacon stronger
        cell.multiplier = 10
        cell.activate()
        cell.make_active_forever()
        self.cells.append(cell)

        self.sources = np.zeros((self.nx, self.ny))
        for cell in self.cells:
            self.sources[cell.position] = cell.source

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
            (self.c0[self.rows_center, self.columns_from_right] - 2*self.c0 + self.c0[self.rows_center, self.columns_from_left]) / self.dx2 \
            + (self.c0[self.rows_from_above, self.columns_center] - 2 * self.c0 + self.c0[self.rows_from_below, self.columns_center]) / self.dy2) \
            - self.gamma * self.c0 + self.sources * self.dt)
            # decay: 
        
        # concentration is strictly positive number
        np.clip(self.c, 0, None, self.c)

        self.c0 = self.c.copy()

    def call_update_and_move_of_cells(self, cells, cell_sync):
        # move cells
        for cell in cells:
            cell.update(cell_sync*self.dt, self.c)
            cell.move(self.c)

    def update_sources(self, cells):
        for cell in cells:
            self.sources[cell.position] = cell.source

    def startSimulation(self, max_steps, sampling=10, cell_sync=10, parallelisation=6):
        # prepare pool of threads 
        #p = Pool(parallelisation)

        # export initial state
        self.exportState("{}_{:04d}".format(self.output, 0))

        # do one timestep to incorporate sources into the cAMP concentration
        self.__timestep()
        # export state after first step
        self.exportState("{}_{:04d}".format(self.output, 1))

        # start simulation
        s0_sampling = 0
        s0_sync = 0
        for s in range(1, max_steps+1):
            self.__timestep()
            s0_sampling += 1
            s0_sync += 1

            if s0_sampling == sampling:
                s0_sampling = 0

                self.exportState("{}_{:04d}".format(self.output, s))

            # collapse cells -- this shouldn't be
            # cell_coords = {}
            # to_delete = []
            # for id_cell, cell in enumerate(self.cells):
            #     if cell.position in cell_coords and not cell.cancer:
            #         to_delete.append(id_cell)
            #         if cell.state == 1:
            #             self.cells[cell_coords[cell.position]].activate()
                        
            #         self.cells[ cell_coords[cell.position] ].multiplier += 1
            #     else:
            #         cell_coords[cell.position] = id_cell

            # for id_cell in sorted(to_delete, reverse=True):
            #     del self.cells[id_cell]


            # update cell source
            for cell in self.cells:
                cell.update(cell_sync * self.dt, self.c)

            # move cells -- this can be parallelised
            #block_length = int(len(self.cells)/parallelisation)+1
            #to_be_moved_cells_split = [ (self.cells[i:i+block_length], cell_sync) for i in range(0,len(self.cells),block_length)]

            #results = p.starmap(self.call_update_and_move_of_cells, to_be_moved_cells_split)
            if s0_sync == cell_sync:
                s0_sync = 0
                for cell in self.cells:
                    cell.move(self.c)

            # set source map based on cells -- this can be parallelised
            self.sources.fill(0.)

            #block_length = int(len(self.cells)/parallelisation)+1
            #to_be_moved_cells_split = [ (self.cells[i:i+block_length], ) for i in range(0,len(self.cells),block_length)]

            #results = p.starmap(self.update_sources, to_be_moved_cells_split)
            
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
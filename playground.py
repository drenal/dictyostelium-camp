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
        Playground.cell_threshold_concentration = cell_threshold_concentration
        Playground.cell_delta_concentration = cell_delta_concentration
        Playground.cell_tau = cell_tau
        Playground.cell_recovery_time = cell_recovery_time
        Playground.lattice_size = lattice_size
        Playground.gamma = gamma
        Playground.rho = rho
        Playground.meshsize_x = meshsize_x
        Playground.meshsize_y = meshsize_y
        Playground.lattice_size_factor = int(1/Playground.lattice_size)

        self.output = output

        self.setupPlayground()


    def setupPlayground(self):
        # setup cAMP layer
        self.nx, self.ny = int(self.meshsize_x/self.lattice_size), int(self.meshsize_y/self.lattice_size)

        self.dx2, self.dy2 = self.lattice_size**2, self.lattice_size**2
        self.dt = self.dx2 * self.dy2 / (2 * self.lattice_size**2 * (self.dx2 + self.dy2))

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

        # number_of_cells_active = 4
        # self.sources = np.zeros((self.nx, self.ny))
        # for i in np.random.randint(low=0, high=number_of_cells, size=number_of_cells_active):
        #     self.cells[i].activate()

        #     x, y = self.cells[i].position
        #     c = self.cells[i].source
        #     self.sources[x, y] = c

        # create central source 
        # as if there were the same amount of cells as there are on the mesh 
        # already in the center
        cell = Cell(id=number_of_cells, threshold_concentration=self.cell_threshold_concentration,
                        delta_concentration = self.cell_delta_concentration, tau = self.cell_tau,
                        recovery_time = self.cell_recovery_time, lattice_size_factor=self.lattice_size_factor)
        cell.position = (int(self.c.shape[0] / 2), int(self.c.shape[0] / 2))
        cell.activate()
        cell.make_active_forever()
        self.cells.append(cell)

        self.__update_sources()

        # setup indices for left, right, center for the forward Euler equation
        # e.g. 4,0,1,2,3
        self.index_left = np.append(self.c.shape[0] - 1, range(0, self.c.shape[0] - 1))
        # # e.g. 0,1,2,3,4
        self.index_center = range(0, self.c.shape[0])
        # # e.g. 1,2,3,4,0
        self.index_right = np.append(range(1, self.c.shape[0]), 0)     
        
        # plot initial
        self.plot(0)

        self.__timestep()
        # plot first step
        self.plot(1)


    def __update_sources(self):
        self.sources = np.zeros((self.nx, self.ny))

        for cell in self.cells:
            x, y = cell.position
            c = cell.source

            self.sources[x][y] = c

    def __timestep(self):
        self.c = self.dt * (self.c0[self.index_center][self.index_center] + self.lattice_size * self.lattice_size * ( \
            np.transpose(self.c0[self.index_left][self.index_center] - 2*self.c0[self.index_center][self.index_center] + self.c0[self.index_right][self.index_center]) / self.dx2 \
            + (self.c0[self.index_center][self.index_left] - 2 * self.c0[self.index_center][self.index_center] + self.c0[self.index_center][self.index_right]) / self.dy2) - self.gamma * self.c0[self.index_center][self.index_center] + self.sources[self.index_center][self.index_center] * self.dt)
        # decay: - self.gamma * self.c0[self.index_center][self.index_center]
        np.clip(self.c, 0, None, self.c)
        self.c0 = self.c.copy()
          

    def startSimulation(self, max_steps):
        # update cAMP sources (initial )
        for s in range(1, max_steps):
            self.__timestep()

            if s % 10 == 0:
                for cell in self.cells:
                    cell.update(s*self.dt, self.c)
                    cell.move(self.c)
                    
                    self.__update_sources()
                    
                self.plot(s)

    def plot(self, step):
        fig, ax = plt.subplots(figsize=(16, 16))
        
        im = ax.imshow(self.c, interpolation='bicubic', label="cAMP")
        fig.colorbar(im)

        cell_dots_x = {"active": [], "dormant": [], "refactory": []}
        cell_dots_y = {"active": [], "dormant": [], "refactory": []}
        for cell in self.cells:
            x, y = cell.position
            if cell.state == 1:
                cell_dots_x["active"].append(x)
                cell_dots_y["active"].append(y)
            elif cell.state == 2:
                cell_dots_x["refactory"].append(x)
                cell_dots_y["refactory"].append(y)
            else:
                cell_dots_x["dormant"].append(x)
                cell_dots_y["dormant"].append(y)


        ax.scatter(x=cell_dots_x["dormant"], y=cell_dots_y["dormant"], label="Cells (dormant)", color="black")
        ax.scatter(x=cell_dots_x["refactory"], y=cell_dots_y["refactory"], label="Cells (refactory)", color="blue")
        ax.scatter(x=cell_dots_x["active"], y=cell_dots_y["active"], label="Cells (active)", color="red")
        
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Simulation at step {}".format(step))

        ax.legend()
        fig.tight_layout()
        plt.savefig("{}_{:03d}.png".format(self.output, step))
                

    def exportState(self, base_path):
        pass
        # export cell's position and state
        # export concentration map
        # export parameters

    def importState(self, base_path):
        pass
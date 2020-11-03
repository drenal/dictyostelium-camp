#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Cell class

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-02)
"""

import numpy as np

class Cell:
    # $c_T$
    threshold_concentration = 20
    # $\delta c$
    delta_concentration = 6000
    # $\tau$
    tau = 2
    # $t_R$
    recovery_time = 20
    # lattice size / cell size factor
    lattice_size_factor = 1

    def __init__(self, id, threshold_concentration = 20,
                 delta_concentration = 6000, tau = 2,
                 recovery_time = 20, lattice_size_factor=1.):
        self.threshold_concentration = threshold_concentration
        self.delta_concentration = delta_concentration
        self.tau = tau
        self.recovery_time=recovery_time
        self.lattice_size_factor = lattice_size_factor

        # unique 
        self.id = id

        # initial setup
        self.state = 0.
        self.source = 0.
        self.current_time = 0.
        self.x = 0
        self.y = 0
        self.cancer = False


    def update(self, delta_t, c):
        self.current_time += delta_t

        if self.state == 1:
            if self.current_time > self.tau and not self.cancer:
                # end being source
                self.state = 2
                self.current_time = 0.
                self.source = 0.
        elif self.state == 2:
            if self.current_time > self.recovery_time:
                self.state = 0
                self.current_time = 0.
        else:
            if c[self.x][self.y] > self.threshold_concentration:
                self.state = 1
                self.source = self.delta_concentration / self.tau


    def move(self, c):
        index_left = np.append(range(c.shape[0] - self.lattice_size_factor, c.shape[0]), range(0, c.shape[0] - self.lattice_size_factor))
        index_center = range(0, c.shape[0])
        index_right = np.append(range(self.lattice_size_factor, c.shape[0]), range(0, self.lattice_size_factor))
        slices = [index_left, index_center, index_right]

        proposal_value = c[self.x, self.y]
        proposed_move = (1,1)
    
        for idx,vdx in enumerate(slices):
            for idy,vdy in enumerate(slices):
                if (c[vdx][vdy])[self.x][self.y] > proposal_value:
                    proposed_move = (idx,idy)
        
        self.x += (proposed_move[0] - 1) * self.lattice_size_factor
        # periodic boundary
        if self.x >= c.shape[0]:
            self.x = 0
        elif self.x < 0:
            self.x = c.shape[0]-1*self.lattice_size_factor

        self.y += (proposed_move[1] - 1) * self.lattice_size_factor
        # periodic boundary
        if self.y >= c.shape[1]:
            self.y = 0
        elif self.y < 0:
            self.y = c.shape[1]-1*self.lattice_size_factor


    @property
    def position(self):
        return self.x, self.y
        
    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def activate(self):
        self.state = 1
        self.source = self.delta_concentration / self.tau

    def make_active_forever(self):
        self.cancer = True
        


        
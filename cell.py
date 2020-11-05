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
                 recovery_time=20, lattice_size_factor=1.,
                 state=0., source=0., current_time=0.,
                 x=0, y=0, cancer=False, multiplier=1):
        # shared by all Cell objects
        Cell.threshold_concentration = float(threshold_concentration)
        Cell.delta_concentration = float(delta_concentration)
        Cell.tau = float(tau)
        Cell.recovery_time = float(recovery_time)
        Cell.lattice_size_factor = int(float(lattice_size_factor))

        # unique 
        self.id = int(float(id))

        # initial setup
        self.state = int(float(state))
        self.source = float(source)
        self.current_time = float(current_time)
        self.x = int(float(x))
        self.y = int(float(y))
        self.cancer = bool(cancer)
        self.multiplier = int(float(multiplier))
        
    
    @classmethod
    def fromstring(cls, from_string):
        """Restore a Cell object from its string representation

        Args:
            from_string (string): a space separated list of Cell properties
                        in the same order as outputted by its __str__ method

        Returns:
            Cell: a Cell class with the given properties
        """
        params = from_string.split()

        return cls(*params)


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
                self.activate()


    def move(self, c):
        if not self.cancer:
            index_left = np.append(range(c.shape[0] - self.lattice_size_factor, c.shape[0]), range(0, c.shape[0] - self.lattice_size_factor))
            index_center = range(0, c.shape[0])
            index_right = np.append(range(self.lattice_size_factor, c.shape[0]), range(0, self.lattice_size_factor))
            slices = [index_left, index_center, index_right]

            proposal_value = c[self.x, self.y]
            proposed_move = (1,1)
        
            for idx,vdx in enumerate(slices):
                for idy,vdy in enumerate(slices):
                    if np.abs(((c[vdx][vdy])[self.x][self.y] - proposal_value)) > 1e-10:
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
        self.source = self.multiplier * self.delta_concentration / self.tau

    def make_active_forever(self):
        self.cancer = True
        
    def __str__(self):

        # order needs to be the same as for __init__ as this output
        # is used as input for classmethod Cell.fromstring()
        return "{} {} {} {} {} {} {} {} {} {} {} {} {}".format(self.id, self.threshold_concentration,
                                                   self.delta_concentration, self.tau,
                                                   self.recovery_time, self.lattice_size_factor,
                                                   self.state, self.source, self.current_time,
                                                   self.x, self.y, int(self.cancer), self.multiplier)


    def __repr__(self):
        return "{}(id={} c_thres={} delta_c={} tau={} t_recovery={} lattice_factor={} state={} source={} time={} x={} y={} cancer={} multiplier={})".format(
                                                   self.__class__.__name__, repr(self.id), repr(self.threshold_concentration),
                                                   repr(self.delta_concentration), repr(self.tau),
                                                   repr(self.recovery_time), repr(self.lattice_size_factor),
                                                   repr(self.state), repr(self.source), repr(self.current_time),
                                                   repr(self.x), repr(self.y), repr(self.cancer), repr(self.multiplier))


        
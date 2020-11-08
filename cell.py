#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Cell class

This class implements the logic of cAMP signaling in a 
Dictyostelium slime mould. 

It's aware of its state, position and what it is allowed or
not allowed to do.

It's unaware of its neighbour cells, that information has to be
processed externally. (It only affects movement, otherwise they
are autnomous.)

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.3 (2020-11-07) New logic based on Kessler and Levine (1993) paper
    - 0.2 (2020-11-05) Bugfixes
    - 0.1 (2020-11-02) Initial implmenetation
"""

import numpy as np

class Cell:
    """Cell class

    This class implements the logic of cAMP signaling in a 
    Dictyostelium slime mould. 

    It's aware of its state, position and what it is allowed or
    not allowed to do.

    It's unaware of its neighbour cells, that information has to be
    processed externally. (It only affects movement, otherwise they
    are autnomous.)

    Returns:
        Cell: instance of a Cell
    """
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
                 x=0, y=0, cancer=False, multiplier=1, moved=False):
        # shared by all Cell objects
        Cell.threshold_concentration = float(threshold_concentration)
        Cell.delta_concentration = float(delta_concentration)
        Cell.tau = float(tau)
        Cell.recovery_time = float(recovery_time)
        Cell.lattice_size_factor = int(float(lattice_size_factor))

        # unique 
        self.id = int(float(id))

        # initial setup of cell instance
        self.state = int(float(state))
        self.source = float(source)
        self.current_time = float(current_time)
        self.x = int(float(x))
        self.y = int(float(y))
        self.cancer = bool(int(float(cancer)))
        self.multiplier = int(float(multiplier))
        self.moved = bool(int(float(moved)))
        
    
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
        """Update cell instance's state

        Args:
            delta_t (float): elapsed time
            c (numpy 2D array of floats): cAMP concentration matrix
        """
        if self.state == 1:
            self.current_time += delta_t

            if self.current_time > self.tau and not self.cancer:
                # end being active
                self.state = 2
                self.current_time = 0.
                self.source = 0.
        elif self.state == 2:
            self.current_time += delta_t
            
            if self.current_time > self.recovery_time:
                self.state = 0
                self.current_time = 0.
        else:
            if c[self.x, self.y] > self.threshold_concentration:
                self.activate()

    def move(self, position):
        """Move cell if cell hasn't been moved yet

        Args:
            position (tuple of ints): proposed x,y-coordinates
        """
        # cells can only move in 
        # - state 1 and
        # - if they are not set to be always active and
        # - if they haven't been moved yet
        if position != self.position:
            if not self.moved and self.state == 1 and not self.cancer:
                self.position = position
                self.moved = True

    def propose_move(self, c):
        """Propose move based on cAMP concentration around this cell instance

        Args:
            c (numpy 2D array of floats): cAMP concentration matrix

        Returns:
            tuple of ints: the porposed x,y-coordinates
        """
        # set x and y ranges for looking around
        coord_range = []
        # x: coord=0, y: coord=1
        for coord in [0,1]:
            coord_range.append([self.position[coord] - self.lattice_size_factor,
                            self.position[coord],
                            self.position[coord] + self.lattice_size_factor])

            # periodic boundary:
            if coord_range[-1][0] < 0:
                coord_range[-1][0] = c.shape[coord] - self.lattice_size_factor

            if coord_range[-1][2] >= c.shape[coord]:
                coord_range[-1][2] = 0
            
        # set initial proposal value (value at current position)
        # proposal_value = c[self.position]
        # proposed_move = []
        proposal_values = {(vdx, vdy): c[vdx][vdy] for vdx in coord_range[0] for vdy in coord_range[1]}
        proposed_moves = [k for k, v in sorted(proposal_values.items(), key=lambda item: item[1], reverse=True) if (v - c[self.position]) > 5e-4]

    
        # visit neighbouring coordinates
        # for vdx in coord_range[0]:                    
        #     for vdy in coord_range[1]:
        #         if np.abs((c[vdx][vdy] - proposal_value)) > 5e-1:
        #             proposal_value = c[vdx][vdy]
        #             proposed_move = (vdx,vdy)
            
        return proposed_moves

    @property
    def position(self):
        """Returns with coordinates of cell instance

        Returns:
            tuple of ints: x,y-coordinates
        """
        return self.x, self.y
        
    @position.setter
    def position(self, pos):
        """Sets the position from a tuple

        Args:
            pos (tuple of ints): x,y-coordinates
        """
        self.x = pos[0]
        self.y = pos[1]

    def activate(self):
        """Puts cell instance in active state

        state is 1, amount of cAMP to release is set, elapsed time and move counter are set to zero.
        """
        self.state = 1
        self.source = self.multiplier * self.delta_concentration / self.tau
        self.current_time = 0.
        self.moved = False
    

    def make_active_forever(self):
        """Makes cell instance locked in state 1 and unable to move
        """
        self.cancer = True
        
    def __str__(self):
        # order needs to be the same as for __init__ as this output
        # is used as input for classmethod Cell.fromstring()
        return "{} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(self.id, self.threshold_concentration,
                                                   self.delta_concentration, self.tau,
                                                   self.recovery_time, self.lattice_size_factor,
                                                   self.state, self.source, self.current_time,
                                                   self.x, self.y, int(self.cancer), self.multiplier, int(self.moved))


    def __repr__(self):
        return "{}(id={} c_thres={} delta_c={} tau={} t_recovery={} lattice_factor={} state={} source={} time={} x={} y={} cancer={} multiplier={} moved={})".format(
                                                   self.__class__.__name__, repr(self.id), repr(self.threshold_concentration),
                                                   repr(self.delta_concentration), repr(self.tau),
                                                   repr(self.recovery_time), repr(self.lattice_size_factor),
                                                   repr(self.state), repr(self.source), repr(self.current_time),
                                                   repr(self.x), repr(self.y), repr(self.cancer), repr(self.multiplier), repr(self.moved))


        
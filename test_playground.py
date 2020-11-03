#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Unittest for playground

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-02)
"""
import playground
import unittest

class SingletonTest(unittest.TestCase):
    def setUp(self):
        self.playground = playground.Playground("test_playground", cell_threshold_concentration = 20., cell_delta_concentration = 6000., cell_tau = 2.,
                 cell_recovery_time = 20., lattice_size = 1.0, gamma = 0.01, rho = 0.2, meshsize_x = 100, meshsize_y = 100)

    def test_equality(self):
        self.assertEqual(self.playground.cell_threshold_concentration, 20.)
        self.assertEqual(self.playground.cell_delta_concentration, 6000.)
        self.assertEqual(self.playground.cell_tau, 2.)
        self.assertEqual(self.playground.cell_recovery_time, 20.)
        self.assertEqual(self.playground.lattice_size, 1.0)
        self.assertEqual(self.playground.gamma, 0.01)
        self.assertEqual(self.playground.rho, 0.2)
        self.assertEqual(self.playground.meshsize_x, 100)
        self.assertEqual(self.playground.meshsize_y, 100)

if __name__ == '__main__':
    unittest.main()


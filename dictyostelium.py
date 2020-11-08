#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Dictyostelium simulation

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-02)
"""

import argparse

from playground import Playground


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', '--lattice', help="Lattice size", default=1, type=float)
    parser.add_argument('-g', '--gamma', help="Gamma: decay constant", default=0.5, type=float)
    parser.add_argument('-r', '--rho', help="Rho: density of cells", default=0.2, type=float)
    parser.add_argument('-c', '--threshold', help="Threshold concentration", default=20., type=float)
    parser.add_argument('-d', '--camp', help="Amount of cAMP released by excited cell over period of tau", default=6000, type=float)
    parser.add_argument('-t', '--tau', help="Timespan of a cell being in excited state", default=2, type=float)
    parser.add_argument('-R', '--recovery', help="Timespan of a cell being resistant to excitation", default=20, type=float)
    parser.add_argument('-m', '--mesh', help="1D size of the 2D mesh to simulate on (it's always a square mesh)", default=10, type=float)
    parser.add_argument('-s', '--steps', help="Steps to run PDE for", default=100, type=int, required=True)
    parser.add_argument('-i', '--import', help="Import state from base path's files", dest="importstate")
    parser.add_argument('-o', '--output', help="Output plots' base", required=True)
    parser.add_argument('-S', '--sampling', help="Number of steps to sample after", default=10, type=int)
    args = parser.parse_args()

    if args.importstate:
        pg = Playground.fromstring(open("{}.playground".format(args.importstate), "r").readline())
        pg.output = args.output
        pg.importCells(args.importstate)
        pg.importCAMP(args.importstate)
    else:
        pg = Playground(args.output, args.threshold, args.camp, args.tau, args.recovery, args.lattice,
                        args.gamma, args.rho, args.mesh, args.mesh)

    pg.startSimulation(max_steps = args.steps, sampling = args.sampling)

    
if __name__ == "__main__":
    main()



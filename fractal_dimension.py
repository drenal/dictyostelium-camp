#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
This script calculates the fractal dimension
from the outputted state files of a simulation

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-08)
"""
import argparse

import numpy as np
import matplotlib.pyplot as plt

from cell import Cell
from playground import Playground

def plot(cells, meshsize_x, meshsize_y,  output):

    cell_coords = []
    for cell in cells:
        cell_coords.append(cell.position)
    cell_coords = np.array(cell_coords)

    scales=np.logspace(0.01, 1, num=10, endpoint=False, base=2)
    Ns = []
    
    for scale in scales:
        H, edges=np.histogramdd(cell_coords, bins=(np.arange(0,meshsize_x,scale),np.arange(0,meshsize_y,scale)))
        Ns.append(np.sum(H>0))

    coeffs = np.polyfit(np.log(scales), np.log(Ns), 1)

    np.savetxt("{}.scaling".format(output), list(zip(scales,Ns)))
    
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.scatter(x=np.log(scales), y=np.log(Ns), label="Number of boxes")
    ax.plot(np.log(scales), np.polyval(coeffs, np.log(scales)), "o-", label="$y={:.04f} \cdot x + {:.04f}$".format(coeffs[0], coeffs[1]))
    ax.set_xlabel("log(box size)", fontsize=20)
    ax.set_ylabel("log(number of boxes)", fontsize=20)
    ax.set_title("Fractal dimension of {}".format(output.split("_fractal_dim")[0]), fontsize=20)
    ax.legend(loc=1)
    fig.tight_layout()
    plt.savefig("{}.png".format(output))

    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', help="Input state files base")
    args = parser.parse_args()

    pg = Playground.fromstring(open("{}.playground".format(args.input), "r").readline())
    pg.importCells(args.input)
    
    plot(pg.cells, pg.meshsize_x, pg.meshsize_y, args.input+"_fractal_dim")


if __name__ == "__main__":
    main()
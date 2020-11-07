#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Script to analyse create plots out of the checkpoints of the simulation

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-04)
"""

import glob
import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from cell import Cell

def plot(step, c, cells, output):
    fig, ax = plt.subplots(figsize=(16, 16))
    
    c_threshold = cells[0].threshold_concentration
    # define the colors
    #cmap = mpl.colors.ListedColormap(['w', 'g'])

    # create a normalize object the describes the limits of
    # each color
    #if np.max(c) < c_threshold:
    #    bounds = [0., 1.0, 1.0]
    #else:
    #    bounds = [0., c_threshold / np.max(c), 1.0]
    #norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    #im = ax.imshow(c.T, interpolation='none', label="cAMP", cmap=cmap, norm=norm)
    im = ax.imshow(c.T, interpolation='none')
    cb = fig.colorbar(im)
    cb.set_label("cAMP", fontsize=16)    

    cell_dots_x = {"active": [], "dormant": [], "refactory": []}
    cell_dots_y = {"active": [], "dormant": [], "refactory": []}
    for cell in cells:
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
    
    ax.set_xlabel("x", fontsize=16)
    ax.set_ylabel("y", fontsize=16)
    ax.set_title("Simulation at step {}".format(step), fontsize=16)

    ax.legend(loc=1)
    fig.tight_layout()
    plt.savefig("{}_{:04d}.png".format(output, step))

    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input', help="Input state files base")
    parser.add_argument('-o', '--output', help="Output plots base path")
    args = parser.parse_args()

    
    # prefix_[step].[cells|camp|playground]
    cells_files = glob.glob("{}_*.cells".format(args.input))
    cells_files = sorted(cells_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    camp_files = glob.glob("{}_*.camp".format(args.input))
    camp_files = sorted(camp_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    for i, _ in enumerate(cells_files):
        cells = []
        with open(cells_files[i]) as cellsfh:
            for line in cellsfh:
                cell = Cell.fromstring(line)
                cells.append(cell)

        camp = np.loadtxt(camp_files[i])

        step = int(cells_files[i].split('_')[-1].split('.')[0])

        plot(step, camp, cells, args.output)


if __name__ == "__main__":
    main()
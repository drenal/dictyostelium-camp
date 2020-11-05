#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set encoding=utf-8 :
# vim: set fileencoding=utf-8 :
"""
Let's clear the array indexing of numpy...

Authors:
    - Lenard Szantho <lenard@drenal.eu>

Version:
    - 0.1 (2020-11-04)
"""

import numpy as np

a = np.array([
    ["00", "01", "02"],
    ["10", "11", "12"],
    ["20", "21", "22"],
])

print("The initial array: a")
print(a)

print("Selecting specific fields: a[[0, 2], [1, 2]]")
print(a[[0, 2], [1, 2]])

print("Selecting submatrix: a[[[0], [2]], [1, 2]]")
print(a[[[0], [2]], [1, 2]])

print("What if column? a[[[0], [2]], [[1], [2]]]")
print(a[[[0], [2]], [[1], [2]]])

print("What if column? a[[0, 2], [[1], [2]]]")
print(a[[0, 2], [[1], [2]]])

print("Center value from left")
rows_normal = [[0],[1],[2]]
columns_left = [2, 0, 1]
print("Row indices: {}".format(rows_normal))
print("Col indices: {}".format(columns_left))
print(a[[rows_normal], columns_left])

print("Center value from right")
rows_normal = [[0],[1],[2]]
columns_right = [1, 2, 0]
print("Row indices: {}".format(rows_normal))
print("Col indices: {}".format(columns_right))
print(a[[rows_normal], columns_right])

print("Center value from above")
rows_above = [[2],[0],[1]]
columns_normal = [0, 1, 2]
print("Row indices: {}".format(rows_above))
print("Col indices: {}".format(columns_normal))
print(a[[rows_above], columns_normal])

print("Center value from below")
rows_below = [[1],[2],[0]]
columns_normal = [0, 1, 2]
print("Row indices: {}".format(rows_below))
print("Col indices: {}".format(columns_normal))
print(a[[rows_below], columns_normal])

# ------------------------------------
print("Again, but now with np.append")
# ------------------------------------

print("Center value from left")
rows_normal = [[i] for i in range(0,a.shape[0])]
columns_left = [i for i in np.append(a.shape[1] - 1, range(0, a.shape[1]-1))]
print("Row indices: {}".format(rows_normal))
print("Col indices: {}".format(columns_left))
print(a[[rows_normal], columns_left])

print("Center value from right")
rows_normal = [[i] for i in range(0,a.shape[0])]
columns_right = [i for i in np.append(range(1, a.shape[1]), 0)]
print("Row indices: {}".format(rows_normal))
print("Col indices: {}".format(columns_right))
print(a[[rows_normal], columns_right])

print("Center value from above")
rows_above = [[i] for i in np.append(a.shape[0]-1, range(0,a.shape[0]-1))]
columns_normal = [i for i in range(0,a.shape[1])]
print("Row indices: {}".format(rows_above))
print("Col indices: {}".format(columns_normal))
print(a[[rows_above], columns_normal])

print("Center value from below")
rows_below = [[i] for i in np.append(range(1,a.shape[0]), 0)]
columns_normal = [i for i in range(0,a.shape[1])]
print("Row indices: {}".format(rows_below))
print("Col indices: {}".format(columns_normal))
print(a[[rows_below], columns_normal])
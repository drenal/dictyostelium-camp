# Simulations

## Simulation0 

Let's have export at each timestep to debug the system.

![simulation](movie_simulation_color.gif)

## Simulation1

Because of multiple bugs the cells always move in the direction of the last neighbour coordinate (bottom right) checked. Also the threshold for difference was below then numerical noise, so cells with 0 concentration neighbours also moved. Thus the source got separated from the rest of the system.

![simulation](movie_simulation.gif)

## Simulation with increased threshold for difference

Now the concentration difference has to be larger than 0.1 so that the cell moves.

![simulation](movie_simulation_difference_0_1.gif)

## Simulation2 

Still bug in movement, but a periodic, spherical wave of excitation is observable from the center.

![simulation](movie_simulation2.gif)

## Simulation3

If movement is fixed, still the area is cleared out, and cells move bottom right.

![simulation](movie_simulation3.gif)

## Simulation4 

Still area gets cleared, cells merge.

![simulation](movie_simulation4.gif)

## Simulation5, 6, 7, 8

Bugs fixed, experimenting with delaying the move step of the cell, so that it only moves after 4 timesteps.

![simulation](movie_simulation5.gif)

![simulation](movie_simulation6.gif)

![simulation](movie_simulation7.gif)

![simulation](movie_simulation8.gif)

## Simulation9 

Better, but no stationary pattern reached, still a bottom right preference of directionality.

![simulation](movie_simulation9.gif)

## Simulation10 

Some trials, still not good.

![simulation](movie_simulation10.gif)

## Simulation11, 12

Other parameters, not good.

![simulation](movie_simulation11.gif)

![simulation](movie_simulation12.gif)

## Simulation13, 14

More sources? The tree-branch-like pattern doesn't emerge

![simulation](movie_simulation13.gif)

![simulation](movie_simulation14.gif)


## Solution

So, if one reads the article, it turns out that:
- cells only move ones per activation
- cells are not allowed to overlap

So my assumptions were wrong until now.



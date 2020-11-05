# Test run with moving cells every 10th step

This outputs are from a run with the following parameters:

- lattice=1
- gamma=0.5
- rho=0.5
- threshold=20.
- camp=6000
- tau=2
- recovery=20
- mesh=100
- steps=1001
- output=test

## TODO

- make gif movie
```
convert -delay 20 -loop 0 *.png movie.gif
convert movie.gif -coalesce -scale 800x800 -fuzz 2% +dither  movie2.gif
```
- text should be larger on the plots
    - SOLVED: fontsize=16, legend fixed to top right
- make cell movement faster 
    - SOLVED: option for multithreading and better cell loopthrough
- runtime: 19:03 - 23:40 
    - SOLVED: do plotting after the simulation is done, 70% of time was spent in plotting
- there is also some memory leakage from 187MB it went up 3400MB durign the 4 hours 
    - SOLVED: matplotlib can start eat up memory if `plt.close(fig)` is not called
- maybe cells on same coordinates could be merged?
    - SOLVED: now they merge and get deleted. Each cell has a multiplier property as if there would be more cells on the same coordinate.
- or at least cells being in the central position? Then calculation would speed up
    - SOLVED by above.
- around the end all cells are always active. no refactory period?
    - SOLVED: the total step size was given to the update function, not the difference of steps from last update
- weird chess-board-like pattern in the concentration of cAMP
    - SOLVED: indexing was plain wrong, it's a miracle that it produced "some" output... see [numpy_2d_array_indexing.py](../numpy_2d_array_indexing.py) for explonation on how one should shift rows and columns in 2D numpy arrays


![movie](movie2.gif)

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

TODO:

- make gif movie
```
onvert -delay 20 -loop 0 *.png movie.gif
```
- text should be larger on the plots
- make cell movement faster
- runtime: 19:03 - 23:40
- there is also some memory leakage from 187MB it went up 3400MB durign the 4 hours
- maybe cells on same coordinates could be merged?
- or at least cells being in the central position? Then calculation would spped up
- around the end all cells are always active. no refactory period???


![movie](movie.gif)

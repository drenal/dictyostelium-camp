# First parameter search conclusions

The goal is that the signal traverses the population with an optimal speed:
- if it's too fast, the signal transduction will be broken
- if it's too slow, the decay of cAMP will break the transduction

Around the optimum it's still a problem, that the tree-like structure is not always reached, so there one should finetune.

## Narrowing the parameters

Increasing the concentration thereshold without increasing the amount of cAMP produced if excited is not going to work.
- let's do a new search with decreasing thresholds: 5 10 20
- let's also increase the amount of released cAMP: 6000 8000 10000

I've expected that decreasing the lattice size, i.e. make the simulation mroe realistic by incroporitng the evident size difference of a chemical moelcule (1-10 A) and a cell (1-100 um), but it looks like that it's not helping the simulation.
- let's keep the assumption of same sized cAMP molecule and cell (lattice size = 1)

The density of cells is also important, the paper writes 5-20% should be enough, but I see that sometimes 50% density is required, which may be unrealistic, so:
- let's keep the 20% density and try to change other parameters so that the signal transduction is optimal.

Having longer excitation doesn't seem to influence the simulation.

Having longer refactory periods may allow that a spiral like pattern emerges.

## Next step

Let's do a parameter search with:
- lattice 1
- density 0.2
- threshold 20
- cAMP release of 6000
- tau 2
- refactory period 20
- and test the decay constant from: 0.1 0.15 0.2 0.25 0.3 0.35 0.4 ( we know that for gamma 0.5 we need density 0.5 so that it works)




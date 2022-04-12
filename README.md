Z3-Minesweeper-Solver
=====================

A solver for the game Minesweeper using the Z3 Sat/Smt solver.

The solver will play optimally/perfectly as long as there are, logically speaking, safe moves possible. 

How it works
------------

The first move will always be in the top left corner.

The solver will consider all 'neighbours' of already uncovered squares and consider them as variables in an equation - 1 being a mine, 0 being a 'free' square. Using the numbers on the uncovered squares we can build an equation describing every square.

For example: When an uncovered square with the value `2` has the neighbours a, b and c, the equation becomes `a + b + c = 2`.  This is repeated for every uncovered square and passed to z3, which will spit out all positions it deems impossible to have a mine.

In situations where there are no safe moves to be made, the solver will consider up to 1000 possible mine arrangements based on the given game state and decide on the square with the smallest probability of it having a mine.

Limitations
-----------
As stated before, there are situations where the solver has to 'guess', therefore making it possible to uncover a mine and subsequently lose the game.

Additionally, the solver only considers squares directly neighbouring already uncovered squares, therefore if some squares are completely surrounded by mines, the solver will never try to uncover them as it has no information about them whatsoever. Luckily this situation happens very rarely, if at all.

Future expansion
----------------
In situations where the solver has to 'guess' a square to uncover, it may also be useful to consider the amount of information gained by uncovering that square.

The amount of total mines may also be useful to the solver, but is not used right now.

The first move has been chosen by me based on my own playstyle, it may be worthwhile to investigate whether other locations yield better win rates.

Motivation
----------
This has been written in a day with the goal to learn the z3 SAT/SMT solver, it may be possible to do this in a more straightforward way. Feel free to submit a pull request if you find any bugs or improvements! 
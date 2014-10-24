Sudoku Solver
======

Coding Challenge

## Solution algorithm

Here is how the search for sudoku solution is carried out currently:

* Find the first empty cell and determine feasible values
	* Feasible values of a cell is the range of 1 - 9, excluding any value that has appeared in the current row, current column, or current block
	* This is the current implementation. It could be smarter (working on this now).
* Fill the cell with one of the feasible values and carry out the search recursively.
	* If the number of feasible values is 0 for some cell, this would be a dead end. Search in the current iteration will finish without returning anything.
	* If all the cells are filled successfully, a solution is found. By convention, published sudoku should have one unique solution.

Right now, of the 21 sudoku puzzles (one given by the challenge, 20 found online: 9 at easy level, 8 at medium level, 3 at hard level), 20 can be solved quickly. The only exception is sudoku_medium16, which is taking a lot of time.

## How to run

* To solve a sudoku in the command line:
	* Go to the root of the repo
	* Type `python src/sudoku.py -f <your_sudoku_input_filename>`
	* Or type `python src/sudoku.py -h` to get help
* To run the tests:
	* Type `py.test tests`

## Notes for myself

* The first and brutal force solution would be to iterate through 1 - 9 for all unfilled cells. But some simple calculation shows this is almost infeasible. Validate a sudoku (as I timed it) takes about 11.7 us. If a sudoku has 26 unfilled cells, this would take 9^26 * 11.7 us = 2.4e12 years. OK, think of something else.

* Apparently, for an unfilled cell, not all number 1 - 9 is feasible. Eliminating some possibilities should expedite the search. So I write a function to produce feasible values of a given cell, by excluding numbers appeared in the same row, same column and same block. The search algorithm would simply find unfilled cells, and fill it if only one value is feasible. The solution algorithm is pretty simple, but out of the ten examples that I give it to solve at the time, only six is solved. The other four needs to go through some kind of trial and error. OK, think of something more intelligent.

* How to implement the search algorithm is a little bit complicated. I thought about building a tree structure, with each layer being an unfilled cell, and nodes in that layer being the feasible values of the unfilled cell. Recursion comes to mind due to the repetitive nature of the search. 

* Right now, of the 21 sudoku puzzles (one given by the challenge, 20 found online: 9 at easy level, 8 at medium level, 3 at hard level), 20 can be solved quickly. The only exception is sudoku_medium16, which is taking a lot of time.

* The next step is to improve the algorithm to determine feasible values. One thought from my own experience is that I would focus on one number, and see within one block (or one row, one column) where that number cannot be placed. Sometimes, this yields unique solution for a cell.
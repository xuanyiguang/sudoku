Sudoku Solver
======

## Assumptions

* It is not a good user experience if the sudoku solver takes too long (more than 2-3 seconds) to solve.
* As long as any given sudoku can be solved quickly (say within 1 second), it is more important to keep the logic simple and the code short for easier maintenance.

## Solution algorithm

Here is how the search for sudoku solution is carried out currently:

1. A greedy search is carried out first.
	* Greedy search means to check feasible values of each unfilled cell, and fill the cell if there is only one feasible value.
	* Feasible values of a cell is determined in the following manner:
		1. Any number that appears on the same row, same column, or same block of the given cell is infeasible and excluded.
        2. Among the remaining feasible values of the cell, if a number is infeasible for any other empty cell in the same block, same row, or same column, that number is uniquely the cell value and other feasible values for the cell become infeasible and are excluded.
2. If the solution is still incomplete after the greedy search, carry out a combinatorial search.
	* Fill the cell with one of the feasible values (criteria defined as above) and carry out the search on the resulting sudoku recursively.
	* If the number of feasible values is 0 for some cell, this would be a dead end (i.e., some value filled earlier in the recursion is wrong). Search in the current iteration will finish without returning anything.
	* If all the cells are filled successfully, a solution is found. By convention, published sudoku should have one unique solution.

I start from the simplest sudoku solution and gradually add more intelligence (more code) to the search algorithm. See my memo below for more details. The current solution method can solve most of the sudoku puzzles within 1 second, so I stopped there. I think the current version of the sudoku solver has a good trade-off between user experience (computing time) and code complexity.

## How to run

* On the command line, go to the root of the repo, and type `cd sudoku_solver` to step into the sudoku_solver folder.
* To solve a sudoku:
	* Type `python sudoku.py -i <your_sudoku_input_filename>`. The solution will be written to a file with default name `solution.csv` in the current folder.
	* Type `python sudoku.py -i <your_sudoku_input_filename> -o <your_sudoku_output_filename>`. The solution will be written to a file with the given filename.
	* If you want to use only the greedy search or only the combinatorial (recursive) search, you can use the mutually exclusive options `python sudoku.py -i <your_sudoku_input_filename> -o <your_sudoku_output_filename> -g` or `python sudoku.py -i <your_sudoku_input_filename> -o <your_sudoku_output_filename> -c`.
	* Or type `python sudoku.py -h` to get help.
* To run the tests:
	* Type `py.test` or `py.test tests/`.
	* Here is more information on [pytest](http://pytest.org/latest/index.html).
	* All test cases should pass in the latest commit.

## Memo for my thought process

* The first and brutal force solution would be to iterate through 1 - 9 for all unfilled cells. But some simple calculation shows this is almost infeasible. Checking the validity of a sudoku solution (as I timed it) takes about 11.7 us. If a sudoku has 26 unfilled cells, this would take 9^26 * 11.7 us = 2.4e12 years. OK, we need something else.

* Apparently, for an unfilled cell, not all number 1 - 9 is feasible. Eliminating some possibilities should expedite the search. So I write a function to produce feasible values of a given cell, by excluding numbers appeared in the same row, same column and same block. I implement a greedy search algorithm that would simply find unfilled cells, and fill it if only one value is feasible. The greedy search algorithm is pretty simple, but out of the ten examples that I give it to solve at the time, only six is solved. The other four needs to go through some kind of trial and error. OK, we need something more intelligent.

* Trial and error means some kind of combinatorial search. How to implement the combinatorial search algorithm is a little bit complicated. I thought about building a tree structure, with each layer being an unfilled cell, and nodes in that layer being the feasible values of the unfilled cell. Then recursion comes to mind due to the repetitive nature of the search. The recursive function makes the code much simpler. The combinatorial search is able to solve 20 out of the 21 sudoku puzzles that I give it to solve. The exception is sudoku medium16, which is taking a lot of time.

* Taking a further look at sudoku medium16. There are too many possible combinations, which is why the search is taking too much time. It seems intuitive to me that more intelligence is needed on the algorithm for feasible value, which would reduce the search space of the combinatorial search. When I try to solve sudoku medium16 by myself, I quickly realize that I am using some different rules to identify feasible values of a cell. I would focus on one number, and see within one block (or one row, one column) where that number cannot be placed. Sometimes, this yields unique solution for a cell. I add this intelligence to the algorithm to identify feasible values, and the search becomes faster.

* Given that I have developed two search algorithms: the greedy search and combinatorial search, it makes sense to combine them. The reason is that the greedy search, by filling empty cells with only one feasible value, reduces the size of the feasible values of other cells, which should expedite the combinatorial search. This is the current version of search algorithm described above.

Table for solution speed comparison.

* It is possible to add further intelligence to the search algorithm and expedite the search. But given the current speed, no further intelligence is added to keep the logic simple and the code short. 

* I will use the following example to demonstrate the possibility of such intelligence. In the example given in the challenge (and as below), let us focus on where 5 can be place. In the middle right block, the cell on row 3, column 6 (zero indexed) cannot be 5 because of the 5 on row 8, column 6. So, one of the cells on row 3, 4, or 5, and column 8 has to be 5. But no matter which cell has 5, the cell on row 2, column 8 in the upper right block cannot be 5. Considering that the cell on row 2, column 6 cannot be 5 due to the 5 on row 8, column 6, the cell on row 1, column 7 then has to be 5. The intelligence is that we can exclude value 5 from the cell on row 2, column 8, and uniquely determine the cell on row 1, column 7 to be 5, even if it is not clear yet where 5 is located in column 8. 

0,3,5,2,9,0,8,6,4  
0,8,2,4,1,0,7,0,3  
7,6,4,3,8,0,0,9,0  
2,1,8,7,3,9,0,4,0  
0,0,0,8,0,4,2,3,0  
0,4,3,0,5,2,9,7,0  
4,0,6,5,7,1,0,0,9  
3,5,9,0,2,8,4,1,7  
8,0,0,9,0,0,5,2,6  

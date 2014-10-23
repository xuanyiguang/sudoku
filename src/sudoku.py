import numpy as np
import argparse

def get_indices_from_same_block(index):
    """ Get indices that fall in the same block as the given index
    
    The sudoku values are zero indexed, so [0,1,2] form a block, 
    [3,4,5] form a block, and [6,7,8] form a block. For example, 
    given index 5, return ndarray array([3,4,5]).
    
    Note:
    This function works for both rows and columns
    
    """
    if index in np.array([0,1,2]):
        return np.array([0,1,2])
    elif index in np.array([3,4,5]):
        return np.array([3,4,5])
    elif index in np.array([6,7,8]):
        return np.array([6,7,8])
        
def validate_sudoku(sudoku_values):
    """ Validate a given sudoku solution
    
    Argument:
        sudoku_values (9x9 ndarray, required) -- sudoku solution
        
    Return:
        True if the solution is valid:
            - place only numbers 1 to 9 in the empty cells
            - each row, each column and each 3x3 block contains 
            the same number only once
        False otherwise
    """
    # # should only have numbers 1 to 9
    if np.min(sudoku_values) <= 0 or np.max(sudoku_values) >= 10:
        return False
        
    # # test row uniqueness
    for row in range(9):
        if len(np.unique(sudoku_values[row,:])) != 9:
            return False
            
    # # test column uniqueness
    for column in range(9):
        if len(np.unique(sudoku_values[:,column])) != 9:
            return False
            
    # # test block uniqueness
    for first_row in range(0,9,3):
        for first_column in range(0,9,3):
            row_range = get_indices_from_same_block(first_row)
            column_range = get_indices_from_same_block(first_column)
            if len(np.unique(sudoku_values[row_range][:,column_range])) != 9:
                return False
    
    # # otherwise
    return True
    
def find_feasible_values(sudoku_values,row,column):
    """ Return feasible values at the given row and column of a sudoku
    
    Argument:
        sudoku_values (9x9 ndarray, required) -- given sudoku, can be partially or fully filled
        row (int, required) -- row number
        column (int, required) -- column number
    
    Returns:
        ndarray that contains the feasible values at the given row and column 
        of the sudoku
    
    Note: 
    - Feasibility only depends on row, column and block uniqueness. 
    - No fancier rules.
    - Only values outside of the given cell will be used to calculate feasible values. Or, the value of the given cell will not be used.
    """
    # # set current cell value to 0 (not to use it)
    # # this could otherwise cause problems with filled sudoku
    sudoku_values[row,column] = 0
    
    # # collect values in the given row
    row_values = sudoku_values[row,:]
    
    # # collect values in the given column
    column_values = sudoku_values[:,column]
    
    # # collect values in the given block
    row_block_range = get_indices_from_same_block(row)
    column_block_range = get_indices_from_same_block(column)
    block_values = sudoku_values[row_block_range][:,column_block_range]
    
    # # subtract (setdiff) appeared values from numbers 1 - 9
    appeared_values = np.append(np.append(row_values,column_values),block_values)
    possible_sudoku_values = np.arange(1,10)
    feasible_values = np.setdiff1d(possible_sudoku_values,appeared_values)
    return feasible_values

def solve_sudoku_simplistic(sudoku_values):
    """ Sudoku solver
    
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, to be solved
    
    Return:
        sudoku_values (9x9 ndarray), with empty cells (typically in the form
        of 0, but could be any number other than 1 - 9) filled
        
    Algorithm:
    For each unfilled cell, determine feasible values based on row, column and 
    block uniqueness
    - if there is only one feasible value, fill it
    - otherwise, wait
    """
    # print sudoku_values

    # # find empty cells
    flag_empty_cells = (sudoku_values <= 0) | (sudoku_values >= 10)
    number_of_cell_filled_this_round = 0
    
    # # while empty cells exist
    while flag_empty_cells.sum() > 0: 
        # # find row, column of empty cells
        positions_empty_cells = np.where(flag_empty_cells)
        rows_empty_cells = positions_empty_cells[0]
        columns_empty_cells = positions_empty_cells[1]
        for row, column in zip(rows_empty_cells,columns_empty_cells):
            # # find feasible values for the empty cell
            feasible_values = find_feasible_values(sudoku_values,row,column)
            
            # # if only one value is feasible, fill it
            if len(feasible_values) == 1:
                sudoku_values[row,column] = feasible_values[0]
                number_of_cell_filled_this_round += 1
                # print "Fill row {}, column {}, with {}".format(
                    # row,column,feasible_values[0])
                # print sudoku_values
            # # otherwise do nothing
            else:
                pass
                # print "Row {}, column {} can possibly be {}, no fill".format(row,column,feasible_values)
                
        # # no cell is filled, stuck
        if number_of_cell_filled_this_round == 0:
            break
            
        # # restart the process
        flag_empty_cells = (sudoku_values <= 0) | (sudoku_values >= 10)
        number_of_cell_filled_this_round = 0
    else:
        print "Finished!"
        print "Sudoku solved: {}".format(validate_sudoku(sudoku_values))
    return sudoku_values

def solve_sudoku(sudoku_values):
    flag_empty_cells = (sudoku_values <= 0) | (sudoku_values >= 10)
    number_empty_cells = flag_empty_cells.sum()
    if number_empty_cells > 0:
        # # find row, column of first empty cell
        positions_empty_cells = np.where(flag_empty_cells)
        row_first_empty_cell = positions_empty_cells[0][0]
        column_first_empty_cell = positions_empty_cells[1][0]
        feasible_values_first_empty_cell = find_feasible_values(
            sudoku_values,
            row_first_empty_cell,
            column_first_empty_cell)
        for value_first_empty_cell in feasible_values_first_empty_cell:
            print number_empty_cells, row_first_empty_cell, column_first_empty_cell, value_first_empty_cell
            new_sudoku_values = sudoku_values.copy()
            new_sudoku_values[row_first_empty_cell, column_first_empty_cell] = \
                value_first_empty_cell
            sudoku_solution = solve_sudoku(new_sudoku_values)
            if sudoku_solution is not None:
                return sudoku_solution
    elif validate_sudoku(sudoku_values):
        return sudoku_values
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Sudoku")
    parser.add_argument(
        "-f",dest="filename",metavar="FILENAME",
        help="Sudoku input filename")
    args = parser.parse_args()
    
    sudoku_values = np.loadtxt(args.filename,delimiter=",",dtype="i4")
    print sudoku_values
    sudoku_solution = solve_sudoku(sudoku_values)
    print sudoku_solution
    print "Sudoku solved: {}".format(validate_sudoku(sudoku_solution))
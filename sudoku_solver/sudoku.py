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
    
def exclude_values_appeared_in_same_row_column_block(sudoku_values,row,column):
    """ Return feasible values at the given row and column of a sudoku
    by excluding numbers that appear on the same row, same column, or same block
    
    Argument:
        sudoku_values (9x9 ndarray, required) -- given sudoku, can be partially or fully filled
        row (int, required) -- row number
        column (int, required) -- column number
    
    Returns:
        ndarray that contains the feasible values at the given row and column 
        of the sudoku
    
    Algorithm:
        - Any number that appears on the same row, same column, or same block is NOT feasible and excluded. The rest is feasible.
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

def _reformat_specified_rows_columns_into_tuple(rows,columns):
    """ Reorganize specified rows and columns into a tuple for looping
    
    This is supposed to be a private function called by find_feasible_values only.
    
    Argument: 
        rows (ndarray, required) -- single or multiple rows specified
        columns (ndarray, required) -- single or multiple columns specified
        
    Return:
        list of tuples that contains all the combinations of rows and columns.
        
    For example, rows = array([1,2]), columns = array([3,4]), the function 
    will return [(1,3),(1,4),(2,3),(2,4)]
    
    """
    mesh = np.meshgrid(rows,columns)
    rows_columns_tuple = zip(
        mesh[0].reshape((1,-1))[0],
        mesh[1].reshape((1,-1))[0])
    return rows_columns_tuple
    
def _find_values_infeasible_for_specified_rows_columns(
        sudoku_values,row,column,feasible_values,rows_columns_tuple):
    """ Find one number (among the remaining feasible values) is infeasible 
    for any other empty cell in the same block, same row, or same column
    
    This is supposed to be a private function called by find_feasible_values only.
    
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, can be partially or fully filled
        row (int, required) -- row number
        column (int, required) -- column number
        feasible_values (ndarray, required) -- returned from exclude_values_appeared_in_same_row_column_block(        sudoku_values,row,column)
        rows_columns_tuple (list of tuple, required) -- returned from _reformat_specified_rows_columns_into_tuple
        
    Return:
        ndarray that contains the feasible values at the given row and column 
        of the sudoku
        
    Note:
        If the number as described is found, the returned ndarray will only have one element. Otherwise, it will have the same output as exclude_values_appeared_in_same_row_column_block.
    
    
    """
    remaining_values = feasible_values.copy()
    for other_row, other_column in rows_columns_tuple:
        # # make sure cell is empty and different
        if ((sudoku_values[other_row,other_column] <= 0) \
            or (sudoku_values[other_row,other_column] >= 10)) \
            and ((other_row != row) or (other_column != column)):
            # # get feasible values for other cells
            other_feasible_values = \
                exclude_values_appeared_in_same_row_column_block(sudoku_values,other_row,other_column)
            # # subtract (setdiff) appeared values
            remaining_values = np.setdiff1d(
                remaining_values,
                other_feasible_values)
            # # no qualifying number is found
            if len(remaining_values) == 0:
                return None
    else:
        # # find the qualifying number
        if len(remaining_values) == 1:
            return remaining_values
    
def find_feasible_values(sudoku_values,row,column):
    """ Return feasible values at the given row and column of a sudoku
    
    Argument:
        sudoku_values (9x9 ndarray, required) -- given sudoku, can be partially or fully filled
        row (int, required) -- row number
        column (int, required) -- column number
    
    Returns:
        ndarray that contains the feasible values at the given row and column 
        of the sudoku
    
    Algorithm:
        - First, exclude_values_appeared_in_same_row_column_block is called to 
        exclude numbers that appear on the same row, same column, or same block
        - Then, among the remaining feasible values, if one number is infeasible
        for any other empty cell in the same block, same row, or same column, 
        that number is uniquely the cell value and other feasible values for 
        the cell become infeasible
    
    """
    feasible_values = exclude_values_appeared_in_same_row_column_block(
        sudoku_values,row,column)
    
    # # try to find one feasible value that is infeasible for 
    # # any other empty cell in the same block
    rows_columns_tuple = _reformat_specified_rows_columns_into_tuple(
        get_indices_from_same_block(row),
        get_indices_from_same_block(column))
    remaining_values = _find_values_infeasible_for_specified_rows_columns(
        sudoku_values,row,column,feasible_values,
        rows_columns_tuple)
    if remaining_values is not None:
        return remaining_values
            
    # # try to find one feasible value that is infeasible for 
    # # any other empty cell in the same row
    rows_columns_tuple = _reformat_specified_rows_columns_into_tuple(
        row,np.arange(9))
    remaining_values = _find_values_infeasible_for_specified_rows_columns(
        sudoku_values,row,column,feasible_values,
        rows_columns_tuple)
    if remaining_values is not None:
        return remaining_values
            
    # # try to find one feasible value that is infeasible for 
    # # any other empty cell in the same column
    rows_columns_tuple = _reformat_specified_rows_columns_into_tuple(
        np.arange(9),column)
    remaining_values = _find_values_infeasible_for_specified_rows_columns(
        sudoku_values,row,column,feasible_values,
        rows_columns_tuple)
    if remaining_values is not None:
        return remaining_values
    
    # # if none of the above works (i.e., returns anything)
    return feasible_values
    
def solve_sudoku_greedy(sudoku_values):
    """ Greedy sudoku solver
    
    Algorithm:
        Determine the feasible values for each unfilled cell, using find_feasible_values. If there is only one feasible value, fill it. Otherwise, wait. 
    
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, to be solved
    
    Return:
        sudoku_values (9x9 ndarray), with empty cells (typically in the form
        of 0, but could be any number other than 1 - 9) filled
    """
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
            
            # # if only one value is feasible, fill it, otherwise do nothing
            if len(feasible_values) == 1:
                sudoku_values[row,column] = feasible_values[0]
                number_of_cell_filled_this_round += 1
                
        # # no cell is filled, stuck
        if number_of_cell_filled_this_round == 0:
            break
            
        # # restart the process
        flag_empty_cells = (sudoku_values <= 0) | (sudoku_values >= 10)
        number_of_cell_filled_this_round = 0

    return sudoku_values
    
def solve_sudoku_combinatorial(sudoku_values):
    """ Combinatorial (recursive) sudoku solver
    
    Algorithm:
        Combinatorially fill the empty cells with feasible values until solution is found.
        The algorithm is implemented recursively: fill the first empty cell with one of the feasible values and apply the algorithm to the resulting sudoku. If the number of feasible values is 0 for some cell, this would be a dead end. Current function call will finish and not return anything. If all the cells are filled successfully, solution is found. By convention, published sudoku should have one unique solution.
        
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, to be solved
    
    Return:
        sudoku_values (9x9 ndarray), with empty cells (typically in the form
        of 0, but could be any number other than 1 - 9) filled        
    """
    # # find all the empty cells
    flag_empty_cells = (sudoku_values <= 0) | (sudoku_values >= 10)
    number_empty_cells = flag_empty_cells.sum()
    
    # # if sudoku unfinished
    if number_empty_cells > 0:
        # # find row, column of the first empty cell
        positions_empty_cells = np.where(flag_empty_cells)
        row_first_empty_cell = positions_empty_cells[0][0]
        column_first_empty_cell = positions_empty_cells[1][0]
        
        # # get all feasible values for the first empty cell
        feasible_values_first_empty_cell = find_feasible_values(
            sudoku_values,row_first_empty_cell,column_first_empty_cell)
        
        # # loop through each feasible value
        for value_first_empty_cell in feasible_values_first_empty_cell:
            # # fill in the feasible value and solve recursively
            new_sudoku_values = sudoku_values.copy()
            new_sudoku_values[row_first_empty_cell, column_first_empty_cell] = \
                value_first_empty_cell
            sudoku_solution = solve_sudoku(new_sudoku_values)
            
            # # pass the solution up the recursion chain
            if sudoku_solution is not None:
                return sudoku_solution
    
    # # sudoku filled successfully
    elif validate_sudoku(sudoku_values):
        return sudoku_values
        
def solve_sudoku(sudoku_values,flag_greedy=True,flag_combinatorial=True):
    """ Sudoku solver
    
    Algorithm:
		By default, first apply solve_sudoku_greedy, then apply solve_sudoku_combinatorial if the sudoku is not solved yet.
        The two flags are 
    
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, to be solved
    
    Return:
        sudoku_values (9x9 ndarray), with empty cells (typically in the form
        of 0, but could be any number other than 1 - 9) filled
    """
    if flag_greedy:
        sudoku_values = solve_sudoku_greedy(sudoku_values)
    if flag_combinatorial:
        sudoku_values = solve_sudoku_combinatorial(sudoku_values)
    return sudoku_values
    
def _int_to_str(int):
    """ Convert integer to string
    
    Padding a white space on each side
    Integers other than 1 - 9 is converted to white space
    
    """
    if int <= 0 or int >=10:
        return " "*3
    else:
        return " " + str(int) + " "
    
def pretty_print(sudoku_values):
    """ Pretty print the sudoku (incomplete or complete)
        
    Numbers other than 1 - 9 will not be printed
    
    Argument: 
        sudoku_values (9x9 ndarray, required) -- given sudoku, to be solved
    """
    print "|-----------+-----------+-----------|"
    for row in range(9):
        str_display = "|"
        for first_column in range(0,9,3):
            column_range = get_indices_from_same_block(first_column)
            str_display += " ".join(map(
                _int_to_str,sudoku_values[row,column_range])) + "|"
        print str_display
        if row == 2 or row == 5 or row == 8:
            print "|-----------+-----------+-----------|"
        else:
            print "|           |           |           |"
        
            
            
if __name__ == "__main__":
    # # config argument parser for command line input
    parser = argparse.ArgumentParser(description="Sudoku solver")
    parser.add_argument(
        "-i","--in-file",dest="in_filename",
        help="Sudoku input filename",required=True)
    parser.add_argument(
        "-o","--out-file",dest="out_filename",
        help="Sudoku output filename")
        
    # # mutually exclusive choice of greedy or combinatorial search
    # # by default (if nothing is specified), both search algorithms will be used
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-g","--greedy",action="store_true",
        help="Use only the greedy search to solve sudoku")
    group.add_argument(
        "-c","--combinatorial",action="store_true",
        help="Use only the combinatorial (recursive) search to solve sudoku")
    
    # # get command line input
    args = parser.parse_args()
    
    # # load sudoku
    sudoku_values = np.loadtxt(args.in_filename,delimiter=",",dtype="i4")
    print "The original sudoku:"
    pretty_print(sudoku_values)
    
    # # by default (if no flag is specified)
    # # first use greedy search then combinatorial (recursive) search
    if args.greedy is False and args.combinatorial is False:
        args.greedy = True
        args.combinatorial = True
        
    # # solve sudoku
    sudoku_solution = solve_sudoku(
        sudoku_values,
        flag_greedy=args.greedy,
        flag_combinatorial=args.combinatorial)
    if validate_sudoku(sudoku_solution):
        print "The sudoku is solved:"
    else:
        print "The sudoku is not finished yet:"
    pretty_print(sudoku_solution)
    
    # # write solution to csv file
    if args.out_filename is None:
        args.out_filename = 'solution.csv'
    np.savetxt(args.out_filename,sudoku_solution,delimiter=',',fmt='%d')
    
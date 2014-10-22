import numpy as np

def get_indices_from_same_block(index):
    """ Get indices that fall in the same block as the given index
    The sudoku values are zero indexed, so [0,1,2] form a block, 
    [3,4,5] form a block, and [6,7,8] form a block.
    For example, given index 5, return ndarray array([3,4,5]).
    """
    if index in np.array([0,1,2]):
        return np.array([0,1,2])
    elif index in np.array([3,4,5]):
        return np.array([3,4,5])
    elif index in np.array([6,7,8]):
        return np.array([6,7,8])
        
def sudoku_is_valid(sudoku_values):
    """ Test if sudoku solution is valid
    
    Argument:
        sudoku_values (ndarray, required) -- sudoku solution with shape (9,9)
        
    Return:
        True if the solution is valid:
            place the numbers 1 to 9 in the empty squares so that 
            each row, each column and each 3x3 block contains 
            the same number only once
        False otherwise
    """
    # # no values <=0 or >=10
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
    sudoku_values[row,column] = 0
    # # values in the given row
    row_values = sudoku_values[row,:]
    # # values in the given column
    column_values = sudoku_values[:,column]
    # # values in the given block
    row_block_range = get_indices_from_same_block(row)
    column_block_range = get_indices_from_same_block(column)
    block_values = sudoku_values[row_block_range][:,column_block_range]
    
    appearred_values = np.append(np.append(row_values,column_values),block_values)
    unique_appearred_values = np.unique(appearred_values)
    possible_sudoku_values = np.arange(1,10)
    feasible_values = np.setdiff1d(possible_sudoku_values,unique_appearred_values)
    return feasible_values
    
if __name__ == "__main__":
    input_filename = "../data/sudoku_1_in.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    
    # # try all possible combinations
    flag_not_answered = (sudoku_values <= 0) | (sudoku_values >= 10)
    count_not_answered = flag_not_answered.sum()

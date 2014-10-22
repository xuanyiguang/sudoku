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

if __name__ == "__main__":
    input_filename = "../data/sudoku_1_in.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    
    # # try all possible combinations
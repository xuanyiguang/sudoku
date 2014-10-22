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

def update_candidate_answers_exhaustive_search(candidate_answers):
    updated_answers = candidate_answers
    # # add one to the last element 
    updated_answers[-1] += 1
    for idx in range(len(updated_answers))[::-1]:
        if updated_answers[idx] > 9:
            updated_answers[idx] -= 9
            if idx-1 >= 0:
                updated_answers[idx-1] += 1
    return updated_answers
    
if __name__ == "__main__":
    input_filename = "../data/sudoku_1_in.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    
    # # try all possible combinations
    flag_not_answered = (sudoku_values <= 0) | (sudoku_values >= 10)
    count_not_answered = flag_not_answered.sum()
    candidate_answers = np.ones(count_not_answered,dtype="i4")
    print candidate_answers
    sudoku_values[flag_not_answered] = candidate_answers
    while not sudoku_is_valid(sudoku_values):
        candidate_answers = update_candidate_answers_exhaustive_search(
            candidate_answers)
        print candidate_answers
        if (candidate_answers == np.ones(count_not_answered,dtype="i4")).all():
            break
        sudoku_values[flag_not_answered] = candidate_answers
    else:
        print "Final Answer"
        print candidate_answers
        print sudoku_values
    
    
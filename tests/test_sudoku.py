import numpy as np
import pytest

from src.sudoku import *

def load_given_sudoku_answer():
    """ Load the sudoku answer provided in the challenge
    """
    input_filename = "../data/sudoku_1_out.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    return sudoku_values

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
        
def test_sudoku_validity_using_given_answer():
    """ The answer provided in the challenge is valid
    """
    sudoku_values = load_given_sudoku_answer()
    assert sudoku_is_valid(sudoku_values) == True
    
def test_sudoku_validity_sudoku_unfinished():
    """ If sudoku is unfinished (zero values), it is invalid
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly set one value to 0, sudoku is unfinished and invalid
    row_index = np.random.random_integers(0,8)
    column_index = np.random.random_integers(0,8)
    sudoku_values[row_index,column_index] = 0
    
    assert sudoku_is_valid(sudoku_values) == False
    
def test_sudoku_validity_violating_row_uniqueness():
    """ Test sudoku that violates row uniqueness
    The input is produced using a valid answer, and then randomly setting
    two values in the same row to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a row index and two column indices
    row_index = np.random.randint(9)
    column1_index = np.random.randint(9)
    column2_index = np.random.randint(9)
    while column2_index == column1_index: # make column1_index != column2_index
        column2_index = np.random.randint(9)
    sudoku_values[[row_index],[column2_index]] = \
        sudoku_values[[row_index],[column1_index]]
    
    assert sudoku_is_valid(sudoku_values) == False    
    
def test_sudoku_validity_violating_column_uniqueness():
    """ Test sudoku that violates column uniqueness
    The input is produced using a valid answer, and then randomly setting 
    two values in the same column to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a column index and two row indices
    column_index = np.random.randint(9)
    row1_index = np.random.randint(9)
    row2_index = np.random.randint(9)
    while row2_index == row1_index: # make row1_index != row2_index
        row2_index = np.random.randint(9)
    sudoku_values[[row2_index],[column_index]] = \
        sudoku_values[[row1_index],[column_index]]
    
    assert sudoku_is_valid(sudoku_values) == False
    
def test_sudoku_validity_violating_block_uniqueness():
    """ Test sudoku that violates block uniqueness
    The input is produced using a valid answer, and then randomly setting 
    two values in the same block to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a column index and two row indices
    row1_index = np.random.randint(9)
    column1_index = np.random.randint(9)
    row2_index = get_indices_from_same_block(row1_index)[
        np.random.randint(2)]
    column2_index = get_indices_from_same_block(column1_index)[
        np.random.randint(2)]
    while row2_index == row1_index and column2_index == column1_index:
        row2_index = get_indices_from_same_block(row1_index)[
            np.random.randint(2)]
        column2_index = get_indices_from_same_block(column1_index)[
            np.random.randint(2)]
    sudoku_values[[row2_index],[column2_index]] = \
        sudoku_values[[row1_index],[column1_index]]
    
    assert sudoku_is_valid(sudoku_values) == False

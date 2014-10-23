import numpy as np
import pytest

from src.sudoku import *

""" Unit tests for the following functions:
sudoku::validate_sudoku
sudoku::find_feasible_values
"""

def load_given_sudoku_answer():
    """ Load the sudoku answer provided in the challenge
    """
    input_filename = "../data/sudoku_example_out.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    return sudoku_values

def test_validate_sudoku_with_given_answer():
    """ The answer provided in the challenge should be valid
    """
    sudoku_values = load_given_sudoku_answer()
    assert validate_sudoku(sudoku_values) == True
    
def test_validate_sudoku_with_unfinished_sudoku():
    """ If sudoku is unfinished (having zero values), it is invalid
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly set one value to 0, sudoku is unfinished and invalid
    row = np.random.random_integers(0,8)
    column = np.random.random_integers(0,8)
    sudoku_values[row,column] = 0
    
    assert validate_sudoku(sudoku_values) == False
    
def test_validate_sudoku_violating_row_uniqueness():
    """ Test sudoku that violates row uniqueness
    
    The input is produced using a valid answer, and then randomly setting
    two values in the same row to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a row index and two column indices
    row = np.random.randint(9)
    column1 = np.random.randint(9)
    column2 = np.random.randint(9)
    while column2 == column1: # make column1 != column2
        column2 = np.random.randint(9)
    sudoku_values[[row],[column2]] = sudoku_values[[row],[column1]]
    
    assert validate_sudoku(sudoku_values) == False    
    
def test_validate_sudoku_violating_column_uniqueness():
    """ Test sudoku that violates column uniqueness
    
    The input is produced using a valid answer, and then randomly setting 
    two values in the same column to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a column index and two row indices
    column = np.random.randint(9)
    row1 = np.random.randint(9)
    row2 = np.random.randint(9)
    while row2 == row1: # make row1 != row2
        row2 = np.random.randint(9)
    sudoku_values[[row2],[column]] = sudoku_values[[row1],[column]]
    
    assert validate_sudoku(sudoku_values) == False
    
def test_validate_sudoku_violating_block_uniqueness():
    """ Test sudoku that violates block uniqueness
    
    The input is produced using a valid answer, and then randomly setting 
    two values in the same block to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly select two (different) cells that are in the same block
    row1 = np.random.randint(9)
    column1 = np.random.randint(9)
    row2 = get_indices_from_same_block(row1)[np.random.randint(2)]
    column2 = get_indices_from_same_block(column1)[np.random.randint(2)]
    while row2 == row1 and column2 == column1:
        row2 = get_indices_from_same_block(row1)[np.random.randint(2)]
        column2 = get_indices_from_same_block(column1)[np.random.randint(2)]
    sudoku_values[[row2],[column2]] = sudoku_values[[row1],[column1]]
    
    assert validate_sudoku(sudoku_values) == False

def test_find_feasible_values_one_feasible_value_with_valid_sudoku():
    """ Test the situation when only one value is feasible for the given cell
    
    The input is produced using a valid sudoku answer. Any randomly chosen 
    cell should only have one feasible value, which is the value in the cell.
    """
    sudoku_values = load_given_sudoku_answer()
    row = np.random.randint(9)
    column = np.random.randint(9)
    cell_value = sudoku_values[row,column]
    feasible_values = find_feasible_values(sudoku_values,row,column)
    assert len(feasible_values) == 1
    assert feasible_values[0] == cell_value
    
def test_find_feasible_values_one_feasible_value_with_incomplete_sudoku():
    """ Test the situation when only one value is feasible for the given cell
    
    The input is produced using a valid sudoku answer, and then delete 
    (replace with 0) a randomly selected number (say all the 5s) from the
    sudoku. There is just one feasible value for zero-valued cells.
    """
    sudoku_values = load_given_sudoku_answer()
    row = np.random.randint(9)
    column = np.random.randint(9)
    cell_value = sudoku_values[row,column]
    sudoku_values[sudoku_values == cell_value] = 0
    feasible_values = find_feasible_values(sudoku_values,row,column)
    
    assert len(feasible_values) == 1
    assert feasible_values[0] == cell_value
    
def test_find_feasible_values_two_feasible_values_with_incomplete_sudoku():
    """ Test the situation when two values are feasible for the given cell
    
    The input is produced using a valid sudoku answer, and then delete 
    (replace with 0) two randomly selected numbers (say all the 5s and 8s) 
    from the sudoku. There are two feasible values for any zero-valued cell.
    """
    sudoku_values = load_given_sudoku_answer()
    row = np.random.randint(9)
    column = np.random.randint(9)
    cell_value = sudoku_values[row,column]
    sudoku_values[sudoku_values == cell_value] = 0
    # # pick another (different) value
    another_cell_value = cell_value
    while another_cell_value == cell_value:
        another_cell_value = np.random.random_integers(9)
    sudoku_values[sudoku_values == another_cell_value] = 0
    feasible_values = find_feasible_values(sudoku_values,row,column)
    
    assert len(feasible_values) == 2
    assert set(feasible_values) == set([cell_value,another_cell_value])


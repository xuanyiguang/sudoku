import numpy as np
import pytest

from src.sudoku import *

def load_given_sudoku_answer():
    """ Load the sudoku answer provided in the challenge
    """
    input_filename = "../data/sudoku_1_out.csv"
    sudoku_values = np.loadtxt(input_filename,delimiter=",",dtype="i4")
    return sudoku_values

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
    row = np.random.random_integers(0,8)
    column = np.random.random_integers(0,8)
    sudoku_values[row,column] = 0
    
    assert sudoku_is_valid(sudoku_values) == False
    
def test_sudoku_validity_violating_row_uniqueness():
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
    
    assert sudoku_is_valid(sudoku_values) == False    
    
def test_sudoku_validity_violating_column_uniqueness():
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
    
    assert sudoku_is_valid(sudoku_values) == False
    
def test_sudoku_validity_violating_block_uniqueness():
    """ Test sudoku that violates block uniqueness
    The input is produced using a valid answer, and then randomly setting 
    two values in the same block to the same value.
    """
    sudoku_values = load_given_sudoku_answer()
    
    # # randomly generate a column index and two row indices
    row1 = np.random.randint(9)
    column1 = np.random.randint(9)
    row2 = get_indices_from_same_block(row1)[np.random.randint(2)]
    column2 = get_indices_from_same_block(column1)[np.random.randint(2)]
    while row2 == row1 and column2 == column1:
        row2 = get_indices_from_same_block(row1)[np.random.randint(2)]
        column2 = get_indices_from_same_block(column1)[np.random.randint(2)]
    sudoku_values[[row2],[column2]] = sudoku_values[[row1],[column1]]
    
    assert sudoku_is_valid(sudoku_values) == False

def test_update_candidate_answers_exhaustive_search_add_one_to_last_element():
    candidate_answers = np.array([1,1,1,1,5])
    expected_answers = np.array([1,1,1,1,6])
    updated_answers = update_candidate_answers_exhaustive_search(
        candidate_answers)
    assert (updated_answers == expected_answers).all()

def test_update_candidate_answers_exhaustive_search_last_element_is_9():
    candidate_answers = np.array([1,1,1,2,9])
    expected_answers = np.array([1,1,1,3,1])
    updated_answers = update_candidate_answers_exhaustive_search(
        candidate_answers)
    assert (updated_answers == expected_answers).all()
    
def test_update_candidate_answers_exhaustive_search_last_two_elements_are_9():
    candidate_answers = np.array([1,2,3,9,9])
    expected_answers = np.array([1,2,4,1,1])
    updated_answers = update_candidate_answers_exhaustive_search(
        candidate_answers)
    assert (updated_answers == expected_answers).all()
    
def test_update_candidate_answers_exhaustive_search_last_all_elements_are_9():
    candidate_answers = np.array([9,9,9,9,9])
    expected_answers = np.array([1,1,1,1,1])
    updated_answers = update_candidate_answers_exhaustive_search(
        candidate_answers)
    assert (updated_answers == expected_answers).all()
    
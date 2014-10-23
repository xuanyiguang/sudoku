import numpy as np
import pytest

from src.sudoku import *

""" User acceptance tests
Sudoku puzzles and solutions are given or come from online sources
"""

def verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename):
    sudoku_input = np.loadtxt(sudoku_input_filename,delimiter=",",dtype="i4")
    sudoku_output = solve_sudoku(sudoku_input)
    sudoku_expected_output = np.loadtxt(sudoku_output_filename,delimiter=",",dtype="i4")
    assert (sudoku_expected_output == sudoku_output).all()

def test_solve_sudoku_given_example():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files provided by the challenge
    """
    sudoku_input_filename = "../data/sudoku_example_in.csv"
    sudoku_output_filename = "../data/sudoku_example_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy1():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 1, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy1_in.csv"
    sudoku_output_filename = "../data/sudoku_easy1_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy2():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 2, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy2_in.csv"
    sudoku_output_filename = "../data/sudoku_easy2_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy3():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 3, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy3_in.csv"
    sudoku_output_filename = "../data/sudoku_easy3_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy4():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 4, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy4_in.csv"
    sudoku_output_filename = "../data/sudoku_easy4_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy5():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 5, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy5_in.csv"
    sudoku_output_filename = "../data/sudoku_easy5_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy6():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 6, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy6_in.csv"
    sudoku_output_filename = "../data/sudoku_easy6_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy7():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 7, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy7_in.csv"
    sudoku_output_filename = "../data/sudoku_easy7_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy8():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 8, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy8_in.csv"
    sudoku_output_filename = "../data/sudoku_easy8_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_easy9():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 9, easy)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_easy9_in.csv"
    sudoku_output_filename = "../data/sudoku_easy9_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)

def test_solve_sudoku_medium10():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 10, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium10_in.csv"
    sudoku_output_filename = "../data/sudoku_medium10_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium11():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 11, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium11_in.csv"
    sudoku_output_filename = "../data/sudoku_medium11_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium12():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 12, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium12_in.csv"
    sudoku_output_filename = "../data/sudoku_medium12_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium13():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 13, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium13_in.csv"
    sudoku_output_filename = "../data/sudoku_medium13_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium14():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 14, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium14_in.csv"
    sudoku_output_filename = "../data/sudoku_medium14_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium15():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 15, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium15_in.csv"
    sudoku_output_filename = "../data/sudoku_medium15_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium16():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 16, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium16_in.csv"
    sudoku_output_filename = "../data/sudoku_medium16_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_medium17():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 17, medium)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_medium17_in.csv"
    sudoku_output_filename = "../data/sudoku_medium17_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_hard18():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 18, hard)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_hard18_in.csv"
    sudoku_output_filename = "../data/sudoku_hard18_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_hard19():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 19, hard)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_hard19_in.csv"
    sudoku_output_filename = "../data/sudoku_hard19_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    
def test_solve_sudoku_hard20():
    """ Test if the sudoku solver gives the same solution
    
    Input and output files are from online (Sample problem 20, hard)
    http://www.nikoli.com/en/puzzles/sudoku/
    """
    sudoku_input_filename = "../data/sudoku_hard20_in.csv"
    sudoku_output_filename = "../data/sudoku_hard20_out.csv"
    verify_sudoku_solution(sudoku_input_filename, sudoku_output_filename)
    

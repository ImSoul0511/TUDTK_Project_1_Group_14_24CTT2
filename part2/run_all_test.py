import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import AutoTestReporter
from test_case import *
from verification import *
from decomposition import run_svd_tests
from diagonalization import run_diagonalize_tests

def run_all_tests():
    """
    Chạy tất cả các unit test.

    Args:
        None

    Returns:
        None
    """
    run_svd_tests(SVD_TEST_CASES)
    run_diagonalize_tests(DIAGONALIZATION_TEST_CASES)
    

if __name__ == "__main__":
    run_all_tests()
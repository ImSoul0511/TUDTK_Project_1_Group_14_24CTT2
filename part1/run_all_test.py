import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from test_case import *
from verification import verify_test_verify_solution
from gaussian import verify_test_back_substitution, verify_test_gaussian_eliminate
from inverse import verify_test_inverse
from determinant import verify_test_determinant
from rank_basis import verify_test_rank_and_basis


def run_all_tests():
    """
    Chạy tất cả các unit test.

    Args:
        None

    Returns:
        None
    """
    verify_test_back_substitution(BACK_SUBSTITUTION_TEST_CASES)
    verify_test_gaussian_eliminate(GAUSSIAN_ELIMINATE_TEST_CASES)
    verify_test_inverse(INVERSE_TEST_CASES)
    verify_test_determinant(DETERMINANT_TEST_CASES)
    verify_test_rank_and_basis(RANK_BASIS_TEST_CASES)
    verify_test_verify_solution(VERIFY_SOLUTION_TEST_CASES)

if __name__ == "__main__":
    run_all_tests()
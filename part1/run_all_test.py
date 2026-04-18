import sys
import os
import time

# Thêm parent directory vào path để lấy config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import AutoTestReporter

from test_case import (
    BACK_SUBSTITUTION_TEST_CASES,
    DETERMINANT_TEST_CASES,
    GAUSSIAN_ELIMINATE_TEST_CASES,
    INVERSE_TEST_CASES,
    RANK_BASIS_TEST_CASES,
    VERIFY_SOLUTION_TEST_CASES
)

from gaussian import verify_test_back_substitution, verify_test_gaussian_eliminate
from determinant import verify_test_determinant
from inverse import verify_test_inverse
from rank_basis import verify_test_rank_and_basis
from verification import verify_test_verify_solution


def print_section_divider(title: str):
    """Hàm hỗ trợ in tiêu đề phân khu nổi bật"""
    print(f"\n{AutoTestReporter.COLOR_WARNING}{AutoTestReporter.STYLE_BOLD}")
    print(f"{'='*56}")
    print(f"PHÂN KHU: {title.upper()}")
    print(f"{'='*56}")
    print(f"{AutoTestReporter.STYLE_RESET}")

def main():
    print(f"{AutoTestReporter.COLOR_CYAN}{AutoTestReporter.STYLE_BOLD}")
    print("============================================================")
    print("KHỞI ĐỘNG HỆ THỐNG AUTO-GRADER - ĐỒ ÁN TOÁN ỨNG DỤNG")
    print("============================================================")
    print(f"{AutoTestReporter.STYLE_RESET}")
    
    start_time = time.time()
    
    
    # NHÓM 1: TÌM NGHIỆM HỆ PHƯƠNG TRÌNH
    print_section_divider("Giải Hệ Phương Trình")
    verify_test_back_substitution(BACK_SUBSTITUTION_TEST_CASES)
    verify_test_gaussian_eliminate(GAUSSIAN_ELIMINATE_TEST_CASES)
    verify_test_verify_solution(VERIFY_SOLUTION_TEST_CASES)
    
    # NHÓM 2: TÍNH ĐỊNH THỨC
    print_section_divider("Tính Định Thức Ma Trận")
    verify_test_determinant(DETERMINANT_TEST_CASES)
    
    # NHÓM 3: TÌM MA TRẬN NGHỊCH ĐẢO
    print_section_divider("Ma Trận Nghịch Đảo")
    verify_test_inverse(INVERSE_TEST_CASES)
    
    # NHÓM 4: TÌM HẠNG VÀ CƠ SỞ
    print_section_divider("Hạng Và Cơ Sở (Rank & Basis)")
    verify_test_rank_and_basis(RANK_BASIS_TEST_CASES)
    
    print_section_divider("Hàm Kiểm Chứng Bằng Numpy")
    verify_test_verify_solution(VERIFY_SOLUTION_TEST_CASES)
    end_time = time.time()
    
    # TỔNG KẾT TOÀN BỘ
    print(f"\n{AutoTestReporter.COLOR_GREEN}{AutoTestReporter.STYLE_BOLD}")
    print("============================================================")
    print(f"HOÀN TẤT TOÀN BỘ KIỂM THỬ TRONG {end_time - start_time:.4f} GIÂY!")
    print("============================================================")
    print(f"{AutoTestReporter.STYLE_RESET}")

if __name__ == "__main__":
    main()
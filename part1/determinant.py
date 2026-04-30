import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cfg
from test_case import DETERMINANT_TEST_CASES

def determinant(matrix_A):
    """
    Tính định thức của ma trận bằng khử Gauss.
    Args:
        matrix_A: Ma trận hệ số.
    Returns:
        float: Giá trị định thức (0.0 nếu ma trận suy biến).
    """
    if not matrix_A or not matrix_A[0]:
        return 0.0
    n = len(matrix_A)
    # Kiểm tra tính vuông của ma trận
    for row in matrix_A:
        if len(row) != n:
            raise ValueError("Ma trận không vuông, không thể tính định thức.")
            
    M = [row[:] for row in matrix_A]
    det = 1.0
    s = 0

    for i in range(n):
        # Tìm phần tử chốt (pivot) lớn nhất trên cột i
        pivot_row = i
        max_val = abs(M[i][i])
        for k in range(i + 1, n):
            if abs(M[k][i]) > max_val:
                max_val = abs(M[k][i])
                pivot_row = k
        
        # Báo lỗi nếu cột toàn số 0 (ma trận suy biến)
        if cfg.is_zero(max_val):
            # Không có pivot tại cột i
            return 0.0
            
        # Hoán đổi dòng và đổi dấu định thức nếu có đổi chỗ
        if pivot_row != i:
            M[i], M[pivot_row] = M[pivot_row], M[i]
            s += 1
            
        det *= M[i][i]
        
        # Khử Gauss các phần tử bên dưới đường chéo chính
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(i + 1, n):
                M[j][k] -= factor * M[i][k]
                
    return ((-1) ** s) * det


def verify_test_determinant(test_cases: list[dict]):
    """
    Kiểm thử hàm tính định thức.
    Args:
        test_cases: Danh sách các bộ test.
    Returns:
        None
    """
    import warnings
    import numpy as np
    warnings.simplefilter("ignore", UserWarning) # Bỏ qua warning pivot nhỏ    
    passed_count = 0
    total_count = len(test_cases)
    cfg.AutoTestReporter.print_header("KIỂM THỬ ĐỊNH THỨC")

    for case in test_cases:
        try:
            # Nếu test case kỳ vọng ném ra lỗi (VD: ma trận không vuông 2x3)
            if "should_raise" in case:
                try:
                    d = determinant(case["Ma trận A"])
                    cfg.AutoTestReporter.print_result(case['Nội dung'], False, "Lẽ ra phải phát sinh lỗi")
                except case["should_raise"] as err:
                    cfg.AutoTestReporter.print_result(case['Nội dung'], True, f"\n-> Bắt đúng lỗi: {type(err).__name__}:{err}")
                    passed_count += 1
                continue

            # Tính toán định thức bình thường
            d = determinant(case["Ma trận A"])
            expected = case["expected_answer"]
            
            # Sử dụng np.isclose để trị sai số dấu phẩy động (đây là điều bắt buộc khi tính toán số thực trên máy tính)
            if np.isclose(d, expected, atol=1e-7):
                cfg.AutoTestReporter.print_result(case['Nội dung'], True, f"(det = {d:.4f})")
                passed_count += 1
            else:
                cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"-> Tính ra: {d}, Kỳ vọng: {expected}")
        except Exception as err:
            cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"-> Lỗi Runtime: {err}")
            
    cfg.AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import DETERMINANT_TEST_CASES
    verify_test_determinant(DETERMINANT_TEST_CASES)
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
from config import AutoTestReporter
from verification import verify_inverse_numpy as verify_inverse

def inverse(matrix_A):
    """
    Tính ma trận nghịch đảo A^-1 bằng phương pháp Gauss-Jordan có Partial Pivoting.

    Args:
        matrix_A: Ma trận hệ số
    
    Returns:
        Ma trận nghịch đảo

    """
    n = len(matrix_A)
    # 1. Kiểm tra ma trận có vuông không
    for row in matrix_A:
        if len(row) != n:
            raise ValueError("Ma trận không vuông, không thể tìm nghịch đảo.")
    # 2. Tạo ma trận  M = [A | I]
    M = []
    for i in range(n):
        row_A = [element for element in matrix_A[i]]
        row_I=[1.0 if i==j else 0.0 for j in range(n) ]
        M.append(row_A + row_I)

    # 3. Quá trình khử Gauss-Jordan
    for k in range(n):
        #a. Tìm dòng p có phần tử chốt lớn nhất từ dòng k trở xuống
        p = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[p][k]):
                p=i
        if config.is_zero(M[p][k]):
            print(f"Không có pivot tại cột {k}")
            return None
        # b. Hoán đổi dòng p và dòng k nếu cần
        if p != k:
            M[k], M[p] = M[p], M[k]
        # c. Chuẩn hóa dòng k
        pivot_val = M[k][k]
        for j in range(k, 2 * n):
            M[k][j] /= pivot_val
        # d. Khử Gauss-Jordan
        for i in range(n):
            if i != k:
                factor = M[i][k]
                for j in range(k, 2 * n):
                    M[i][j]=M[i][j]-factor*M[k][j]
    #4. Ma trận nghịch đảo
    inverse_matrix = []
    for i in range(n):
        inverse_matrix.append(M[i][n:])
    return inverse_matrix


def verify_test_inverse(test_cases: list[dict]):
    import warnings
    warnings.simplefilter("ignore", UserWarning)
    
    # Hàm chạy các bộ test cho thuật toán tìm ma trận nghịch đảo
    AutoTestReporter.print_suite_header("Ma Trận Nghịch Đảo (Inverse)")
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        try:
            inv_A = inverse(case["input"])
            if case.get("should_raise"):
                AutoTestReporter.print_result(case['name'], False, "Lẽ ra phải phát sinh ValueError")
                continue
                
            expected = case.get("expected_inv")
            if expected:
                import numpy as np
                assert np.allclose(inv_A, expected, atol=1e-7), "Ma trận nghịch đảo không khớp expected"
            else:
                # Nếu không có expected cụ thể, tự nhân ngược lại với A để kiểm tra bằng hàm verify_inverse
                # Định lý: A * A^-1 sẽ ra ma trận đơn vị I
                assert verify_inverse(case["input"], inv_A), "AA^-1 không bằng ma trận đơn vị I"
                
            AutoTestReporter.print_result(case['name'], True)
            passed_count += 1
            
        except ValueError as err:
            if case.get("should_raise") == ValueError:
                AutoTestReporter.print_result(case['name'], True, f"(Bắt đúng lỗi: {err})")
                passed_count += 1
            else:
                AutoTestReporter.print_result(case['name'], False, f"(Lỗi ngoài mong đợi: {err})")
        except AssertionError as err:
            AutoTestReporter.print_result(case['name'], False, f"(Assertion: {err})")
            
    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import INVERSE_TEST_CASES
    verify_test_inverse(INVERSE_TEST_CASES)


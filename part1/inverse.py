import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cfg
from verification import verify_inverse_numpy as verify_inverse

def inverse(matrix_A):
    """
    Tìm ma trận nghịch đảo bằng khử Gauss-Jordan.
    Args:
        matrix_A: Ma trận vuông.
    Returns:
        list: Ma trận nghịch đảo hoặc None nếu không tồn tại.
    """
    n = len(matrix_A)
    # Kiểm tra ma trận có vuông không
    for row in matrix_A:
        if len(row) != n:
            raise ValueError("Ma trận không vuông, không thể tìm nghịch đảo.")
    # Tạo ma trận  M = [A | I]
    M = []
    for i in range(n):
        row_A = [element for element in matrix_A[i]]
        row_I=[1.0 if i==j else 0.0 for j in range(n) ]
        M.append(row_A + row_I)

    # Quá trình khử Gauss-Jordan
    for k in range(n):
        #a. Tìm dòng p có phần tử chốt lớn nhất từ dòng k trở xuống
        p = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[p][k]):
                p=i
        if cfg.is_zero(M[p][k]):
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
    # Ma trận nghịch đảo
    inverse_matrix = []
    for i in range(n):
        inverse_matrix.append(M[i][n:])
    return inverse_matrix


def verify_test_inverse(test_cases: list[dict]):
    """
    Kiểm thử hàm tìm ma trận nghịch đảo.
    Args:
        test_cases: Danh sách các bộ test.
    Returns:
        None
    """
    import warnings
    warnings.simplefilter("ignore", UserWarning)
    passed_count = 0
    total_count = len(test_cases)
    cfg.AutoTestReporter.print_header("KIỂM THỬ MA TRẬN NGHỊCH ĐẢO")
    for case in test_cases:
        try:
            inv_A = inverse(case["Ma trận A"])
            if case.get("should_raise"):
                cfg.AutoTestReporter.print_result(case['Nội dung'], False, "Lẽ ra phải phát sinh ValueError")
                continue
                
            expected = case.get("expected_answer")
            if expected:
                import numpy as np
                assert np.allclose(inv_A, expected, atol=1e-7), "Ma trận nghịch đảo không khớp expected"
            else:
                # Nếu không có expected cụ thể, tự nhân ngược lại với A để kiểm tra bằng hàm verify_inverse
                # Định lý: A * A^-1 sẽ ra ma trận đơn vị I
                assert verify_inverse(case["Ma trận A"], inv_A), "AA^-1 không bằng ma trận đơn vị I"
                
            cfg.AutoTestReporter.print_result(case['Nội dung'], True)
            passed_count += 1
            
        except ValueError as err:
            if case.get("should_raise") == ValueError:
                cfg.AutoTestReporter.print_result(case['Nội dung'], True, f"\n -> Bắt đúng lỗi: {err}")
                passed_count += 1
            else:
                cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"\n -> Lỗi ngoài mong đợi: {err}")
        except AssertionError as err:
            cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"\n -> Lỗi ngoài mong đợi: {err}")
            
    cfg.AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import INVERSE_TEST_CASES
    verify_test_inverse(INVERSE_TEST_CASES)


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import config as cfg

def verify_solution(A, b, x_custom):
    """
    Kiểm chứng kết quả bằng NumPy

    Args:
        A: Ma trận hệ số
        b: Vector vế phải
        x_custom: nghiệm
    
    Return:
        True: Kết quả của bạn Khớp
        False: Kết quả của bạn Sai

    """
    # Xử lý kiểm tra cho trường hợp hệ vô số nghiệm / vô nghiệm (x là chuỗi hoặc x = None)
    if isinstance(x_custom, str) or x_custom is None:
        try:
            np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
            return False 
        except (np.linalg.LinAlgError, ValueError):
            return True 
        
    # Dùng numpy để kiểm tra lại trường hợp có nghiệm duy nhất
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    x_np = np.array(x_custom, dtype=float)

    # Kiểm tra xem A * x có xấp xỉ bằng b không
    return np.allclose(np.dot(A_np, x_np), b_np)

def verify_determinant_numpy(matrix_A, custom_det):
    """
    Kiểm chứng kết quả định thức bằng NumPy

    Args:
        matrix_A: Ma trận hệ số
        custom_det: Giá trị định thức
    
    Returns:
        True: Nếu trùng khớp
        False: Nếu không trùng khớp
    """
    if not matrix_A:
        return custom_det == 0.0
    
    A_np = np.array(matrix_A, dtype=float)
    numpy_det = np.linalg.det(A_np)
    
    # Sử dụng isclose vì tính toán số thực luôn có sai số nhỏ
    return np.isclose(custom_det, numpy_det)


def verify_inverse_numpy(matrix_A, inverse_A):
    """
    Kiểm chứng AA^-1 = I và so sánh kết quả với NumPy.

    Args:
        matrix_A: Ma trận hệ số
        inverse_A: Ma trận nghịch đảo
    
    Returns:
        True: Nếu tích AA^{-1} ra đúng ma trận đơn vị
        False: Nếu tích ra sai
    """
    # Kiểm tra xem inverse_A có tồn tại không (tránh lỗi khi hàm inverse tạch)
    if inverse_A is None:
        det_A = np.linalg.det(np.array(matrix_A, dtype=float))
        if cfg.is_zero(det_A): 
            return True 
        else:
            return False 
        
    # 1. Kiểm tra kích thước trước khi tính toán để tránh lỗi Broadcast
    rows_A = len(matrix_A)
    cols_A = len(matrix_A[0])
    rows_inv = len(inverse_A)
    cols_inv = len(inverse_A[0])

    # Ma trận nghịch đảo phải vuông và cùng kích thước với ma trận gốc
    if rows_A != cols_A or rows_inv != cols_inv or rows_A != rows_inv:
        return False
    
    A_np = np.array(matrix_A, dtype=float)
    inv_custom_np = np.array(inverse_A, dtype=float)
    n = len(matrix_A)

    # 1. Kiểm tra điều kiện AA^-1 = I
    # Tính tích A * A^-1
    identity_check = np.dot(A_np, inv_custom_np)
    I_matrix = np.eye(n)
    
    # Kiểm tra xem tích có xấp xỉ ma trận đơn vị không
    is_identity = np.allclose(identity_check, I_matrix)

    # 2. So sánh trực tiếp với kết quả của NumPy
    try:
        inv_numpy = np.linalg.inv(A_np)
        matches_numpy = np.allclose(inv_custom_np, inv_numpy)
    except np.linalg.LinAlgError:
        matches_numpy = False

    return is_identity and matches_numpy

def verify_rank_and_basis_numpy(A, rank_custom, row_basis, col_basis, null_basis):
    """
    Kiểm chứng  hạng và cơ sở của không gian dòng, không gian cột, 
    và không gian nghiệm bằng Numpy

    Args:
        A: Ma trận hệ số
        rank_custom: Hạng ma trận
        row_basis: cơ sở không gian dòng
        col_basis: Cơ sở không gian cột
        null_basis: Cơ sở không gian nghiệm
    
    Returns:
        True: Nếu trùng khớp
        False: Nếu không trùng khớp
    """
    A_np = np.array(A, dtype=float)
    rows, cols = A_np.shape

    # --- 1. Kiểm tra Hạng (Rank) ---
    rank_np = np.linalg.matrix_rank(A_np)
    check_rank = (rank_custom == rank_np)

    # --- 2. Kiểm tra Không gian dòng (Row Space) ---
    # Các vector trong row_basis phải độc lập tuyến tính và có số lượng = rank
    check_row = False
    if len(row_basis) == rank_custom:
        # Cơ sở dòng tìm được phải có cùng không gian dòng với ma trận A gốc
        if np.linalg.matrix_rank(np.vstack((A_np, np.array(row_basis)))) == rank_custom:
            check_row = True

    # --- 3. Kiểm tra Không gian cột (Column Space) ---
    check_col = False
    if len(col_basis) == rank_custom:
        # Cơ sở cột tìm được phải có cùng không gian cột với ma trận A gốc
        if np.linalg.matrix_rank(np.hstack((A_np, np.array(col_basis).T))) == rank_custom:
            check_col = True

    # --- 4. Kiểm tra Không gian nghiệm (Null Space) ---
    # A * v phải = 0 và số lượng vector = cols - rank
    check_null = True
    if len(null_basis) != (cols - rank_custom):
        check_null = False
    else:
        for v in null_basis:
            if not np.allclose(np.dot(A_np, np.array(v)), 0, atol=cfg.EPSILON):
                check_null = False
                break

    return check_rank, check_row, check_col, check_null
    

def verify_test_verify_solution(test_cases: list[dict]): 
    """
    Hàm tự kiểm thử (Self-test) cho chính hàm verify_solution.
    Nó dùng Numpy làm 'trọng tài' để xác nhận hàm verify của chúng ta báo đúng hay sai.
    """
    import numpy as np
    from config import AutoTestReporter
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        e = verify_solution(case['A'], case['b'], case['x'])

        try:
            A_np = np.array(case['A'], dtype=float)
            b_np = np.array(case['b'], dtype=float)
            x_given = np.array(case['x'], dtype=float)

            if case.get("expect_mismatch"):
                if e == False: 
                    AutoTestReporter.print_result(case['Nội dung'], True)
                    passed_count += 1
                else:
                    AutoTestReporter.print_result(case['Nội dung'], False)

            else:
                # Trường hợp nghiệm chuẩn
                try:
                    x_np = np.linalg.solve(A_np, b_np)
                    matches_np = np.allclose(x_np, x_given, atol=1e-9)
                except np.linalg.LinAlgError:
                    matches_np = True # Coi như chấp nhận nếu hệ đặc biệt
                
                if e == matches_np:
                    AutoTestReporter.print_result(case['Nội dung'], True)
                    passed_count += 1
                else:
                    AutoTestReporter.print_result(case['Nội dung'], False)

        except Exception as ex:
            AutoTestReporter.print_result(case['Nội dung'], False, f"\n-> Lỗi Runtime: {ex}")

    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import *
    verify_test_verify_solution(VERIFY_SOLUTION_TEST_CASES)
 
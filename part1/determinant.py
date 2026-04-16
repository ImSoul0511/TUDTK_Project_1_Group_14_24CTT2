import config
from config import AutoTestReporter

def determinant(matrix_A):
    """
    Tính định thức của ma trận qua khử Gauss

    Args:
        A: Ma trận hệ số
    
    Return:
        Giá trị định thức
        Hoặc 0.0 nếu suy biến
        
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
        # 1. Tìm phần tử chốt (pivot) lớn nhất trên cột i
        pivot_row = i
        max_val = abs(M[i][i])
        for k in range(i + 1, n):
            if abs(M[k][i]) > max_val:
                max_val = abs(M[k][i])
                pivot_row = k
        
        # 2. Báo lỗi nếu cột toàn số 0 (ma trận suy biến)
        if config.is_zero(max_val):
            # Không có pivot tại cột i
            return 0.0
            
        # 3. Hoán đổi dòng và đổi dấu định thức nếu có đổi chỗ
        if pivot_row != i:
            M[i], M[pivot_row] = M[pivot_row], M[i]
            s += 1
            
        det *= M[i][i]
        
        # 4. Khử Gauss các phần tử bên dưới đường chéo chính
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(i + 1, n):
                M[j][k] -= factor * M[i][k]
                
    return ((-1) ** s) * det


def verify_test_determinant(test_cases: list[dict]):
    import warnings
    import numpy as np
    warnings.simplefilter("ignore", UserWarning) # Bỏ qua warning pivot nhỏ    
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        try:
            # 1. Nếu test case kỳ vọng ném ra lỗi (VD: ma trận không vuông 2x3)
            if "should_raise" in case:
                try:
                    d = determinant(case["Ma trận A"])
                    AutoTestReporter.print_result(case['Nội dung'], False, "Lẽ ra phải phát sinh lỗi")
                except case["should_raise"] as err:
                    AutoTestReporter.print_result(case['Nội dung'], True, f"\n-> Bắt đúng lỗi: {type(err).__name__}:{err}")
                    passed_count += 1
                continue

            # 2. Tính toán định thức bình thường
            d = determinant(case["Ma trận A"])
            expected = case["expected_answer"]
            
            # Sử dụng np.isclose để trị sai số dấu phẩy động (đây là điều bắt buộc khi tính toán số thực trên máy tính)
            if np.isclose(d, expected, atol=1e-7):
                AutoTestReporter.print_result(case['Nội dung'], True, f"(det = {d:.4f})")
                passed_count += 1
            else:
                AutoTestReporter.print_result(case['Nội dung'], False, f"-> Tính ra: {d}, Kỳ vọng: {expected}")
        except Exception as err:
            AutoTestReporter.print_result(case['Nội dung'], False, f"-> Lỗi Runtime: {err}")
            
    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import DETERMINANT_TEST_CASES
    verify_test_determinant(DETERMINANT_TEST_CASES)
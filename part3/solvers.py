import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config


from part1.gaussian import gaussian_eliminate, back_substitution
from part2.decomposition import svd

def is_diagonally_dominant(A: list[list[float]]) -> bool:
    """
    Kiểm tra ma trận có chéo trội chặt hàng không.
    Điều kiện: |a_ii| > sum(|a_ij|) với mọi j != i
    """


def gauss_seidel_iteration(A: list[list[float]], b: list[float], max_iter=1000, tol=1e-9) -> list[float]:
    """
    Cài đặt thuật toán lặp Gauss-Seidel.
    Gợi ý cho Khoa:
    1. Khởi tạo x = vector 0.
    2. Lặp max_iter lần.
    3. Trong mỗi lần lặp, cập nhật từng thành phần x_i dựa trên công thức.
    4. Kiểm tra điều kiện dừng: Nếu ||x_new - x_old|| < tol thì break.
    """
    pass 

def solve_system(A: list[list[float]], b: list[float], method: str) -> list[float]:
    """
    Hàm router phân luồng phương pháp giải.
    """
    if method == 'gauss':
        # Gợi ý: Gọi gaussian_eliminate(A, b). Nhớ xử lý kết quả trả về.
        # Lưu ý hàm của Khải trả về (M, x, swaps) hoặc (M, formula, swaps)
        pass 

    elif method == 'svd':
        # Gợi ý: 
        # 1. Gọi U, Sigma, Vt = svd(A)
        # 2. Tính giả nghịch đảo Sigma_plus: 1/sigma_i nếu sigma_i > EPSILON, ngược lại = 0
        # 3. Nghiệm x = Vt^T * Sigma_plus * U^T * b (Nên cast sang numpy dùng np.dot cho lẹ)
        pass

    elif method == 'gauss_seidel':
        if not is_diagonally_dominant(A): 
            raise ValueError("Ma trận không chéo trội chặt hàng, Gauss-Seidel không đảm bảo hội tụ.")
        return gauss_seidel_iteration(A, b) 

        
    else:
        raise ValueError(f"Phương pháp {method} không hợp lệ.")
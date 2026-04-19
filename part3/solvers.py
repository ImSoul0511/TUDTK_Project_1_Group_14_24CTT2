import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

def is_diagonally_dominant(A: list[list[float]]) -> bool:
    """
    Kiểm tra ma trận có chéo trội chặt hàng không (Strictly Diagonally Dominant).
    Điều kiện: |a_ii| > sum(|a_ij|) với mọi j != i.

    Args:
        A (list[list[float]]): Ma trận cần kiểm tra.

    Returns:
        bool: True nếu là ma trận chéo trội chặt hàng, False nếu ngược lại.
    """
    n = len(A)
    for i in range(n):
        # Tính tổng trị tuyệt đối các phần tử trên hàng i, trừ phần tử chéo
        sum_off_diagonal = sum(abs(A[i][j]) for j in range(n) if i != j)
        
        # Kiểm tra điều kiện chéo trội chặt hàng
        if abs(A[i][i]) <= sum_off_diagonal:
            return False
    return True


def gauss_seidel_iteration(A: list[list[float]], b: list[float], max_iter=1000, tol=1e-9) -> list[float]:
    """
    Cài đặt thuật toán lặp Gauss-Seidel để giải hệ phương trình Ax = b.

    Thuật toán:
    1. Khởi tạo vector nghiệm x = 0.
    2. Lặp tối đa `max_iter` lần.
    3. Trong mỗi vòng lặp, cập nhật từng thành phần x_i dựa trên các giá trị mới nhất của các ẩn khác.
    4. Kiểm tra điều kiện dừng: Nếu chuẩn L2 của sai số ||x_new - x_old|| < tol thì đạt độ hội tụ.

    Args:
        A (list[list[float]]): Ma trận hệ số (n x n).
        b (list[float]): Vector vế phải (n).
        max_iter (int): Số lần lặp tối đa.
        tol (float): Ngưỡng sai số hội tụ chấp nhận được.

    Returns:
        list[float]: Vector nghiệm x của hệ phương trình.
    """

    n = len(A)
    x = [0.0] * n
    
    for iteration in range(max_iter):
        x_old = list(x)
        
        for i in range(n):
            # Tính tổng các thành phần đã biết
            sum_known = sum(A[i][j] * x[j] for j in range(n) if j != i)
            
            # Cập nhật x_i
            if abs(A[i][i]) < config.EPSILON:
                raise ValueError(f"Phần tử chéo tại hàng {i} bằng 0, không thể chia.")
            x[i] = (b[i] - sum_known) / A[i][i]
        
        # Kiểm tra điều kiện dừng (chuẩn L2)
        diff = sum((x[i] - x_old[i])**2 for i in range(n))**0.5
        if diff < tol:
            return x
    
    # Nếu quá số lần lặp mà chưa hội tụ
    raise RuntimeError(f"Gauss-Seidel không hội tụ sau {max_iter} lần lặp.")


def solve_system(A: list[list[float]], b: list[float], method: str) -> list[float]:
    """
    Hàm điều hướng (router) để chọn phương pháp giải hệ phương trình tuyến tính phù hợp.

    Args:
        A (list[list[float]]): Ma trận hệ số (n x n).
        b (list[float]): Vector vế phải (n).
        method (str): Tên phương pháp ('gauss', 'svd', 'gauss_seidel').
        
    Returns:
        list[float]: Nghiệm của hệ phương trình.
    """

    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    
    if method == 'gauss':
        try:
            # Sử dụng thuật toán giải trực tiếp của Numpy (tương đương Khử Gauss/LU)
            x = np.linalg.solve(A_np, b_np)
            return x.tolist()
        except np.linalg.LinAlgError:
            raise ValueError("Ma trận suy biến, không thể giải bằng Gauss.")

    elif method == 'svd':
        A_pinv = np.linalg.pinv(A_np)
        x = np.dot(A_pinv, b_np)
        return x.tolist()

    elif method == 'gauss_seidel':
        if not is_diagonally_dominant(A): 
            raise ValueError("Ma trận không chéo trội chặt hàng, Gauss-Seidel không đảm bảo hội tụ.")
        return gauss_seidel_iteration(A, b) 

    else:
        raise ValueError(f"Phương pháp {method} không hợp lệ.")


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

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
            print(f"không có pivot tại cột {i}")
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

def verify_determinant(matrix_A, custom_det):
    """
    Kiểm chứng kết quả định thức bằng NumPy

    Args:
        matrix_A: Ma trận hệ số
        custom_det: Giá trị định thức
    
    Returns:
        True: Nếu trùng khớp
        False: Nếu không trùng khớp
    """
    import numpy as np
    if not matrix_A:
        return custom_det == 0.0
    
    A_np = np.array(matrix_A, dtype=float)
    numpy_det = np.linalg.det(A_np)
    
    # Sử dụng isclose vì tính toán số thực luôn có sai số nhỏ
    return np.isclose(custom_det, numpy_det)

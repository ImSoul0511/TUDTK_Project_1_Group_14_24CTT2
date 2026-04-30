import math
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
import numpy as np

def matrix_transpose(A):
    """
    Tìm ma trận chuyển vị.

    Args:
        A: Ma trận đầu vào.

    Returns:
        list: Ma trận chuyển vị.
    """
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def matrix_multiply(A, B):
    """
    Nhân hai ma trận.

    Args:
        A: Ma trận trái.
        B: Ma trận phải.

    Returns:
        list: Ma trận kết quả.
    """
    # Kiểm tra điều kiện nhân ma trận: cột A = hàng B
    try:
        m, n, p = len(A), len(A[0]), len(B[0])
    except:
        raise ValueError("Ma trận A hoặc B không hợp lệ")
    if n != len(B):
        raise ValueError("Số cột của ma trận A phải bằng số hàng của ma trận B")
    result = [[0.0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def vector_norm(v):
    """
    Tính chuẩn L2 của vector.

    Args:
        v: Vector đầu vào.

    Returns:
        float: Chuẩn L2 của vector.
    """
    return math.sqrt(sum(x**2 for x in v))

def dot_product(v1, v2):
    """
    Tính tích vô hướng của hai vector.

    Args:
        v1: Vector 1.
        v2: Vector 2.

    Returns:
        float: Tích vô hướng.
    """
    return sum(x * y for x, y in zip(v1, v2))

def subtract_vectors(v1, v2, scalar):
    """
    Trừ hai vector.

    Args:
        v1: Vector bị trừ.
        v2: Vector trừ.

    Returns:
        list: Vector kết quả.
    """
    return [x - (scalar * y) for x, y in zip(v1, v2)]

def vector_normalize(v):
    """
    Chuẩn hóa vector.

    Args:
        v: Vector đầu vào.

    Returns:
        list: Vector đã chuẩn hóa.
    """
    norm = vector_norm(v)
    if config.is_zero(norm): return v
    return [x / norm for x in v]

def get_col_slice(M, j, start_row):
    """
    Trả về vector v từ trong cột j trong ma trận M từ dòng start_row

    Args: 
        M: Ma trận gốc
        j: Cột thứ j trong ma trận
        start_row: Hàng bắt đầu 

    Returns:
        Vector v
    """
    return [M[i][j] for i in range(start_row, len(M))]

def find_orthogonal_u(existing_vectors, dim):
    """
    Tìm các vector trực chuẩn.

    Args:
        A: Ma trận đầu vào.
        V: Ma trận V.
        sigma_values: Các giá trị kỳ dị.

    Returns:
        list: Ma trận U.
    """
    # Thử lần lượt các vector đơn vị chuẩn: [1, 0, 0...], [0, 1, 0...]
    for i in range(dim):
        # Tạo vector đơn vị chuẩn e_i
        v = [0.0] * dim
        v[i] = 1.0
        
        # Quá trình Gram-Schmidt
        v_projected = v[:]
        for u in existing_vectors:
            # Tính hệ số chiếu: (v . u) / (u . u)
            # Vì u đã là vector đơn vị nên u.u = 1
            projection_scalar = dot_product(v, u)
            v_projected = subtract_vectors(v_projected, u, projection_scalar)
            
        # Kiểm tra độ dài vector còn lại
        mag = vector_norm(v_projected)
        if mag > 1e-10: 
            # Chuẩn hóa để trả về vector đơn vị
            return [x / mag for x in v_projected]
            
    return None

def identity_matrix(n):
    """
    Trả về ma trận đơn vị nxn

    Args: 
        n: Kích thước ma trận
    
    Returns:
        Ma trận đơn vị 
    """
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def copy_matrix(M):
    """
    Trả về bản deep_copy của ma trận ban đầu

    Args: 
        M: Ma trận ban đầu
    
    Returns: 
        Ma trận copy
    """
    return [row[:] for row in M]

def matrix_inverse(A):
    """
    Tính ma trận nghịch đảo của ma trận vuông A
    
    Args:
        A: Ma trận vuông cần tính nghịch đảo
    
    Returns:
        Ma trận nghịch đảo của A
    """
    n = len(A)
    if n == 0:
        return []
    if n != len(A[0]):
        raise ValueError("Ma trận phải là ma trận vuông")
    
    # Tạo ma trận mở rộng [A | I]
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    
    # Thực hiện phép biến đổi Gauss-Jordan
    for i in range(n):
        # Tìm pivot
        pivot = i
        for j in range(i + 1, n):
            if abs(aug[j][i]) > abs(aug[pivot][i]):
                pivot = j
        
        # Hoán đổi dòng
        aug[i], aug[pivot] = aug[pivot], aug[i]
        
        # Kiểm tra ma trận không khả nghịch
        if config.is_zero(aug[i][i]):
            raise ValueError("Ma trận không khả nghịch")
        
        # Chuẩn hóa dòng pivot
        pivot_val = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= pivot_val
        
        # Triệt tiêu các phần tử khác trong cột pivot
        for j in range(n):
            if i != j:
                factor = aug[j][i]
                for k in range(2 * n):
                    aug[j][k] -= factor * aug[i][k]
    
    # Trích xuất ma trận nghịch đảo
    inv_A = [row[n:] for row in aug]
    return inv_A

def orthogonal_matrix(eigenvectors):
    """
    Tạo ma trận trực giao từ các vector riêng
    
    Args:
        eigenvectors: Danh sách các vector riêng
    
    Returns:
        Ma trận trực giao Q
    """
    Q = []
    for v in eigenvectors:
        Q.append(vector_normalize(v))
    return Q 
    
def matrix_sub_lambda_I(A, lam):
    """
    Trừ ma trận cho lambda * I.

    Args:
        A: Ma trận đầu vào.
        lam: Giá trị lambda.

    Returns:
        list: Ma trận kết quả.
    """
    n = len(A)
    res = copy_matrix(A)
    for i in range(n):
        res[i][i] -= lam
    return res

def _mat_max_abs_diff(A, B):
    """
    Tìm sai số tuyệt đối lớn nhất giữa 2 ma trận.

    Args:
        A: Ma trận 1.
        B: Ma trận 2.

    Returns:
        float: Sai số.
    """
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    return float(np.max(np.abs(A_np - B_np)))

def _frobenius_error(A, B):
    """
    Tính sai số Frobenius.

    Args:
        A: Ma trận 1.
        B: Ma trận 2.

    Returns:
        float: Sai số Frobenius.
    """
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    return float(np.linalg.norm(A_np - B_np, 'fro'))

def _mat_multiply_np(A, B):
    """
    Nhân ma trận bằng numpy.

    Args:
        A: Ma trận trái.
        B: Ma trận phải.

    Returns:
        ndarray: Ma trận kết quả.
    """
    return np.dot(np.array(A, dtype=float), np.array(B, dtype=float)).tolist()

def _identity_np(n):
    """
    Tạo ma trận đơn vị bằng numpy.

    Args:
        n: Kích thước.

    Returns:
        ndarray: Ma trận đơn vị.
    """
    return np.eye(n).tolist()

def _sort_eigenvalues(vals):
    """
    Sắp xếp trị riêng giảm dần.

    Args:
        eigenvalues: Danh sách trị riêng.
        eigenvectors: Danh sách vector riêng tương ứng.

    Returns:
        tuple: Trị riêng và vector riêng đã sắp xếp.
    """
    return sorted([float(v) for v in vals], reverse=True)
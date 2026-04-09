import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

def matrix_transpose(A):
    """ Chuyển vị ma trận """
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def matrix_multiply(A, B):
    """ Nhân hai ma trận """
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
    """ Tính độ dài Euclid của vector """
    return math.sqrt(sum(x**2 for x in v))

def vector_normalize(v):
    """ Chuẩn hóa vector """
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

def diag(s):
    """
    Tạo ma trận đường chéo từ vector s
    
    Args:
        s: Vector chứa các phần tử trên đường chéo
    
    Returns:
        Ma trận đường chéo
    """
    n = len(s)
    return [[s[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
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
    m, n, p = len(A), len(A[0]), len(B[0])
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

def vec_norm(v): 
    """
    Tính độ dài của vector
    
    Args:
        v: Vector v
    
    Returns:
        Độ dài vector
    """
    return sum(x**2 for x in v) ** 0.5

# def vec_dot(v1, v2):
#     """
#     Tính tích vô hướng của 2 vector (dot product)

#     Args:
#         v1, v2: 2 vector

#     Returns: 
#         Tích vô hướng 2 vector
#     """
#     if (len(v1) != len(v2)):
#         raise ValueError("2 ma trận khác độ dài")
#     res = 0
#     for i in range(len(v1)):
#         res += v1[i] * v2[i]
#     return res 

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

# def vec_scalar_mul(v, s):
#     """
#     Nhân vector với scalar

#     Args: 
#         v: Vector
#         s: Scalar
    
#     Returns: 
#         Vector sau khi nhân
#     """
#     return [x * s for x in v]

# def vec_sub(v1, v2):
#     """
#     Trừ 2 vector

#     Args: 
#         v1, v2: 2 vector
    
#     Returns: 
#         Vector sau khi trừ
#     """
#     return [v1[i] - v2[i] for i in range(len(v1))]

# def transpose(M):
#     """
#     Chuyển vị ma trận

#     Args: 
#         M: Ma trận
    
#     Returns: 
#         Ma trận sau khi chuyển vị
#     """
#     return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
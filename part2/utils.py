import math

# --- CÁC HÀM TIỆN ÍCH CƠ BẢN ---

def matrix_transpose(A):
    """ Chuyển vị ma trận """
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def matrix_multiply(A, B):
    """ Nhân hai ma trận """
    # Kiểm tra điều kiện nhân ma trận: cột A = hàng B
    if len(A[0]) != len(B):
        raise ValueError("Số cột của ma trận A phải bằng số hàng của ma trận B")
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def vector_norm(v):
    """ Tính độ dài Euclid của vector """
    return math.sqrt(sum(x**2 for x in v))

def vector_normalize(v):
    """ Chuẩn hóa vector """
    norm = vector_norm(v)
    if norm < 1e-15: return v
    return [x / norm for x in v]
import utils as ut
from decomposition import householder_qr_v1

def matrix_multiply(A, B):
    """Nhân hai ma trận A (m x n) và B (n x p)"""
    m, n, p = len(A), len(A[0]), len(B[0])
    res = [[0.0] * p for _ in range(m)]
    for i in range(m):
        for k in range(n):
            for j in range(p):
                res[i][j] += A[i][k] * B[k][j]
    return res

def matrix_sub_lambda_I(A, lam):
    """Tính ma trận (A - λI)"""
    n = len(A)
    res = ut.copy_matrix(A)
    for i in range(n):
        res[i][i] -= lam
    return res

def get_eigenvalues_with_epsilon(A, max_iterations=100, epsilon=1e-12):
    Ak = ut.copy_matrix(A)
    n = len(Ak)
    
    for _ in range(max_iterations):
        Q, R = householder_qr_v1(Ak)
        Ak = matrix_multiply(R, Q)
        
        # Kiểm tra tổng các phần tử dưới đường chéo chính
        off_diag_sum = 0
        for i in range(1, n):
            for j in range(i):
                off_diag_sum += abs(Ak[i][j])
        
        # Nếu đã đủ "phẳng" (trở thành ma trận tam giác), thì dừng
        if off_diag_sum < epsilon:
            break
            
    return [Ak[i][i] for i in range(n)]

def back_substitution_solve_homo(R):
    """Giải hệ Rv = 0 với R là ma trận tam giác trên (tìm null space)"""
    n = len(R)
    v = [0.0] * n
    v[n-1] = 1.0  # Giả định tự do cho thành phần cuối
    
    for i in range(n - 2, -1, -1):
        sum_val = 0
        for j in range(i + 1, n):
            sum_val += R[i][j] * v[j]
        
        if abs(R[i][i]) > 1e-12:
            v[i] = -sum_val / R[i][i]
        else:
            v[i] = 0.0 # Trường hợp phụ thuộc tuyến tính
            
    # Chuẩn hóa vector riêng
    norm = ut.vec_norm(v)
    return [x / norm for x in v]

def find_eigenvectors(A, eigenvalues):
    """Tìm danh sách các vector riêng tương ứng với các giá trị riêng"""
    P = []
    for lam in eigenvalues:
        # 1. Tạo ma trận (A - λI)
        B = matrix_sub_lambda_I(A, lam)
        # 2. QR cho B để đưa về tam giác trên R
        _, R = householder_qr_v1(B)
        # 3. Giải Rv = 0
        v = back_substitution_solve_homo(R)
        P.append(v)
    
    # Chuyển danh sách vector hàng thành ma trận P (các vector riêng là cột)
    n = len(A)
    P_matrix = [[P[j][i] for j in range(n)] for i in range(n)]
    return P_matrix

def diagonalize(A):
    """
    Thực hiện chéo hóa ma trận A = PDP^-1
    Returns:
        P: Ma trận các vector riêng (cột)
        D: Ma trận đường chéo chứa các giá trị riêng
    """
    # 1. Tìm giá trị riêng
    evals = get_eigenvalues(A)
    
    # 2. Tạo ma trận đường chéo D
    n = len(A)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = evals[i]
        
    # 3. Tìm ma trận vector riêng P
    P = find_eigenvectors(A, evals)
    
    return P, D
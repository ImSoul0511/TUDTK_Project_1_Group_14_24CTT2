import math
import utils as ut
from decomposition import householder_qr_v1
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

# Dùng thuật toán Jacobi để tìm toàn bộ vector riêng 
def eigen_decomposition(M, iterations=100):
    """
    Sử dụng phương pháp xoay Jacobi để 'chéo hóa' ma trận đối xứng M.
    Đây là cách máy tính thay thế việc giải phương trình det(M - lambda*I) = 0.
    """
    n = len(M)
    # V ban đầu là ma trận đơn vị, sau này sẽ chứa các vector riêng (eigenvectors)
    V = ut.identity_matrix(n)
    # Tạo bản sao của ma trận M để tính toán (tránh làm hỏng dữ liệu gốc)
    A = ut.copy_matrix(M)

    for _ in range(iterations):
        # Tìm phần tử ngoài đường chéo lớn nhất
        max_val = 0
        p, q = 0, 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j

        # Nếu mọi phần tử ngoài đường chéo đã gần bằng 0, coi như ma trận đã chéo hóa xong
        if max_val < config.EPSILON: break

        # Tính góc xoay Jacobi (theta) để triệt tiêu phần tử A[p][q]
        theta = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
        c = math.cos(theta)
        s = math.sin(theta)

        # Xoay ma trận A và ma trận vector riêng V
        for i in range(n):
            # Cập nhật V
            temp_v_p = V[i][p]
            V[i][p] = c * temp_v_p - s * V[i][q]
            V[i][q] = s * temp_v_p + c * V[i][q]
            
            # Cập nhật A (chỉ cần các hàng/cột p, q)
            if i != p and i != q:
                temp_a_ip = A[i][p]
                A[i][p] = A[p][i] = c * temp_a_ip - s * A[i][q]
                A[i][q] = A[q][i] = s * temp_a_ip + c * A[i][q]

        # Cập nhật các phần tử tại các đỉnh của hình chữ nhật xoay (p,p), (q,q), (p,q)
        p_val = A[p][p]
        q_val = A[q][q]
        pq_val = A[p][q]
        A[p][p] = c*c*p_val + s*s*q_val - 2*s*c*pq_val
        A[q][q] = s*s*p_val + c*c*q_val + 2*s*c*pq_val
        A[p][q] = A[q][p] = 0

    # Các giá trị riêng (eigenvalues) nằm trên đường chéo chính của A sau khi xoay
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, V

def matrix_sub_lambda_I(A, lam):
    """Tính ma trận (A - λI)"""
    n = len(A)
    res = ut.copy_matrix(A)
    for i in range(n):
        res[i][i] -= lam
    return res

def back_substitution_solve_homo(R):
    """Giải hệ Rv = 0 với R là ma trận tam giác trên (tìm null space)"""
    n = len(R)
    v = [0.0] * n
    v[n-1] = 1.0  # Giả định tự do cho thành phần cuối
    
    for i in range(n - 2, -1, -1):
        sum_val = 0
        for j in range(i + 1, n):
            sum_val += R[i][j] * v[j]
        
        if abs(R[i][i]) > config.EPSILON:
            v[i] = -sum_val / R[i][i]
        else:
            v[i] = 0.0 # Trường hợp phụ thuộc tuyến tính
            
    # Chuẩn hóa vector riêng
    norm = ut.vector_norm(v)
    return [x / norm for x in v]

def eigen_decomposition_with_qr(A, max_iterations=100):
    Ak = ut.copy_matrix(A)
    n = len(Ak)
    
    for _ in range(max_iterations):
        Q, R = householder_qr_v1(Ak)
        Ak = ut.matrix_multiply(R, Q)
        
        # Kiểm tra tổng các phần tử dưới đường chéo chính
        off_diag_sum = 0
        for i in range(1, n):
            for j in range(i):
                off_diag_sum += abs(Ak[i][j])
        
        # Nếu đã đủ "phẳng" (trở thành ma trận tam giác), thì dừng
        if off_diag_sum < config.EPSILON:
            break
    
    # Tìm vector riêng
    eigenvalues = [Ak[i][i] for i in range(n)]
    P = []
    for lam in eigenvalues:
        B = matrix_sub_lambda_I(A, lam)
        _, R = householder_qr_v1(B)
        v = back_substitution_solve_homo(R)
        P.append(v)
    
    P_matrix = [[P[j][i] for j in range(n)] for i in range(n)]
    return eigenvalues, P_matrix

def diagonalize(A):
    """
    Thực hiện chéo hóa ma trận A = PDP^-1
    Returns:
        P: Ma trận các vector riêng (cột)
        D: Ma trận đường chéo chứa các giá trị riêng
    """
    # 1. Tìm giá trị riêng
    eigenvalues, P = eigen_decomposition_with_qr(A) 
    
    # 2. Tạo ma trận đường chéo D
    n = len(A)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = eigenvalues[i]
        
    return P, D

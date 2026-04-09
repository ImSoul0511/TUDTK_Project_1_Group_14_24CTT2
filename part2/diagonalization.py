import math
import utils as ut
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
        if config.is_zero(max_val): break

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

def get_null_space(A):
    """
    Tìm cơ sở không gian rỗng của ma trận A (giải hệ Ax = 0).  
    """
    # Tạo bản sao để không làm hỏng ma trận gốc
    M = ut.copy_matrix(A)
    row = len(M)
    col = len(M[0])

    pivot_cols = []   
    current_row = 0

    # 1. Khử Gauss để đưa về dạng bậc thang (Row Echelon Form)
    for k in range(col):
        if current_row >= row:
            break

        # Tìm pivot
        p = current_row
        for i in range(current_row + 1, row):
            if abs(M[i][k]) > abs(M[p][k]):
                p = i

        if config.is_zero(M[p][k]): 
            continue
        
        if p != current_row:
            M[current_row], M[p] = M[p], M[current_row]
            
        pivot_cols.append(k)
        
        for i in range(current_row + 1, row):
            l_ik = M[i][k] / M[current_row][k]
            M[i][k] = 0
            for j in range(k + 1, col):
                M[i][j] -= l_ik * M[current_row][j]
        current_row += 1

    rank = len(pivot_cols)

    # 2. Tìm cơ sở không gian nghiệm (null_basis)
    free_cols = [j for j in range(col) if j not in pivot_cols]
    null_basis = []
    
    for f in free_cols:
        v = [0.0] * col
        v[f] = 1.0  # Bật ẩn tự do = 1
        
        # Thế ngược để tìm các ẩn chốt
        for i in range(rank - 1, -1, -1):
            p_col = pivot_cols[i]
            s_val = sum(M[i][j] * v[j] for j in range(p_col + 1, col))
            v[p_col] = -s_val / M[i][p_col]
            
        norm = ut.vector_norm(v)
        if norm > config.EPSILON:
            v = [x / norm for x in v]
            
        null_basis.append(v)

    return null_basis

def eigen_decomposition_with_qr(A, max_iterations=500):
    from decomposition import householder_qr_v1
    Ak = ut.copy_matrix(A)
    n = len(Ak)
    
    for _ in range(max_iterations):
        Q, R = householder_qr_v1(Ak)
        Ak = ut.matrix_multiply(R, Q)
        
        # Kiểm tra tổng các phần tử dưới đường chéo chính
        off_diag_sum = sum(abs(Ak[i][j]) for i in range(1, n) for j in range(i))
        
        # Nếu đã đủ "phẳng" (trở thành ma trận tam giác), thì dừng
        if config.is_zero(off_diag_sum):
            break
    
    # Tìm vector riêng
    eigenvalues = [Ak[i][i] for i in range(n)]

    # Gộp các trị riêng trùng lặp (trị riêng bội)
    unique_eigenvalues = []
    for lam in eigenvalues:
        if not any(config.is_zero(lam - u) for u in unique_eigenvalues):
            unique_eigenvalues.append(lam)
    P_cols = []
    final_eigenvalues = []
    for lam in unique_eigenvalues:
        B = matrix_sub_lambda_I(A, lam)
        
        # Tìm Không gian rỗng bằng Khử Gauss-Jordan (tốt hơn back_substitution)
        basis = get_null_space(B)
        
        for v in basis:
            P_cols.append(v)
            final_eigenvalues.append(lam) # Ánh xạ trị riêng tương ứng với vector
    
    return final_eigenvalues, P_cols

def diagonalize_with_qr(A):
    """
    Thực hiện chéo hóa ma trận A = PDP^-1 bằng thuật toán lặp QR.
    Returns:
        P: Ma trận các vector riêng (cột)
        D: Ma trận đường chéo chứa các giá trị riêng
        P_inv: Ma trận nghịch đảo của P
    Raises:
        ValueError: Nếu A không phải ma trận vuông.
        ValueError: Nếu A không thể chéo hóa (ma trận thiếu hụt - P suy biến).
    """
    # Kiểm tra ma trận vuông
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Ma trận A phải là ma trận vuông để thực hiện chéo hóa.")

    # 1. Tìm giá trị riêng và vector riêng
    eigenvalues, P_cols = eigen_decomposition_with_qr(A)

    if len(P_cols) < n:
        raise ValueError("Ma trận A không thể chéo hóa (thiếu hụt vector riêng - defective matrix).")
    
    P = [[P_cols[j][i] for j in range(n)] for i in range(n)]
    
    # 2. Tạo ma trận đường chéo D
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = eigenvalues[i]

    # Kiểm tra P có khả nghịch không (dấu hiệu ma trận có thể chéo hóa)
    try:
        P_inv = ut.matrix_inverse(P)
    except ValueError:
        raise ValueError("Ma trận A không thể chéo hóa: các vector riêng không độc lập tuyến tính (ma trận thiếu hụt).")

    return P, D, P_inv

def diagonalize(A):
    """
    Thực hiện chéo hóa ma trận A = PDP^-1 bằng thuật toán Jacobi.
    Returns:
        P: Ma trận các vector riêng (cột)
        D: Ma trận đường chéo chứa các giá trị riêng
        P_inv: Ma trận nghịch đảo của P
    Raises:
        ValueError: Nếu A không phải ma trận vuông.
        ValueError: Nếu A không đối xứng (Jacobi chỉ hoạt động với ma trận đối xứng).
        ValueError: Nếu A không thể chéo hóa (ma trận thiếu hụt - P suy biến).
    """
    # Kiểm tra ma trận vuông
    n = len(A)
    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("Ma trận A phải là ma trận vuông để thực hiện chéo hóa.")

    # Kiểm tra ma trận đối xứng (điều kiện để Jacobi hoạt động đúng)
    for i in range(n):
        for j in range(i + 1, n):
            if not config.is_zero(A[i][j] - A[j][i]):
                raise ValueError(f"Thuật toán Jacobi chỉ áp dụng cho ma trận đối xứng. A[{i}][{j}]={A[i][j]} ≠ A[{j}][{i}]={A[j][i]}.")

    # 1. Tìm giá trị riêng và vector riêng bằng phương pháp Jacobi
    eigenvalues, P = eigen_decomposition(A)

    # 2. Tạo ma trận đường chéo D
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = eigenvalues[i]

    # Kiểm tra P có khả nghịch không (dấu hiệu ma trận có thể chéo hóa)
    try:
        P_inv = ut.matrix_inverse(P)
    except ValueError:
        raise ValueError("Ma trận A không thể chéo hóa: các vector riêng không độc lập tuyến tính (ma trận thiếu hụt).")

    return P, D, P_inv

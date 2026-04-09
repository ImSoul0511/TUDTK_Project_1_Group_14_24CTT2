import math
import utils as ut
from diagonalization import eigen_decomposition
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

def svd(A):
    """
    Phân rã giá trị đơn lẻ (Singular Value Decomposition - SVD).
    Biến đổi ma trận A (m x n) thành tích của ba ma trận: U * Sigma * Vt
    
    Thuật toán:
    1. Tính ma trận đối xứng ATA = A^T * A.
    2. Tìm các giá trị riêng (lambdas) và vector riêng (V) của ATA bằng phương pháp Jacobi.
    3. Tính các giá trị kỳ dị (sigmas): σ_i = √λ_i.
    4. Tính ma trận U dựa trên công thức: u_i = (1/σ_i) * A * v_i.
    
    Công thức chính:
       - A = U * Σ * V^T
       - U: Ma trận trực giao chứa các vector kỳ dị trái (m x m).
       - Σ: Ma trận đường chéo chứa các giá trị kỳ dị giảm dần.
       - V^T: Chuyển vị của ma trận trực giao chứa các vector kỳ dị phải (n x n).

    Args:
        A: Ma trận đầu vào kích thước m x n (list of lists).

    Returns:
        U: Ma trận trực giao (m x k).
        sigmas: Danh sách các giá trị kỳ dị σ sắp xếp giảm dần.
        Vt: Ma trận V đã được chuyển vị (k x n).
    """
    # Bước 1: Tính ATA để tìm các giá trị riêng cho V
    # Phân rã ma trận ATA cho ta các Vector riêng (Cột của V) và các Trị riêng (Lambda)
    At = ut.matrix_transpose(A)
    ATA = ut.matrix_multiply(At, A)
    lambdas_V, V = eigen_decomposition(ATA)

    # Bước 2: Tính các giá trị kỳ dị (sigma = căn bậc hai của lambda)
    # Lọc bỏ các giá trị âm nhỏ do sai số máy tính và sắp xếp giảm dần
    sigmas = [math.sqrt(max(0, l)) for l in lambdas_V]
    
    # Sắp xếp thứ tự giảm dần cho sigma (kéo theo V và U)
    indices = sorted(range(len(sigmas)), key=lambda i: sigmas[i], reverse=True)
    sigmas = [sigmas[i] for i in indices]

    # Bước 3: Tìm ma trận V (Đã làm ở Bước 1 & 2)
    # V lúc này là ma trận mà mỗi cột là một vector riêng của ATA
    V = [[V[row][i] for i in indices] for row in range(len(V))]

    # Bước 4: Tìm ma trận U (Vector riêng của AAT)
    # Sử dụng công thức liên hệ: u_i = (1 / sigma_i) * A * v_i
    U = []
    for i in range(len(sigmas)):
        if sigmas[i] > config.EPSILON: # Chỉ tính nếu giá trị kỳ dị đủ lớn (tránh nhiễu)
            v_i = [V[row][i] for row in range(len(V))]
            u_i = [sum(A[r][c] * v_i[c] for c in range(len(v_i))) for r in range(len(A))]
            U.append(ut.vector_normalize(u_i))
        else:
            # Nếu sigma = 0, cần tìm vector trực giao với các u trước đó
            U.append([0.0] * len(A)) # Đơn giản hóa

    # Bước 5: Tạo ma trận Sigma (đường chéo)
    # (Trả về danh sách sigmas để tiết kiệm bộ nhớ, dễ dàng tạo ma trận sau)
    
    return ut.matrix_transpose(U), sigmas, ut.matrix_transpose(V)

# --- TÁI TẠO MA TRẬN TỪ KẾT QUẢ PHÂN RÃ ---
def rebuild_matrix(U_mtx, sigmas, Vt_mtx, m, n):
    """ Tái tạo ma trận A từ kết quả phân rã SVD """
    # k là số lượng trị kỳ dị thực tế tìm được (ví dụ k=2)
    k = len(sigmas)
    
    # Tạo Sigma là ma trận vuông (k x k)
    Sigma_k = [[0.0 for _ in range(k)] for _ in range(k)]
    for i in range(k):
        Sigma_k[i][i] = sigmas[i]
    
    # Phép nhân: (m x k) * (k x k) * (k x n) = (m x n)
    U_Sigma = ut.matrix_multiply(U_mtx, Sigma_k)
    A_reconstructed = ut.matrix_multiply(U_Sigma, Vt_mtx)
    return A_reconstructed

def householder_qr_v1(A):
    """
    Phân rã QR bằng phương pháp phản xạ Householder (Householder QR Decomposition).
    
    Thuật toán: 
        Tại mỗi bước j, xây dựng ma trận phản xạ Householder H_j để triệt tiêu
        các phần tử bên dưới đường chéo trong cột j của ma trận R.
        
    Công thức chính (từ lec16):
        1. Trích cột:       x = R(j:m, j)
        2. Chuẩn:           normx = ||x||₂
        3. Chọn dấu:        s = -sign(x₁)     (tránh triệt tiêu catastrophic)
        4. Thành phần u₁:   u₁ = x₁ - s * normx
        5. Vector phản xạ:  w = x / u₁,  w[0] = 1
        6. Hệ số tau:       τ = -s * u₁ / normx
        7. Ma trận phản xạ: H = I - τ * w * wᵀ
        
    Cập nhật:
        - R(j:m, j:n)  ←  R(j:m, j:n) - (τ * w) * (wᵀ * R(j:m, j:n))
        - Q(:, j:m)    ←  Q(:, j:m)   - (Q(:, j:m) * w) * (τ * wᵀ)
    
    Args:
        A: Ma trận đầu vào kích thước m x n (list of lists)
    
    Returns:
        Q: Ma trận trực giao kích thước m x m (Q^T * Q = I)
        R: Ma trận tam giác trên kích thước m x n
    """
    m = len(A)
    n = len(A[0])
    Q = ut.identity_matrix(m)
    R = ut.copy_matrix(A)
    
    for j in range(min(m - 1, n)):
        # Bước 1: Trích vector cột x = R(j:m, j)
        slice_col = ut.get_col_slice(R, j, j) 
        
        # Bước 2: Tính chuẩn ||x||₂
        normx = ut.vector_norm(slice_col)

        if config.is_zero(normx):
            continue 

        # Bước 3: Chọn dấu s = -sign(x₁), tránh triệt tiêu catastrophic
        s = -1 if R[j][j] >= 0 else 1 
        
        # Bước 4: Tính u₁ = x₁ - s * normx
        u1 = R[j][j] - s * normx 

        if config.is_zero(u1):   
            continue 
            
        # Bước 5: Xây dựng vector phản xạ w = x / u₁, chuẩn hóa w[0] = 1
        w = [x / u1 for x in slice_col] 
        w[0] = 1
        
        # Bước 6: Tính hệ số tau: τ = -s * u₁ / normx
        tau = -s * u1 / normx 

        # Bước 7a: Cập nhật R(j:m, j:n) = R(j:m, j:n) - (τ * w) * (wᵀ * R(j:m, j:n))
        # Tính wᵀ * R (chỉ các cột từ j trở đi)
        w_T_R = []
        for col in range(j, n):
            dot_val = 0
            for row in range(j, m):
                dot_val += w[row - j] * R[row][col]
            w_T_R.append(dot_val)
        
        # Cập nhật trực tiếp R
        for row in range(j, m):
            for idx, col in enumerate(range(j, n)):
                R[row][col] -= tau * w[row - j] * w_T_R[idx]
        
        # Bước 7b: Cập nhật Q(:, j:m) = Q(:, j:m) - (Q(:, j:m) * w) * (τ * wᵀ)
        # Tính Q(:, j:m) * w
        Q_w = []
        for row in range(m):
            dot_val = 0
            for col in range(len(w)):
                dot_val += Q[row][j + col] * w[col]
            Q_w.append(dot_val)
        
        # Cập nhật Q
        for row in range(m):
            for col in range(len(w)):
                Q[row][j + col] -= Q_w[row] * (w[col] * tau)
    
    return Q, R

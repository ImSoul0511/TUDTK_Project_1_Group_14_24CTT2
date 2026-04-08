import math
from utils import matrix_transpose, matrix_multiply, vector_normalize
from diagonalization import eigen_decomposition

# --- THUẬT TOÁN SVD ---

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
    At = matrix_transpose(A)
    ATA = matrix_multiply(At, A)
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
        if sigmas[i] > 1e-10: # Chỉ tính nếu giá trị kỳ dị đủ lớn (tránh nhiễu)
            v_i = [V[row][i] for row in range(len(V))]
            u_i = [sum(A[r][c] * v_i[c] for c in range(len(v_i))) for r in range(len(A))]
            U.append(vector_normalize(u_i))
        else:
            # Nếu sigma = 0, cần tìm vector trực giao với các u trước đó
            U.append([0.0] * len(A)) # Đơn giản hóa

    # Bước 5: Tạo ma trận Sigma (đường chéo)
    # (Trả về danh sách sigmas để tiết kiệm bộ nhớ, dễ dàng tạo ma trận sau)
    
    return matrix_transpose(U), sigmas, matrix_transpose(V)

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
    U_Sigma = matrix_multiply(U_mtx, Sigma_k)
    A_reconstructed = matrix_multiply(U_Sigma, Vt_mtx)
    return A_reconstructed



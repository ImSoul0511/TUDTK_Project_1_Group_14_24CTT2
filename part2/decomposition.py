import math
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cfg
import part2.utils as ut
from config import AutoTestReporter
from part2.diagonalization import eigen_calculation_with_jacobi
from part2.test_case import SVD_TEST_CASES
from part2.verification import verify_svd_numpy

def svd(A):
    """
    Phân rã giá trị đơn lẻ (Singular Value Decomposition - SVD).
    Biến đổi ma trận A (m x n) thành tích của ba ma trận: U * Sigma * Vt
    
    Thuật toán:
    1. Tính ma trận đối xứng ATA = A^T * A.
    2. Tìm các giá trị riêng (lambdas) và vector riêng (V) của ATA bằng phương pháp Jacobi.
    3. Tính các giá trị kỳ dị (sigmas): sigma_i = √lambda_i.
    4. Tính ma trận U dựa trên công thức: u_i = (1/sigma_i) * A * v_i.
    
    Công thức chính:
       - A = U * Σ * V^T
       - U: Ma trận trực giao chứa các vector kỳ dị trái (m x m).
       - Σ: Ma trận đường chéo chứa các giá trị kỳ dị giảm dần.
       - V^T: Chuyển vị của ma trận trực giao chứa các vector kỳ dị phải (n x n).

    Args:
        A: Ma trận đầu vào kích thước m x n (list of lists).

    Returns:
        U: Ma trận trực giao (m x k).
        sigmas: Danh sách các giá trị kỳ dị sigma sắp xếp giảm dần.
        Vt: Ma trận V đã được chuyển vị (k x n).
    """
    # Bước 1: Tính ATA để tìm các giá trị riêng cho V
    # Phân rã ma trận ATA cho ta các Vector riêng (Cột của V) và các Trị riêng (Lambda)
    At = ut.matrix_transpose(A)
    ATA = ut.matrix_multiply(At, A)
    lambdas_V, V = eigen_calculation_with_jacobi(ATA)

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
    for i in range(min(len(A), len(sigmas))):
        if not cfg.is_zero(sigmas[i]): # Chỉ tính nếu giá trị kỳ dị đủ lớn (tránh nhiễu)
            v_i = [V[row][i] for row in range(len(V))]
            u_i = [sum(A[r][c] * v_i[c] for c in range(len(v_i))) for r in range(len(A))]
            U.append(ut.vector_normalize(u_i))
        else:
            # Nếu sigma = 0, cần tìm vector trực giao với các u trước đó
            new_u = ut.find_orthogonal_u(U, len(A))
            U.append(new_u)

    # Nếu số chiều của U nhỏ hơn số hàng của A, cần tìm thêm vector trực giao
    while len(U) < len(A):
        new_u = ut.find_orthogonal_u(U, len(A))
        U.append(new_u)

    # Bước 5: Tạo ma trận Sigma (kích thước m x n)
    m, n = len(A), len(A[0])
    Sigma = [[0.0] * n for _ in range(m)]
    for i in range(min(m, n)):
        Sigma[i][i] = sigmas[i]
    
    return ut.matrix_transpose(U), Sigma, ut.matrix_transpose(V)

def householder_qr_v1(A):
    """
    Phân rã QR bằng phương pháp phản xạ Householder (Householder QR Decomposition).
    
    Thuật toán: 
        Tại mỗi bước j, xây dựng ma trận phản xạ Householder H_j để triệt tiêu
        các phần tử bên dưới đường chéo trong cột j của ma trận R.
        
    Công thức chính:
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
    if m == 0:
        return [], []
    n = len(A[0])
    Q = ut.identity_matrix(m)
    R = ut.copy_matrix(A)
    
    for j in range(min(m - 1, n)):
        # Bước 1: Trích vector cột x = R(j:m, j)
        slice_col = ut.get_col_slice(R, j, j) 
        
        # Bước 2: Tính chuẩn ||x||₂
        normx = ut.vector_norm(slice_col)

        if cfg.is_zero(normx):
            continue 

        # Bước 3: Chọn dấu s = -sign(x₁), tránh triệt tiêu catastrophic
        s = -1 if R[j][j] >= 0 else 1 
        
        # Bước 4: Tính u₁ = x₁ - s * normx
        u1 = R[j][j] - s * normx 

        if cfg.is_zero(u1):   
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

def run_svd_tests(test_cases: list[dict]):
    """
    Chạy kiểm thử cho thuật toán SVD.

    Args:
        test_cases: Danh sách ca kiểm thử.

    Returns:
        None
    """
    AutoTestReporter.print_header("KIỂM CHỨNG THUẬT TOÁN: SVD (Singular Value Decomposition) — Tự cài đặt vs NumPy")

    col_name    = 38
    col_rebuild = 16
    col_orth_u  = 16
    col_orth_v  = 16
    col_status  = 8

    header = (
        f"{'Test Case':<{col_name}}"
        f"{'Err Tái tạo':>{col_rebuild}}"
        f"{'Err Orth(U)':>{col_orth_u}}"
        f"{'Err Orth(Vt)':>{col_orth_v}}"
        f"{'Kết quả':>{col_status}}"
    )
    print(header)

    passed_count = 0
    total_count  = len(test_cases)

    for case in test_cases:
        name = case["Nội dung"]
        A    = case["Ma trận A"]

        try:
            ok, r_err, u_err, v_err, sigmas = verify_svd_numpy(A)

            # Nếu có expected_sigmas thì kiểm tra thêm
            if "expected_sigmas" in case:
                expected = sorted(case["expected_sigmas"], reverse=True)
                got      = sorted(sigmas, reverse=True)

                # So sánh từng giá trị
                sigma_ok = len(expected) == len(got) and all(
                    abs(e - g) < 1e-4
                    for e, g in zip(expected, got)
                )
                sigma_err = max(
                    abs(e - g)
                    for e, g in zip(
                        sorted(expected, reverse=True),
                        sorted(got,      reverse=True)
                    )
                ) if len(expected) == len(got) else float('inf')

                ok = ok and sigma_ok
                sigma_note = f"  sigma-err={sigma_err:.2e}"
            elif "expected_rank" in case:
                expected_rank = case["expected_rank"]
                actual_rank   = sum(1 for s in sigmas if s > 1e-6)
                ok = ok and (actual_rank == expected_rank)
                sigma_note = f"  rank={actual_rank}(exp={expected_rank})"
            else:
                sigma_note = ""

            status = "[OK]  " if ok else "[FAIL]"
            if ok:
                passed_count += 1

            name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
            print(
                f"{name_str:<{col_name}}"
                f"{r_err:>{col_rebuild}.2e}"
                f"{u_err:>{col_orth_u}.2e}"
                f"{v_err:>{col_orth_v}.2e}"
                f"{status:>{col_status}}"
                f"{sigma_note}"
            )

        except Exception as ex:
            status = "[FAIL]"
            name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
            print(
                f"{name_str:<{col_name}}"
                f"{'N/A':>{col_rebuild}}"
                f"{'N/A':>{col_orth_u}}"
                f"{'N/A':>{col_orth_v}}"
                f"{status:>{col_status}}"
                f"  -> Lỗi: {ex}"
            )

    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    run_svd_tests(SVD_TEST_CASES)

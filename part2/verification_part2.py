import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import utils as ut
import config as cfg 
from test_case_part2 import SVD_TEST_CASES 

def verify_svd_numpy(A):
    """
    Kiểm chứng kết quả SVD tự cài đặt bằng 3 điều kiện toán học:
        1. Tái tạo : A ≈ U * Σ * Vt
        2. Trực giao U : U^T * U ≈ I
        3. Trực giao Vt : Vt * Vt^T ≈ I

    Args:
        A: Ma trận đầu vào (list of lists, m × n)

    Returns:
        ok          : bool  – True nếu cả 3 điều kiện đều thỏa
        rebuild_err : float – Sai số Frobenius của bước tái tạo
        u_orth_err  : float – Sai số Frobenius kiểm tra trực giao U
        v_orth_err  : float – Sai số Frobenius kiểm tra trực giao Vt
        sigmas      : list  – Danh sách các giá trị kỳ dị
    """
    from part2.decomposition import svd
    m = len(A)
    n = len(A[0])

    # Gọi hàm tự cài
    U, Sigma, Vt = svd(A)

    A_np  = np.array(A,     dtype=float)
    U_np  = np.array(U,     dtype=float)   # shape (m, m)
    S_np  = np.array(Sigma, dtype=float)   # shape (m, n)
    Vt_np = np.array(Vt,    dtype=float)   # shape (n, n)

    # --- 1. Tái tạo: A ≈ U * Σ * Vt ---
    A_rebuild   = U_np @ S_np @ Vt_np
    rebuild_err = float(np.linalg.norm(A_np - A_rebuild, 'fro'))

    # --- 2. Trực giao U: U^T * U = I_m ---
    UTU         = U_np.T @ U_np
    u_orth_err  = float(np.linalg.norm(UTU - np.eye(m), 'fro'))

    # --- 3. Trực giao Vt: Vt * Vt^T = I_n ---
    VtVtT       = Vt_np @ Vt_np.T
    v_orth_err  = float(np.linalg.norm(VtVtT - np.eye(n), 'fro'))

    # Các giá trị kỳ dị (lấy từ đường chéo Sigma)
    k      = min(m, n)
    sigmas = [S_np[i][i] for i in range(k)]

    TOL = 1e-6
    ok  = (rebuild_err < TOL) and (u_orth_err < TOL) and (v_orth_err < TOL)

    return ok, rebuild_err, u_orth_err, v_orth_err, sigmas


def verify_diagonalize_numpy(A):
    """
    Kiểm chứng kết quả chéo hóa QR tự cài đặt bằng 2 điều kiện:
        1. Tái tạo : A ≈ P * D * P_inv
        2. Trị riêng : D[i][i] khớp với np.linalg.eig (theo tập hợp)

    Args:
        A: Ma trận vuông (list of lists, n × n)

    Returns:
        ok           : bool  – True nếu cả 2 điều kiện đều thỏa
        rebuild_err  : float – Sai số Frobenius của bước tái tạo A
        max_eig_err  : float – Sai số tuyệt đối lớn nhất của trị riêng với numpy
        eigenvalues  : list  – Danh sách trị riêng (thực) từ đường chéo D
    """
    from part2.diagonalization import diagonalize
    n = len(A)
    A_np = np.array(A, dtype=float)

    # Gọi hàm tự cài
    P, D, P_inv = diagonalize(A)

    P_np    = np.array(P,     dtype=float)
    D_np    = np.array(D,     dtype=float)
    Pinv_np = np.array(P_inv, dtype=float)

    # --- 1. Tái tạo: A ≈ P * D * P_inv ---
    A_rebuild   = P_np @ D_np @ Pinv_np
    rebuild_err = float(np.linalg.norm(A_np - A_rebuild, 'fro'))

    # --- 2. So sánh trị riêng với numpy (theo tập hợp, sắp xếp giảm dần) ---
    eigenvalues_custom = ut._sort_eigenvalues([D_np[i][i] for i in range(n)])
    eig_np_raw         = np.linalg.eigvals(A_np)
    # Chỉ lấy phần thực cho ma trận hội tụ về trị thực
    eigenvalues_np = ut._sort_eigenvalues(eig_np_raw.real)

    if len(eigenvalues_custom) == len(eigenvalues_np):
        max_eig_err = max(
            abs(c - e)
            for c, e in zip(eigenvalues_custom, eigenvalues_np)
        )
    else:
        max_eig_err = float('inf')

    TOL = 1e-6
    ok  = (rebuild_err < TOL) and (max_eig_err < TOL)

    return ok, rebuild_err, max_eig_err, eigenvalues_custom

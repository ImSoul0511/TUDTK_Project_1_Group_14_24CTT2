import numpy as np
import sys
import os

# Đảm bảo import được từ gốc project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
from config import AutoTestReporter
from part2.decomposition import svd, householder_qr_v1
from part2.diagonalization import diagonalize_with_qr


# ============================================================================
# HÀM TIỆN ÍCH NỘI BỘ
# ============================================================================

def _mat_max_abs_diff(A, B):
    """Tính sai số tuyệt đối lớn nhất giữa 2 ma trận (list of lists)."""
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    return float(np.max(np.abs(A_np - B_np)))

def _frobenius_error(A, B):
    """Tính chuẩn Frobenius của hiệu |A - B|_F."""
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    return float(np.linalg.norm(A_np - B_np, 'fro'))

def _mat_multiply_np(A, B):
    """Nhân 2 ma trận (list of lists) → list of lists dùng numpy."""
    return np.dot(np.array(A, dtype=float), np.array(B, dtype=float)).tolist()

def _identity_np(n):
    """Trả về ma trận đơn vị n×n dạng list of lists."""
    return np.eye(n).tolist()

def _sort_eigenvalues(vals):
    """Sắp xếp danh sách trị riêng thực theo thứ tự giảm dần để so sánh."""
    return sorted([float(v) for v in vals], reverse=True)


# ============================================================================
# 1. VERIFY SVD  (svd)
# ============================================================================

def verify_svd_custom(A):
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

    # --- 2. Trực giao U: U^T * U ≈ I_m ---
    UTU         = U_np.T @ U_np
    u_orth_err  = float(np.linalg.norm(UTU - np.eye(m), 'fro'))

    # --- 3. Trực giao Vt: Vt * Vt^T ≈ I_n ---
    VtVtT       = Vt_np @ Vt_np.T
    v_orth_err  = float(np.linalg.norm(VtVtT - np.eye(n), 'fro'))

    # Các giá trị kỳ dị (lấy từ đường chéo Sigma)
    k      = min(m, n)
    sigmas = [S_np[i][i] for i in range(k)]

    TOL = 1e-6
    ok  = (rebuild_err < TOL) and (u_orth_err < TOL) and (v_orth_err < TOL)

    return ok, rebuild_err, u_orth_err, v_orth_err, sigmas


def run_svd_tests(test_cases: list[dict]):
    """
    Chạy toàn bộ test cases cho thuật toán SVD tự cài đặt.

    Với mỗi test case sẽ in:
      - Tên test case
      - Trạng thái PASS / FAIL
      - Sai số tái tạo, sai số trực giao U, sai số trực giao Vt
      - (Nếu có expected_sigmas) Sai số so với numpy
    """
    SEP = "=" * 95
    HDR = "-" * 95

    print(f"\n{SEP}")
    print(f"  KIỂM CHỨNG THUẬT TOÁN: SVD (Singular Value Decomposition) — Tự cài đặt vs NumPy")
    print(SEP)

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
    print(HDR)

    passed_count = 0
    total_count  = len(test_cases)

    for case in test_cases:
        name = case["Nội dung"]
        A    = case["Ma trận A"]

        try:
            ok, r_err, u_err, v_err, sigmas = verify_svd_custom(A)

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
                sigma_note = f"  σ-err={sigma_err:.2e}"
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

    print(HDR)
    _print_summary_table(passed_count, total_count)


# ============================================================================
# 2. VERIFY DIAGONALIZATION (diagonalize_with_qr)
# ============================================================================

def verify_diagonalize_qr_custom(A):
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
    n = len(A)
    A_np = np.array(A, dtype=float)

    # Gọi hàm tự cài
    P, D, P_inv = diagonalize_with_qr(A)

    P_np    = np.array(P,     dtype=float)
    D_np    = np.array(D,     dtype=float)
    Pinv_np = np.array(P_inv, dtype=float)

    # --- 1. Tái tạo: A ≈ P * D * P_inv ---
    A_rebuild   = P_np @ D_np @ Pinv_np
    rebuild_err = float(np.linalg.norm(A_np - A_rebuild, 'fro'))

    # --- 2. So sánh trị riêng với numpy (theo tập hợp, sắp xếp giảm dần) ---
    eigenvalues_custom = _sort_eigenvalues([D_np[i][i] for i in range(n)])
    eig_np_raw         = np.linalg.eigvals(A_np)
    # Chỉ lấy phần thực cho ma trận hội tụ về trị thực
    eigenvalues_np = _sort_eigenvalues(eig_np_raw.real)

    if len(eigenvalues_custom) == len(eigenvalues_np):
        max_eig_err = max(
            abs(c - e)
            for c, e in zip(eigenvalues_custom, eigenvalues_np)
        )
    else:
        max_eig_err = float('inf')

    TOL = 1e-5
    ok  = (rebuild_err < TOL) and (max_eig_err < TOL)

    return ok, rebuild_err, max_eig_err, eigenvalues_custom


def run_diagonalize_qr_tests(test_cases: list[dict]):
    """
    Chạy toàn bộ test cases cho thuật toán Chéo hóa lặp QR tự cài đặt.

    Với mỗi test case sẽ in:
      - Tên test case
      - Trạng thái PASS / FAIL
      - Sai số tái tạo A = P*D*P_inv
      - Sai số trị riêng so với numpy (max absolute error)
    """
    SEP = "=" * 90
    HDR = "-" * 90

    print(f"\n{SEP}")
    print(f"  KIỂM CHỨNG THUẬT TOÁN: Chéo hóa lặp QR (diagonalize_with_qr) — Tự cài đặt vs NumPy")
    print(SEP)

    col_name    = 44
    col_rebuild = 20
    col_eig     = 18
    col_status  = 8

    header = (
        f"{'Test Case':<{col_name}}"
        f"{'Err Tái tạo A':>{col_rebuild}}"
        f"{'Err Trị riêng':>{col_eig}}"
        f"{'Kết quả':>{col_status}}"
    )
    print(header)
    print(HDR)

    passed_count = 0
    total_count  = len(test_cases)

    for case in test_cases:
        name = case["Nội dung"]
        A    = case["Ma trận A"]

        try:
            # Trường hợp mong đợi ném ngoại lệ
            if case.get("should_raise"):
                try:
                    diagonalize_with_qr(A)
                    # Không ném → FAIL
                    status = "[FAIL]"
                    name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
                    print(
                        f"{name_str:<{col_name}}"
                        f"{'N/A':>{col_rebuild}}"
                        f"{'N/A':>{col_eig}}"
                        f"{status:>{col_status}}"
                        f"  -> Lẽ ra phải ném {case['should_raise'].__name__}"
                    )
                except case["should_raise"]:
                    passed_count += 1
                    status = "[OK]  "
                    name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
                    print(
                        f"{name_str:<{col_name}}"
                        f"{'N/A':>{col_rebuild}}"
                        f"{'N/A':>{col_eig}}"
                        f"{status:>{col_status}}"
                        f"  (Bắt đúng {case['should_raise'].__name__})"
                    )
                except Exception as ex:
                    status = "[FAIL]"
                    name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
                    print(
                        f"{name_str:<{col_name}}"
                        f"{'N/A':>{col_rebuild}}"
                        f"{'N/A':>{col_eig}}"
                        f"{status:>{col_status}}"
                        f"  -> Lỗi ngoài mong đợi: {ex}"
                    )
                continue

            # Trường hợp thông thường
            ok, r_err, eig_err, eigenvalues = verify_diagonalize_qr_custom(A)

            # Kiểm tra thêm expected_eigenvalues nếu có
            if "expected_eigenvalues" in case:
                expected = _sort_eigenvalues(case["expected_eigenvalues"])
                got      = eigenvalues  # đã được sort_eigenvalues rồi
                sig_ok   = len(expected) == len(got) and all(
                    abs(e - g) < 1e-4 for e, g in zip(expected, got)
                )
                ok = ok and sig_ok

            if ok:
                passed_count += 1

            status   = "[OK]  " if ok else "[FAIL]"
            name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
            print(
                f"{name_str:<{col_name}}"
                f"{r_err:>{col_rebuild}.2e}"
                f"{eig_err:>{col_eig}.2e}"
                f"{status:>{col_status}}"
            )

        except Exception as ex:
            status   = "[FAIL]"
            name_str = (name[:col_name - 2] + "..") if len(name) > col_name else name
            print(
                f"{name_str:<{col_name}}"
                f"{'N/A':>{col_rebuild}}"
                f"{'N/A':>{col_eig}}"
                f"{status:>{col_status}}"
                f"  -> Lỗi: {ex}"
            )

    print(HDR)
    _print_summary_table(passed_count, total_count)


# ============================================================================
# TIỆN ÍCH IN TỔNG KẾT
# ============================================================================

def _print_summary_table(passed: int, total: int):
    """In dòng tổng kết theo format nhất quán với part1."""
    if total == 0:
        print("  [!] Không có test case nào.\n")
        return
    percent = passed / total * 100
    if passed == total:
        verdict = "TẤT CẢ ĐẠT"
    elif passed >= total * 0.8:
        verdict = "ĐẠT (còn lỗi nhỏ)"
    else:
        verdict = "CẦN KIỂM TRA LẠI"
    print(f"\n  Kết luận: {passed}/{total} test ({percent:.0f}%)  —  {verdict}\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    from part2.test_case_part2 import SVD_TEST_CASES, DIAGONALIZE_QR_TEST_CASES

    run_svd_tests(SVD_TEST_CASES)
    run_diagonalize_qr_tests(DIAGONALIZE_QR_TEST_CASES)

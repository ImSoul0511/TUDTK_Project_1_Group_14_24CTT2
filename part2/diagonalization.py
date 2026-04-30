import math
import random 
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import part2.utils as ut
import config as cfg 
from config import AutoTestReporter
from part2.verification import verify_diagonalize_numpy 
from part2.test_case import DIAGONALIZATION_TEST_CASES
from part1.gaussian import gaussian_eliminate

# Dùng thuật toán Jacobi để tìm toàn bộ vector riêng 
def eigen_calculation_with_jacobi(M, iterations=100):
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
        if cfg.is_zero(max_val): break

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

def eigen_calculation_reverse_iteration(A, max_iterations=500, tol=1e-7):
    """
    Tính toán Trị riêng và Vector riêng thông qua 2 bước:
    1. Dùng QR phân rã để tìm các Trị riêng xấp xỉ.
    2. Dùng Inverse Iteration (Lặp ngược) để tìm Vector riêng và làm mịn Trị riêng.
    """
    from part2.decomposition import householder_qr_v1
    
    Ak = ut.copy_matrix(A)
    n = len(Ak)
    
    # --- Tìm trị riêng xấp xỉ bằng thuật toán QR ---
    for _ in range(max_iterations):
        Q, R = householder_qr_v1(Ak)
        Ak = ut.matrix_multiply(R, Q)
        
        # Kiểm tra tổng các phần tử dưới đường chéo chính
        off_diag_sum = sum(abs(Ak[i][j]) for i in range(1, n) for j in range(i))
        
        # Nếu đã đủ "phẳng" (trở thành ma trận tam giác), thì dừng
        if cfg.is_zero(off_diag_sum):
            break
            
    # Trích xuất các trị riêng xấp xỉ trên đường chéo
    approx_eigenvalues = [Ak[i][i] for i in range(n)]

    # Lọc ra các trị riêng duy nhất
    unique_eigenvalues = []
    for lam in approx_eigenvalues:
        if not any(cfg.is_zero(lam - u) for u in unique_eigenvalues):
            unique_eigenvalues.append(lam)

    # --- Tìm vector riêng & làm mịn bằng lặp ngược ---
    final_eigenvalues = []
    P_cols = []

    # Hàm helper thực hiện lặp ngược cho từng nhóm trị riêng
    def _inverse_iteration(lam_approx, multiplicity):
        eps = 1e-10
        B = ut.matrix_sub_lambda_I(A, lam_approx + eps)
        
        eigenvecs = []
        refined_lams = []
        
        for _ in range(multiplicity):
            x = [random.random() for _ in range(n)]
            x = ut.vector_normalize(x)
            
            for _ in range(30): # max_iter của lặp ngược
                try:
                    _, y, _ = gaussian_eliminate(B, x)
                except ValueError:
                    y = x 
                    
                # Trực giao hóa (Gram-Schmidt) cho nghiệm kép
                for v in eigenvecs:
                    scalar = ut.dot_product(y, v)
                    y = ut.subtract_vectors(y, v, scalar)
                    
                x_new = ut.vector_normalize(y)
                
                # Kiểm tra hội tụ
                diff1 = max(abs(x_new[i] - x[i]) for i in range(n))
                diff2 = max(abs(x_new[i] + x[i]) for i in range(n))
                
                x = x_new
                if min(diff1, diff2) < tol:
                    break
                    
            # Tinh chỉnh trị riêng bằng Thương số Rayleigh
            Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            lam_refined = ut.dot_product(x, Ax)
            
            eigenvecs.append(x)
            refined_lams.append(lam_refined)
            
        return eigenvecs, refined_lams

    # Duyệt qua từng trị riêng duy nhất để tiến hành lặp ngược
    for lam in unique_eigenvalues:
        # Đếm bội số đại số (multiplicity) của trị riêng này
        multiplicity = sum(1 for val in approx_eigenvalues if cfg.is_zero(val - lam))
        
        # Gọi hàm lặp ngược
        found_vectors, refined_lams = _inverse_iteration(lam, multiplicity)
        
        # Đổ kết quả vào mảng tổng
        for i in range(len(found_vectors)):
            P_cols.append(found_vectors[i])
            final_eigenvalues.append(refined_lams[i])

    return final_eigenvalues, P_cols

def diagonalize(A):
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

    # Tìm giá trị riêng và vector riêng
    eigenvalues, P_cols = eigen_calculation_reverse_iteration(A)

    if len(P_cols) < n:
        raise ValueError("Ma trận A không thể chéo hóa (thiếu hụt vector riêng - defective matrix).")
    
    P = [[P_cols[j][i] for j in range(n)] for i in range(n)]
    
    # Tạo ma trận đường chéo D
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = eigenvalues[i]

    # Kiểm tra P có khả nghịch không (dấu hiệu ma trận có thể chéo hóa)
    try:
        P_inv = ut.matrix_inverse(P)
    except ValueError:
        raise ValueError("Ma trận A không thể chéo hóa: các vector riêng không độc lập tuyến tính (ma trận thiếu hụt).")

    return P, D, P_inv

def run_diagonalize_tests(test_cases: list[dict]):
    """
    Chạy toàn bộ test cases cho thuật toán Chéo hóa lặp QR tự cài đặt.

    Với mỗi test case sẽ in:
      - Tên test case
      - Trạng thái PASS / FAIL
      - Sai số tái tạo A = P*D*P_inv
      - Sai số trị riêng so với numpy (max absolute error)
    """
    AutoTestReporter.print_header("KIỂM CHỨNG THUẬT TOÁN: Chéo hóa (diagonalize) — Tự cài đặt vs NumPy")

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

    passed_count = 0
    total_count  = len(test_cases)

    for case in test_cases:
        name = case["Nội dung"]
        A    = case["Ma trận A"]

        try:
            # Trường hợp mong đợi ném ngoại lệ
            if case.get("should_raise"):
                try:
                    diagonalize(A)
                    # Không ném => FAIL
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
            ok, r_err, eig_err, eigenvalues = verify_diagonalize_numpy(A)

            # Kiểm tra thêm expected_eigenvalues nếu có
            if "expected_eigenvalues" in case:
                expected = ut._sort_eigenvalues(case["expected_eigenvalues"])
                got      = eigenvalues  # đã được sort_eigenvalues rồi
                len_ok   = len(expected) == len(got) and all(
                    abs(e - g) < 1e-5 for e, g in zip(expected, got)
                )
                ok = ok and len_ok

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

    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    run_diagonalize_tests(DIAGONALIZATION_TEST_CASES)

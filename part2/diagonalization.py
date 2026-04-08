import math
from utils import matrix_transpose

# --- TÌM GIÁ TRỊ RIÊNG & VECTOR RIÊNG ---
# Dùng thuật toán Jacobi để tìm toàn bộ vector riêng 
def eigen_decomposition(M, iterations=100):
    """
    Sử dụng phương pháp xoay Jacobi để 'chéo hóa' ma trận đối xứng M.
    Đây là cách máy tính thay thế việc giải phương trình det(M - lambda*I) = 0.
    """
    n = len(M)
    # V ban đầu là ma trận đơn vị, sau này sẽ chứa các vector riêng (eigenvectors)
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    # Tạo bản sao của ma trận M để tính toán (tránh làm hỏng dữ liệu gốc)
    A = [row[:] for row in M]

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
        if max_val < 1e-15: break

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

import utils as ut 

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
        normx = ut.vec_norm(slice_col)

        if normx == 0:
            continue 

        # Bước 3: Chọn dấu s = -sign(x₁), tránh triệt tiêu catastrophic
        s = -1 if R[j][j] >= 0 else 1 
        
        # Bước 4: Tính u₁ = x₁ - s * normx
        u1 = R[j][j] - s * normx 

        if abs(u1) < 1e-12: 
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
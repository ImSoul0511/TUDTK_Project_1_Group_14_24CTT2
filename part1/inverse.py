import config

def inverse(matrix_A):
    """
    Tính ma trận nghịch đảo A^-1 bằng phương pháp Gauss-Jordan có Partial Pivoting.

    Args:
        matrix_A: Ma trận hệ số
    
    Returns:
        Ma trận nghịch đảo

    """
    n = len(matrix_A)
    # 1. Kiểm tra ma trận có vuông không
    for row in matrix_A:
        if len(row) != n:
            raise ValueError("Ma trận không vuông, không thể tìm nghịch đảo.")
    # 2. Tạo ma trận  M = [A | I]
    M = []
    for i in range(n):
        row_A = [element for element in matrix_A[i]]
        row_I=[1.0 if i==j else 0.0 for j in range(n) ]
        M.append(row_A + row_I)

    # 3. Quá trình khử Gauss-Jordan
    for k in range(n):
        #a. Tìm dòng p có phần tử chốt lớn nhất từ dòng k trở xuống
        p = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[p][k]):
                p=i
        if config.is_zero(M[p][k]):
            print(f"Không có pivot tại cột {k}")
            return None
        # b. Hoán đổi dòng p và dòng k nếu cần
        if p != k:
            M[k], M[p] = M[p], M[k]
        # c. Chuẩn hóa dòng k
        pivot_val = M[k][k]
        for j in range(k, 2 * n):
            M[k][j] /= pivot_val
        # d. Khử Gauss-Jordan
        for i in range(n):
            if i != k:
                factor = M[i][k]
                for j in range(k, 2 * n):
                    M[i][j]=M[i][j]-factor*M[k][j]
    #4. Ma trận nghịch đảo
    inverse_matrix = []
    for i in range(n):
        inverse_matrix.append(M[i][n:])
    return inverse_matrix

def verify_inverse(matrix_A, inverse_A):
    """
    Kiểm chứng AA^-1 = I và so sánh kết quả với NumPy.

    Args:
        matrix_A: Ma trận hệ số
        inverse_A: Ma trận nghịch đảo
    
    Returns:
        True: Nếu tích AA^{-1} ra đúng ma trận đơn vị
        False: Nếu tích ra sai
    """
    import numpy as np
    # Kiểm tra xem inverse_A có tồn tại không (tránh lỗi khi hàm inverse tạch)
    if inverse_A is None:
        det_A = np.linalg.det(np.array(matrix_A, dtype=float))
        if config.is_zero(det_A): 
            return True 
        else:
            return False 
        
    # 1. Kiểm tra kích thước trước khi tính toán để tránh lỗi Broadcast
    rows_A = len(matrix_A)
    cols_A = len(matrix_A[0])
    rows_inv = len(inverse_A)
    cols_inv = len(inverse_A[0])

    # Ma trận nghịch đảo phải vuông và cùng kích thước với ma trận gốc
    if rows_A != cols_A or rows_inv != cols_inv or rows_A != rows_inv:
        return False
    
    A_np = np.array(matrix_A, dtype=float)
    inv_custom_np = np.array(inverse_A, dtype=float)
    n = len(matrix_A)

    # 1. Kiểm tra điều kiện AA^-1 = I
    # Tính tích A * A^-1
    identity_check = np.dot(A_np, inv_custom_np)
    I_matrix = np.eye(n)
    
    # Kiểm tra xem tích có xấp xỉ ma trận đơn vị không
    is_identity = np.allclose(identity_check, I_matrix, atol=config.EPSILON)

    # 2. So sánh trực tiếp với kết quả của NumPy
    try:
        inv_numpy = np.linalg.inv(A_np)
        matches_numpy = np.allclose(inv_custom_np, inv_numpy, atol=config.EPSILON)
    except np.linalg.LinAlgError:
        matches_numpy = False

    return is_identity and matches_numpy


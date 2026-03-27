
#Tính ma trận nghịch đảo A^-1 bằng phương pháp Gauss-Jordan có Partial Pivoting.
def inverse(matrix_A):
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

    EPSILON = 1e-12 # Ngưỡng để kiểm tra số 0, tránh sai số float
    # 3. Quá trình khử Gauss-Jordan
    for k in range(n):
        #a. Tìm dòng p có phần tử chốt lớn nhất từ dòng k trở xuống
        p = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[p][k]):
                p=i
        if abs(M[p][k]) < EPSILON:
            raise ValueError("Ma trận có định thức bằng 0, không tồn tại ma trận nghịch đảo.")
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




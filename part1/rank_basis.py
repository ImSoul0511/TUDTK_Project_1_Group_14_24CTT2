def rank_and_basis(matrix_A):
    """
    Tính hạng và tìm cơ sở của không gian dòng, không gian cột, 
    và không gian nghiệm dựa trên dạng bậc thang rút gọn (RREF).

    Args:
        A: Ma trận hệ số
    
    Returns:
        Hạng ma trận, cơ sở không gian dòng, không gian cột, 
        và không gian nghiệm

    """
    if not matrix_A or not matrix_A[0]:
        return 0, [], [], []            
    
    rows = len(matrix_A)
    cols = len(matrix_A[0])
    # 1. Giữ lại bản sao của A gốc để tìm Không gian cột
    A_original= [[val for val in row] for row in matrix_A]

    # 2. Tạo ma trận M để khử Gauss-Jordan về RREF
    M = [[val for val in row] for row in matrix_A]
    EPSILON = 1e-12 # Ngưỡng để kiểm tra số 0, tránh sai số float
    pivot_row = 0
    pivot_cols = []

    # 3. Khử Gauss-Jordan về dạng RREF
    for j in range(cols):
        if pivot_row >= rows:
            break
        
        max_row = pivot_row            # Tìm phần tử chốt (trị tuyệt đối lớn nhất) để giảm sai số
        for i in range(pivot_row + 1, rows):
            if abs(M[i][j]) > abs(M[max_row][j]):
                max_row = i

        if abs(M[max_row][j]) < EPSILON:
            print(f"Không có pivot tại cột {j}")
            continue

        if max_row != pivot_row:
            M[pivot_row], M[max_row] = M[max_row], M[pivot_row]
        pivot_cols.append(j)
        pivot_val = M[pivot_row][j]
        for c in range(j, cols):
            M[pivot_row][c] /= pivot_val
        for i in range(rows):
            if i != pivot_row:
                factor = M[i][j]
                for c in range(j, cols):
                    M[i][c] -= factor * M[pivot_row][c]
        pivot_row += 1

    #4 Trích xuất dữ liệu
    # a. Hạng ma trận
    rank_matrix = len(pivot_cols)

    # b. Cơ sở Không gian dòng R(A)
    row_space_basis = [M[i] for i in range(rank_matrix)]

    # c. Cơ sở Không gian cột C(A)
    col_space_basis = []
    for j in pivot_cols:
        col = [A_original[i][j] for i in range(rows)]
        col_space_basis.append(col)

    # d. Cơ sở Không gian nghiệm N(A) (Tập nghiệm Ax = 0)
    null_space_basis = []
    free_cols = [j for j in range(cols) if j not in pivot_cols ]
    for free_col_idx in free_cols:
        x = [0.0]*cols
        x[free_col_idx] = 1.0
        for i in range(rank_matrix):
            p=pivot_cols[i]
            x[p]=-M[i][free_col_idx]
        null_space_basis.append(x)

    return rank_matrix, row_space_basis, col_space_basis, null_space_basis

def verify_rank_and_basis(A, rank_custom, row_basis, col_basis, null_basis):
    """
    Kiểm chứng  hạng và cơ sở của không gian dòng, không gian cột, 
    và không gian nghiệm bằng Numpy

    Args:
        A: Ma trận hệ số
        rank_custom: Hạng ma trận
        row_basis: cơ sở không gian dòng
        col_basis: Cơ sở không gian cột
        null_basis: Cơ sở không gian nghiệm
    
    Returns:
        True: Nếu trùng khớp
        False: Nếu không trùng khớp
    """
    import numpy as np
    A_np = np.array(A, dtype=float)
    rows, cols = A_np.shape

    # --- 1. Kiểm tra Hạng (Rank) ---
    rank_np = np.linalg.matrix_rank(A_np)
    check_rank = (rank_custom == rank_np)

    # --- 2. Kiểm tra Không gian dòng (Row Space) ---
    # Các vector trong row_basis phải độc lập tuyến tính và có số lượng = rank
    check_row = False
    if len(row_basis) == rank_custom:
        # Cơ sở dòng tìm được phải có cùng không gian dòng với ma trận A gốc
        if np.linalg.matrix_rank(np.vstack((A_np, np.array(row_basis)))) == rank_custom:
            check_row = True

    # --- 3. Kiểm tra Không gian cột (Column Space) ---
    check_col = False
    if len(col_basis) == rank_custom:
        # Cơ sở cột tìm được phải có cùng không gian cột với ma trận A gốc
        if np.linalg.matrix_rank(np.hstack((A_np, np.array(col_basis).T))) == rank_custom:
            check_col = True

    # --- 4. Kiểm tra Không gian nghiệm (Null Space) ---
    # A * v phải = 0 và số lượng vector = cols - rank
    check_null = True
    if len(null_basis) != (cols - rank_custom):
        check_null = False
    else:
        for v in null_basis:
            if not np.allclose(np.dot(A_np, np.array(v)), 0, atol=1e-10):
                check_null = False
                break

    return check_rank, check_row, check_col, check_null



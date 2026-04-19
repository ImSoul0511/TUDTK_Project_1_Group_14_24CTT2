import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cfg

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

        if cfg.is_zero(M[max_row][j]):
            # Không có pivot tại cột j
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

def verify_test_rank_and_basis(test_cases: list[dict]):
    import warnings
    warnings.simplefilter("ignore", UserWarning)
    
    # Hàm test này kiểm tra hạng, số chiều của không gian nghiệm và cơ sở không gian nghiệm
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        try:
            rank, r_basis, c_basis, n_basis = rank_and_basis(case["Ma trận A"])
            
            assert rank == case["expected_rank"], f"Rank sai: got {rank}, want {case['expected_rank']}"
            
            if "expected_null_dim" in case:
                assert len(n_basis) == case["expected_null_dim"], f"Null dim sai: got {len(n_basis)}, want {case['expected_null_dim']}"
            if case.get("null_is_empty"):
                assert len(n_basis) == 0, "Không gian nghiệm lẽ ra phải rỗng"
                
            cfg.AutoTestReporter.print_result(case['Nội dung'], True)
            passed_count += 1
            
        except AssertionError as err:
            cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"(Assertion: {err})")
        except Exception as err:
            cfg.AutoTestReporter.print_result(case['Nội dung'], False, f"(Lỗi Runtime: {err})")
            
    cfg.AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import RANK_BASIS_TEST_CASES
    verify_test_rank_and_basis(RANK_BASIS_TEST_CASES)


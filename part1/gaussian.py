import config
from config import AutoTestReporter

def back_substitution(U, c):
    """
    Thực hiện phép thế ngược để giải hệ tam giác trên
    
    Args:
        U: Ma trận tam giác trên
        c: Vector vế phải
    
    Returns:
        Vector nghiệm x
    """
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        # Kiểm tra phần tử trên đường chéo chính
        if abs(U[i][i]) < config.EPSILON:
            return None
        x[i] = (c[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def gaussian_eliminate(A, b):
    """
    Thực hiện phép biến đổi Gauss để đưa ma trận A về dạng tam giác trên
    
    Args:
        A: Ma trận hệ số
        b: Vector vế phải
    
    Returns:
        Ma trận sau khi khử, nghiệm x, số lần hoán đổi
    """
    # Ghép ma trận A và vector b thành ma trận tăng cường M
    M = [row + [b[i]] for i, row in enumerate(A)]
    row = len(M)
    col = len(M[0])

    s = 0  # Đếm số lần hoán đổi dòng
    pivot_cols = []   
    current_row = 0

    for k in range(col-1):
        if current_row >= row:
            break

        # Tìm phần tử chốt (trị tuyệt đối lớn nhất) để giảm sai số
        p = current_row
        for i in range(current_row + 1, row):
            if abs(M[i][k]) > abs(M[p][k]):
                p = i

        if config.is_zero(M[p][k]): 
            # Không có pivot tại cột k
            continue
        
        if p != current_row:
            M[current_row], M[p] = M[p], M[current_row]
            s += 1
        pivot_cols.append(k)
        for i in range(current_row + 1, row):
            l_ik = M[i][k] / M[current_row][k]
            M[i][k] = 0
            for j in range(k + 1, col):
                M[i][j] -= l_ik * M[current_row][j]
        current_row += 1

    rank = len(pivot_cols)  #Tính hạng của ma trận

    #Hệ vô nghiệm
    #Tồn tại dòng có vế trái bằng 0 nhưng vế phải khác 0
    for i in range(rank, row):
        if not config.is_zero(M[i][col-1]):
            raise ValueError("Hệ phương trình vô nghiệm.")
    
    # Hệ có vô số nghiệm
    # rank < n (số ẩn): hệ vố số nghiệm
    if rank < col - 1:
        free_cols = [j for j in range(col-1) if j not in pivot_cols]

        # 1. Tìm nghiệm riêng x_p (Ngầm định các ẩn tự do = 0)
        x_p = [0.0] * (col-1)
        for i in range(rank - 1, -1, -1):
            p_col = pivot_cols[i]

            #Tính tổng giá trị của tất cả các ẩn số nằm bên phải ẩn chốt hiện tại
            s_val = sum(M[i][j] * x_p[j] for j in range(p_col + 1, col-1))  
            # x_chốt = (vế phải - tổng đã chuyển vế) / hệ số chốt
            x_p[p_col] = (M[i][col-1] - s_val) / M[i][p_col] 

        # 2. Tìm cơ sở không gian nghiệm (Giải hệ thuần nhất Ax = 0, bật lần lượt ẩn tự do = 1)
        null_basis = []
        for f in free_cols:
            v = [0.0] * (col-1)
            v[f] = 1.0  # Lần lượt cho từng ẩn tự do bằng 1, các ẩn tự do khác bằng 0
            for i in range(rank - 1, -1, -1):
                p_col = pivot_cols[i]

                # Tính tổng các ẩn nằm bên phải ẩn chốt hiện tại
                s_val = sum(M[i][j] * v[j] for j in range(p_col + 1, col-1))

                # Tìm ẩn chốt: x_chốt = -tổng / hệ số chốt (Do 0 - s_val = -s_val)
                v[p_col] = -s_val / M[i][p_col]
            null_basis.append(v)

        # 3. Nghiệm tổng quát = Nghiệm riêng + các cơ sở không gian nghiệm (kèm tham số c)
        formula = f"x = {[round(val, 4) for val in x_p]}"
        for idx, v in enumerate(null_basis):
            formula += f" + c{idx+1}*{[round(val, 4) for val in v]}"
        print("\nHệ có vô số nghiệm, công thức nghiệm tổng quát:")
        print(formula)
        return M, formula, s
    
    #Hệ có nghiệm duy nhất
    #rank = n (số ẩn)
    U = [row[:-1] for row in M[:rank]]
    c = [row[-1] for row in M[:rank]]
    x = back_substitution(U, c)

    return M, x, s 

def verify_solution(A, b, x_custom):
    """
    Kiểm chứng kết quả bằng NumPy

    Args:
        A: Ma trận hệ số
        b: Vector vế phải
        x_custom: nghiệm
    
    Return:
        True: Kết quả của bạn Khớp
        False: Kết quả của bạn Sai

    """
    import numpy as np
    # Xử lý kiểm tra cho trường hợp hệ vô số nghiệm / vô nghiệm (x là chuỗi hoặc x = None)
    if isinstance(x_custom, str) or x_custom is None:
        try:
            np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
            return False 
        except (np.linalg.LinAlgError, ValueError):
            return True 
        
    # Dùng numpy để kiểm tra lại trường hợp có nghiệm duy nhất
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    x_np = np.array(x_custom, dtype=float)

    # Kiểm tra xem A * x có xấp xỉ bằng b không
    return np.allclose(np.dot(A_np, x_np), b_np)

def verify_test_back_substitution(test_cases: list[dict]):
    import warnings
    warnings.simplefilter("ignore", UserWarning)
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        try:
            x_res = back_substitution(case["Ma trận U"], case["Vector cột c"])
            if case.get("expected_answer") == ValueError:
                AutoTestReporter.print_result(case['Nội dung'], False, "Lẽ ra phải phát sinh lỗi")
                continue
            
            expected = case.get("Nghiệm x")
            if expected is None:
                assert x_res is None, f"got {x_res}, want None"
            elif expected == []:
                assert x_res == [] or x_res is None, f"got {x_res}, want [] hoặc None"
            else:
                import numpy as np
                assert np.allclose(x_res, expected, atol=1e-7), f"got {x_res}, want {expected}"
                
            AutoTestReporter.print_result(case['Nội dung'], True)
            passed_count += 1
            
        except ValueError as err:
            if case.get("expected_answer") == ValueError:
                AutoTestReporter.print_result(case['Nội dung'], True, f"(Bắt đúng lỗi: {err})")
                passed_count += 1
            else:
                AutoTestReporter.print_result(case['Nội dung'], False, f"(Lỗi ngoài mong đợi: {err})")
        except AssertionError as err:
            AutoTestReporter.print_result(case['Nội dung'], False, f"(Assertion: {err})")
            
    AutoTestReporter.print_summary(passed_count, total_count)

def verify_test_gaussian_eliminate(test_cases: list[dict]):
    import warnings
    warnings.simplefilter("ignore", UserWarning)
    passed_count = 0
    total_count = len(test_cases)

    for case in test_cases:
        try:
            M_res, x_res, swaps = gaussian_eliminate(case["Ma trận A"], case.get("Vector cột b", []))
            if case.get("expected_answer"):
                AutoTestReporter.print_result(case['Nội dung'], False, "Lẽ ra phải phát sinh lỗi")
                continue
                
            if case.get("expected_non_unique"):
                assert isinstance(x_res, str) or x_res is None, "Hệ vô số/vô nghiệm nhưng trả về mảng"
            elif case.get("Nghiệm x"):
                import numpy as np
                assert np.allclose(x_res, case["Nghiệm x"], atol=1e-7), f"Nghiệm sai. got {x_res}, want {case['Nghiệm x']}"
                if "Số lần hoán đổi" in case:
                    assert swaps == case["Số lần hoán đổi"], f"Hoán đổi sai. got {swaps}, want {case['Số lần hoán đổi']}"
            
            AutoTestReporter.print_result(case['Nội dung'], True)
            passed_count += 1
            
        except ValueError as err:
            if case.get("expected_answer") == ValueError:
                AutoTestReporter.print_result(case['Nội dung'], True, f"\n-> Bắt đúng lỗi: {err}")
                passed_count += 1
            elif case.get("expected_non_unique") and "vô nghiệm" in str(err).lower():
                AutoTestReporter.print_result(case['Nội dung'], True, f"\n-> Bắt đúng hệ vô nghiệm")
                passed_count += 1
            else:
                AutoTestReporter.print_result(case['Nội dung'], False, f"\n-> Lỗi ngoài mong đợi: {err}")
        except Exception as err:
            if case.get("expected_answer") == type(err):
                AutoTestReporter.print_result(case['Nội dung'], True, f"\n-> Bắt đúng lỗi: {err}")
                passed_count += 1
            else:
                AutoTestReporter.print_result(case['Nội dung'], False, f"\n-> Lỗi Exception: {err}")
            
    AutoTestReporter.print_summary(passed_count, total_count)

if __name__ == "__main__":
    from test_case import BACK_SUBSTITUTION_TEST_CASES, GAUSSIAN_ELIMINATE_TEST_CASES
    verify_test_back_substitution(BACK_SUBSTITUTION_TEST_CASES)
    verify_test_gaussian_eliminate(GAUSSIAN_ELIMINATE_TEST_CASES)

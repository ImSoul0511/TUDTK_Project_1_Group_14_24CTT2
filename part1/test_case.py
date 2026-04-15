
# ----------------------------------------------------------------------------
# 1. TEST CASES: BACK SUBSTITUTION (THẾ NGƯỢC)
# ----------------------------------------------------------------------------
BACK_SUBSTITUTION_TEST_CASES = [
    {
        "name": "Hệ 2x2 cơ bản",
        "U": [[2.0, 1.0], [0.0, 4.0]],
        "c": [5.0, 8.0],
        "expect_x": [1.5, 2.0],
    },
    {
        "name": "Hệ 3x3 ma trận đường chéo",
        "U": [[3.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 5.0]],
        "c": [9.0, 4.0, -10.0],
        "expect_x": [3.0, -2.0, -2.0],
    },
    {
        "name": "Hệ 4x4 tam giác trên chuẩn",
        "U": [
            [1.0, 2.0, -1.0, 1.0],
            [0.0, -1.0, 3.0, 0.0],
            [0.0, 0.0, 2.0, -2.0],
            [0.0, 0.0, 0.0, 3.0],
        ],
        "c": [2.0, 5.0, -2.0, 6.0],
        "expect_x": [5.0, -2.0, 1.0, 2.0], 
    },
    {
        "name": "Có số 0 ở đường chéo chính (Suy biến) -> Trả về None",
        "U": [[1.0, 2.0, 3.0], [0.0, 0.0, 4.0], [0.0, 0.0, 5.0]],
        "c": [1.0, 2.0, 3.0],
        "expect_x": None, 
    },
    {
        "name": "Ma trận hệ số có giá trị cực lớn (Kiểm tra tràn số/sai số)",
        "U": [[1.0e8, -1.0], [0.0, 2.0e8]],
        "c": [1.0e8 - 2.0, 4.0e8],
        "expect_x": [1.0, 2.0],
    },
    {
        "name": "Hệ 1x1 (Kiểm tra biên nhỏ nhất)",
        "U": [[5.0]],
        "c": [10.0],
        "expect_x": [2.0],
    },
    {
        "name": "Ma trận rỗng (Edge Case)",
        "U": [],
        "c": [],
        "expect_x": [],
    },
]

# ----------------------------------------------------------------------------
# 2. TEST CASES: ĐỊNH THỨC (DETERMINANT)
# ----------------------------------------------------------------------------
DETERMINANT_TEST_CASES = [
    {
        "name": "Ma trận 2x2 thông thường",
        "A": [[4.0, 3.0], [6.0, 3.0]],
        "expected": -6.0, 
    },
    {
        "name": "Ma trận 3x3 đối xứng",
        "A": [[2.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]],
        "expected": 4.0,
    },
    {
        "name": "Cần hoán đổi dòng (Pivot swap)",
        "A": [[0.0, 2.0, 1.0], [3.0, -1.0, 4.0], [1.0, 1.0, 1.0]],
        "expected": 6.0, 
    },
    {
        "name": "Ma trận suy biến (Có dòng tỷ lệ với nhau)",
        "A": [[1.0, -2.0, 3.0], [-2.0, 4.0, -6.0], [5.0, 1.0, 2.0]],
        "expected": 0.0,
    },
    {
        "name": "Ma trận tam giác dưới",
        "A": [[5.0, 0.0, 0.0], [2.0, -3.0, 0.0], [1.0, 4.0, 2.0]],
        "expected": -30.0, 
    },
    {
        "name": "Trường hợp không vuông (Bắt lỗi)",
        "A": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        "should_raise": ValueError,
    },
    {
        "name": "Ma trận cấp 4x4",
        "A": [
            [1.0, 0.0, 2.0, -1.0],
            [3.0, 0.0, 0.0, 5.0],
            [2.0, 1.0, 4.0, -3.0],
            [1.0, 0.0, 5.0, 0.0],
        ],
        "expected": 30.0,
    },
    {
        "name": "Ma trận 1x1",
        "A": [[7.0]],
        "expected": 7.0,
    },
    {
        "name": "Ma trận toàn số 0 (Kích thước 2x2)",
        "A": [[0.0, 0.0], [0.0, 0.0]],
        "expected": 0.0,
    }
]

# ----------------------------------------------------------------------------
# 3. TEST CASES: KHỬ GAUSS (GAUSSIAN ELIMINATION)
# ----------------------------------------------------------------------------
GAUSSIAN_ELIMINATE_TEST_CASES = [
    {
        "name": "Hệ phương trình 2x2 nghiệm duy nhất",
        "A": [[2.0, 1.0], [1.0, -1.0]],
        "b": [4.0, -1.0],
        "expect_x": [1.0, 2.0],
        "expect_swaps": 0,
    },
    {
        "name": "Bắt buộc Partial Pivoting (Phần tử a[0][0] = 0)",
        "A": [[0.0, 2.0], [3.0, 1.0]],
        "b": [4.0, 5.0],
        "expect_x": [1.0, 2.0],
        "expect_swaps": 1,
    },
    {
        "name": "Hệ 3x3 cơ bản",
        "A": [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]],
        "b": [8.0, -11.0, -3.0],
        "expect_x": [2.0, 3.0, -1.0],
    },
    {
        "name": "Hệ vô nghiệm (Dòng cuối 0x = c với c != 0)",
        "A": [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]],
        "b": [3.0, 4.0, 5.0],
        "expect_non_unique": True,
        "should_raise": ValueError, 
    },
    {
        "name": "Hệ vô số nghiệm (Bậc tự do)",
        "A": [[1.0, -2.0, 1.0], [2.0, -4.0, 2.0], [3.0, -6.0, 3.0]],
        "b": [5.0, 10.0, 15.0],
        "expect_non_unique": True,
    },
    {
        "name": "Cột đầu tiên là số cực nhỏ (Chống lỗi sai số chuẩn)",
        "A": [[1e-15, 1.0], [1.0, 1.0]],
        "b": [2.0, 3.0],
        "expect_x": [1.0, 2.0],
    },
    {
        "name": "Hệ nhiều phương trình hơn số ẩn (Overdetermined), có nghiệm duy nhất",
        "A": [[1.0, 1.0], [1.0, -1.0], [2.0, 1.0]],
        "b": [3.0, 1.0, 5.0],
        "expect_x": [2.0, 1.0],
    }
]

# ----------------------------------------------------------------------------
# 4. TEST CASES: MA TRẬN NGHỊCH ĐẢO (INVERSE)
# ----------------------------------------------------------------------------
INVERSE_TEST_CASES = [
    {
        "name": "Ma trận 2x2 đẹp (det = 1)",
        "input": [[2.0, 5.0], [1.0, 3.0]],
        "expected_inv": [[3.0, -5.0], [-1.0, 2.0]]
    },
    {
        "name": "Ma trận 3x3 hoán vị",
        "input": [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        "expected_inv": [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
    },
    {
        "name": "Ma trận suy biến (Phải văng lỗi hoặc trả về None)",
        "input": [[4.0, 6.0], [2.0, 3.0]],
        "expected_inv": None
    },
    {
        "name": "Ma trận có nhiễu rất nhỏ (Ill-conditioned)",
        "input": [[1.0, 1.0], [1.0, 1.0 + 1e-12]],
        # Kiểm tra xem code có xử lý được hệ số cực gần nhau không
    },
    {
        "name": "Ma trận không vuông (Bắt lỗi ngay từ đầu)",
        "input": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        "should_raise": ValueError
    },
    {
        "name": "Ma trận 1x1",
        "input": [[4.0]],
        "expected_inv": [[0.25]]
    },
    {
        "name": "Ma trận đường chéo (chỉ nghịch đảo các phần tử chéo)",
        "input": [[2.0, 0.0], [0.0, 5.0]],
        "expected_inv": [[0.5, 0.0], [0.0, 0.2]]
    }
]

# ----------------------------------------------------------------------------
# 5. TEST CASES: HẠNG VÀ CƠ SỞ (RANK & BASIS)
# ----------------------------------------------------------------------------
RANK_BASIS_TEST_CASES = [
    {
        "name": "Rank đầy đủ (Ma trận 3x3)",
        "input": [[2.0, 0.0, -1.0], [4.0, -5.0, 2.0], [0.0, 0.0, 7.0]],
        "exp_rank": 3,
        "exp_null_dim": 0
    },
    {
        "name": "Ma trận toàn số 0 (Rank = 0)",
        "input": [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
        "exp_rank": 0,
        "exp_null_dim": 2
    },
    {
        "name": "Ma trận chữ nhật 3x4 (Thực tế Rank = 2)",
        "input": [
            [1.0, 2.0, 0.0, -1.0],
            [2.0, 6.0, -3.0, -3.0],
            [3.0, 10.0, -6.0, -5.0]
        ],
        "exp_rank": 2,
        "exp_null_dim": 2
    },
    {
        "name": "Các dòng phụ thuộc tuyến tính (Rank 1)",
        "input": [[1.0, -3.0, 2.0], [-2.0, 6.0, -4.0], [3.0, -9.0, 6.0]],
        "exp_rank": 1,
        "exp_null_dim": 2
    },
    {
        "name": "Ma trận chữ nhật dọc 4x2 (Rank tối đa = 2)",
        "input": [
            [1.0, 2.0], 
            [3.0, 4.0], 
            [5.0, 6.0], 
            [7.0, 8.0]
        ],
        "exp_rank": 2,
        "exp_null_dim": 0 # Số cột (2) - Rank (2) = 0
    },
    {
        "name": "Cần hoán vị dòng (Pivot a[0][0] = 0)",
        "input": [
            [0.0, 2.0, 1.0], 
            [1.0, -1.0, 0.0], 
            [0.0, 0.0, 3.0]
        ],
        "exp_rank": 3,
        "exp_null_dim": 0
    },
    {
        "name": "Chống sai số số học (Kiểm tra dung sai EPSILON)",
        "input": [
            [1.0, 1.0], 
            [1.0, 1.0 + 1e-16]
        ],
        "exp_rank": 1,
        "exp_null_dim": 1
    }
]

# ----------------------------------------------------------------------------
# 6. TEST CASES: KIỂM CHỨNG NGHIỆM (VERIFY SOLUTION)
# ----------------------------------------------------------------------------
VERIFY_SOLUTION_TEST_CASES = [
    {
        "name": "Nghiệm khớp hoàn hảo (Số nguyên)",
        "A": [[3.0, 2.0], [1.0, -1.0]], "x": [1.0, 1.0], "b": [5.0, 0.0],
        "expect_match": True,
    },
    {
        "name": "Nghiệm sai cố ý",
        "A": [[1.0, 2.0], [3.0, 4.0]], "x": [0.0, 0.0], "b": [5.0, 11.0],
        "expect_match": False,
    },
    {
        "name": "Kiểm tra sai số vô hạn tuần hoàn (1/3)",
        "A": [[3.0, 0.0], [0.0, 6.0]], "x": [1/3, 1/6], "b": [1.0, 1.0],
        "expect_match": True,
    },
    {
        "name": "Ma trận Hilbert 4x4 (Thử thách độ ổn định)",
        "A": [
            [1.0, 1/2, 1/3, 1/4],
            [1/2, 1/3, 1/4, 1/5],
            [1/3, 1/4, 1/5, 1/6],
            [1/4, 1/5, 1/6, 1/7]
        ],
        "x": [1.0, 1.0, 1.0, 1.0],
        "b": [25/12, 77/60, 57/60, 319/420], # Tính tổng từng dòng
        "expect_match": True,
    },
    {
        "name": "Nghiệm chứa giá trị 0",
        "A": [[2.0, -1.0], [1.0, 1.0]], 
        "x": [0.0, 3.0], 
        "b": [-3.0, 3.0],
        "expect_match": True,
    },
    {
        "name": "Hệ 3x3 với vector x chứa số không tương thích (Edge error)",
        "A": [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ],
        "x": [1.0, -1.0, 0.0],
        "b": [-1.0, -1.0, 0.0], 
        "expect_match": bool(False), # Kết quả mong muốn là False
        "expect_mismatch": True # Đánh dấu cờ in ra thông báo màu xanh dương
    }
]

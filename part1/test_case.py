
# ----------------------------------------------------------------------------
# TEST CASES: BACK SUBSTITUTION (THẾ NGƯỢC)
# ----------------------------------------------------------------------------
BACK_SUBSTITUTION_TEST_CASES = [
    {
        "Nội dung": "Hệ 2x2",
        "Ma trận U": [[2.0, 1.0], [0.0, 4.0]],
        "Vector cột c": [5.0, 8.0],
        "Nghiệm x": [1.5, 2.0],
    },
    {
        "Nội dung": "Hệ 3x3",
        "Ma trận U": [[3.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 5.0]],
        "Vector cột c": [9.0, 4.0, -10.0],
        "Nghiệm x": [3.0, -2.0, -2.0],
    },
    {
        "Nội dung": "Hệ 4x4 đơn giản",
        "Ma trận U": [
            [1.0, 2.0, -1.0, 1.0],
            [0.0, -1.0, 3.0, 0.0],
            [0.0, 0.0, 2.0, -2.0],
            [0.0, 0.0, 0.0, 3.0],
        ],
        "Vector cột c": [2.0, 5.0, -2.0, 6.0],
        "Nghiệm x": [5.0, -2.0, 1.0, 2.0], 
    },
    {
        "Nội dung": "Có số 0 ở đường chéo chính",
        "Ma trận U": [[1.0, 2.0, 3.0], [0.0, 0.0, 4.0], [0.0, 0.0, 5.0]],
        "Vector cột c": [1.0, 2.0, 3.0],
        "Nghiệm x": None, 
    },
    {
        "Nội dung": "Ma trận hệ số có giá trị cực lớn",
        "Ma trận U": [[1.0e8, -1.0], [0.0, 2.0e8]],
        "Vector cột c": [1.0e8 - 2.0, 4.0e8],
        "Nghiệm x": [1.0, 2.0],
    },
    {
        "Nội dung": "Hệ 1x1",
        "Ma trận U": [[5.0]],
        "Vector cột c": [10.0],
        "Nghiệm x": [2.0],
    }
]

# ----------------------------------------------------------------------------
# TEST CASES: expected_answer (DETERMINANT)
# ----------------------------------------------------------------------------
DETERMINANT_TEST_CASES = [
    {
        "Nội dung": "Ma trận 2x2",
        "Ma trận A": [[1.0, 2.0], [3.0, 4.0]],
        "expected_answer": -2.0, 
    },
    {
        "Nội dung": "Ma trận 3x3",
        "Ma trận A": [[1.0, -9.4, -12.0], [2.0, -6.0, 5.0], [5.0, -7.0, 6.5]],
        "expected_answer": -308.8,
    },
    {
        "Nội dung": "Ma trận suy biến",
        "Ma trận A": [[1.0, -2.0, 3.0], [-2.0, 4.0, -6.0], [5.0, 1.0, 2.0]],
        "expected_answer": 0.0,
    },
    {
        "Nội dung": "Ma trận không vuông",
        "Ma trận A": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        "should_raise": ValueError,
    },
    {
        "Nội dung": "Ma trận 4x4",
        "Ma trận A": [
            [1.0, 0.0, 2.0, -1.0],  
            [3.0, 0.0, 0.0, 5.0],
            [2.0, 1.0, 4.0, -3.0],
            [1.0, 0.0, 5.0, 0.0],
        ],
        "expected_answer": 30.0,
    },
    {
        "Nội dung": "Ma trận 1x1",
        "Ma trận A": [[1.0]],
        "expected_answer": 1.0,
    },
    {
        "Nội dung": "Ma trận toàn số 0",
        "Ma trận A": [[0.0, 0.0], [0.0, 0.0]],
        "expected_answer": 0.0,
    }
]

# ----------------------------------------------------------------------------
# TEST CASES: KHỬ GAUSS (GAUSSIAN ELIMINATION)
# ----------------------------------------------------------------------------
GAUSSIAN_ELIMINATE_TEST_CASES = [
    {
        "Nội dung": "Hệ phương trình 2x2 nghiệm duy nhất",
        "Ma trận A": [[2.0, 1.0], [1.0, -1.0]],
        "Vector cột b": [4.0, -1.0],
        "Nghiệm x": [1.0, 2.0],
        "Số lần hoán đổi": 0,
    },
    {
        "Nội dung": "Bắt buộc Partial Pivoting (Phần tử a[0][0] = 0)",
        "Ma trận A": [[0.0, 2.0], [3.0, 1.0]],
        "Vector cột b": [4.0, 5.0],
        "Nghiệm x": [1.0, 2.0],
        "Số lần hoán đổi": 1,
    },
    {
        "Nội dung": "Hệ 3x3 cơ bản",
        "Ma trận A": [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]],
        "Vector cột b": [8.0, -11.0, -3.0],
        "Nghiệm x": [2.0, 3.0, -1.0],
    },
    {
        "Nội dung": "Hệ vô nghiệm",
        "Ma trận A": [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]],
        "Vector cột b": [3.0, 4.0, 5.0],
        "expected_non_unique": True,
        "expected_answer": ValueError,
    },
    {
        "Nội dung": "Hệ vô số nghiệm",
        "Ma trận A": [[1.0, -2.0, 1.0], [2.0, -4.0, 2.0], [3.0, -6.0, 3.0]],
        "Vector cột b": [5.0, 10.0, 15.0],
        "expected_non_unique": True,
    },
    {
        "Nội dung": "Cột đầu tiên là số cực nhỏ (Chống lỗi sai số chuẩn)",
        "Ma trận A": [[1e-15, 1.0], [1.0, 1.0]],
        "Vector cột b": [2.0, 3.0],
        "Nghiệm x": [1.0, 2.0],
    },
    {
        "Nội dung": "Hệ nhiều phương trình hơn số ẩn, có nghiệm duy nhất",
        "Ma trận A": [[1.0, 1.0], [1.0, -1.0], [2.0, 1.0]],
        "Vector cột b": [3.0, 1.0, 5.0],
        "Nghiệm x": [2.0, 1.0],
    }
]

# ----------------------------------------------------------------------------
# TEST CASES: MA TRẬN NGHỊCH ĐẢO (INVERSE)
# ----------------------------------------------------------------------------
INVERSE_TEST_CASES = [
    {
        "Nội dung": "Ma trận 2x2",
        "Ma trận A": [[2.0, 5.0], [1.0, 3.0]],
        "expected_answer": [[3.0, -5.0], [-1.0, 2.0]]
    },
    {
        "Nội dung": "Ma trận 3x3 hoán vị",
        "Ma trận A": [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        "expected_answer": [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
    },
    {
        "Nội dung": "Ma trận suy biến",
        "Ma trận A": [[4.0, 6.0], [2.0, 3.0]],
        "expected_answer": None
    },
    {
        "Nội dung": "Ma trận không vuông",
        "Ma trận A": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        "should_raise": ValueError
    },
    {
        "Nội dung": "Ma trận 1x1",
        "Ma trận A": [[4.0]],
        "expected_answer": [[0.25]]
    }
]

# ----------------------------------------------------------------------------
# TEST CASES: HẠNG VÀ CƠ SỞ (RANK & BASIS)
# ----------------------------------------------------------------------------
RANK_BASIS_TEST_CASES = [
    {
        "Nội dung": "Rank đầy đủ (Ma trận 3x3)",
        "Ma trận A": [[2.0, 0.0, -1.0], [4.0, -5.0, 2.0], [0.0, 0.0, 7.0]],
        "expected_rank": 3,
        "expected_null_dim": 0
    },
    {
        "Nội dung": "Ma trận toàn số 0 (Rank = 0)",
        "Ma trận A": [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
        "expected_rank": 0,
        "expected_null_dim": 2
    },
    {
        "Nội dung": "Ma trận chữ nhật 3x4 (Thực tế Rank = 2)",
        "Ma trận A": [
            [1.0, 2.0, 0.0, -1.0],
            [2.0, 6.0, -3.0, -3.0],
            [3.0, 10.0, -6.0, -5.0]
        ],
        "expected_rank": 2,
        "expected_null_dim": 2
    },
    {
        "Nội dung": "Các dòng phụ thuộc tuyến tính (Rank 1)",
        "Ma trận A": [[1.0, -3.0, 2.0], [-2.0, 6.0, -4.0], [3.0, -9.0, 6.0]],
        "expected_rank": 1,
        "expected_null_dim": 2
    },
    {
        "Nội dung": "Ma trận chữ nhật dọc 4x2 (Rank tối đa = 2)",
        "Ma trận A": [
            [1.0, 2.0], 
            [3.0, 4.0], 
            [5.0, 6.0], 
            [7.0, 8.0]
        ],
        "expected_rank": 2,
        "expected_null_dim": 0 # Số cột (2) - Rank (2) = 0
    },
    {
        "Nội dung": "Cần hoán vị dòng (Pivot a[0][0] = 0)",
        "Ma trận A": [
            [0.0, 2.0, 1.0], 
            [1.0, -1.0, 0.0], 
            [0.0, 0.0, 3.0]
        ],
        "expected_rank": 3,
        "expected_null_dim": 0
    },
    {
        "Nội dung": "Chống sai số số học (Kiểm tra dung sai EPSILON)",
        "Ma trận A": [
            [1.0, 1.0], 
            [1.0, 1.0 + 1e-16]
        ],
        "expected_rank": 1,
        "expected_null_dim": 1
    }
]

# ----------------------------------------------------------------------------
# TEST CASES: KIỂM CHỨNG NGHIỆM (VERIFY SOLUTION)
# ----------------------------------------------------------------------------
VERIFY_SOLUTION_TEST_CASES = [
    {
        "Nội dung": "Nghiệm trả về đúng",
        "A": [[3.0, 2.0], [1.0, -1.0]], "x": [1.0, 1.0], "b": [5.0, 0.0],
    },
    {
        "Nội dung": "Nghiệm trả về sai",
        "A": [[1.0, 2.0], [3.0, 4.0]], "x": [0.0, 0.0], "b": [5.0, 11.0],
        "expect_mismatch": True,
    },
    {
        "Nội dung": "Ma trận Hilbert 4x4",
        "A": [
            [1.0, 1/2, 1/3, 1/4],
            [1/2, 1/3, 1/4, 1/5],
            [1/3, 1/4, 1/5, 1/6],
            [1/4, 1/5, 1/6, 1/7]
        ],
        "x": [1.0, 1.0, 1.0, 1.0],
        "b": [25/12, 77/60, 57/60, 319/420], 
    },
    {
        "Nội dung": "Nghiệm chứa 0",
        "A": [[2.0, -1.0], [1.0, 1.0]], 
        "x": [0.0, 3.0], 
        "b": [-3.0, 3.0],
    },
    {
        "Nội dung": "Nghiệm chênh lệch nhỏ",
        "A": [[1.0, 1.0], [1.0, 1.0000000000001]],
        "x": [1.0, 1.0],
        "b": [2.0, 2.0000000000001]
    }
]

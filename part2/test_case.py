import numpy as np

# --- HÀM BỔ TRỢ TÍNH GIÁ TRỊ THAM CHIẾU ---
def get_expected_sigmas(A):
    """Sử dụng numpy để tính các giá trị kỳ dị (sigmas) tham chiếu."""
    _, s, _ = np.linalg.svd(A)
    return s.tolist()
# ----------------------------------------------------------------------------
# TEST CASES: PHÂN RÃ SVD (Singular Value Decomposition)
# ----------------------------------------------------------------------------
# Chiến lược kiểm chứng:
#   - Tái tạo: A ≈ U * Σ * Vt  (sai số tối đa EPSILON)
#   - Trực giao: U^T * U ≈ I  và  Vt * Vt^T ≈ I
#   - Thứ tự: sigmas giảm dần (sigmas[i] >= sigmas[i+1])
#   - Giá trị kỳ dị: so sánh với numpy (nếu có "expected_sigmas")
# ----------------------------------------------------------------------------
SVD_TEST_CASES = [
    {
        "Nội dung": "Ma trận 2x2 cơ bản",
        "Ma trận A": [
            [3.0, 0.0],
            [4.0, 5.0],
        ],
        # sigmas tính bằng np.linalg.svd để tham chiếu
        "expected_sigmas": get_expected_sigmas([
            [3.0, 0.0],
            [4.0, 5.0],
        ]),
    },
    {
        "Nội dung": "Ma trận 3x2 (chữ nhật ngang hơn dọc)",
        "Ma trận A": [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ],
        "expected_sigmas": get_expected_sigmas ([
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]),
    },
    {
        "Nội dung": "Ma trận 2x3 (chữ nhật rộng hơn cao)",
        "Ma trận A": [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]),
    },
    {
        "Nội dung": "Ma trận đường chéo 3x3 (sigma = |đường chéo| giảm dần)",
        "Ma trận A": [
            [4.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [4.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, 1.0],
        ]),
    },
    {
        "Nội dung": "Ma trận đơn vị 3x3 (tất cả sigma = 1)",
        "Ma trận A": [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]),
    },
    {
        "Nội dung": "Ma trận có hàng tuyến tính phụ thuộc (sigma bé nhất = 0)",
        "Ma trận A": [
            [1.0, 2.0, 3.0],
            [2.0, 4.0, 6.0],   # = 2 * hàng 1
            [0.0, 1.0, 0.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [1.0, 2.0, 3.0],
            [2.0, 4.0, 6.0],
            [0.0, 1.0, 0.0],
        ]),
        # Rank = 2 → sigma thứ nhỏ nhất ≈ 0
        "expected_rank": 2,
    },
    {
        "Nội dung": "Ma trận vuông 3x3 không đối xứng",
        "Ma trận A": [
            [1.0, 2.0, 3.0],
            [0.0, 4.0, 5.0],
            [0.0, 0.0, 6.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [1.0, 2.0, 3.0],
            [0.0, 4.0, 5.0],
            [0.0, 0.0, 6.0],
        ]),
    },
    {
        "Nội dung": "Ma trận vuông 4x4",
        "Ma trận A": [
            [ 1.0,  2.0,  0.0, -1.0],
            [ 3.0,  0.0,  1.0,  2.0],
            [-1.0,  4.0,  2.0,  0.0],
            [ 2.0, -1.0,  3.0,  1.0],
        ],
        "expected_sigmas": get_expected_sigmas([
            [ 1.0,  2.0,  0.0, -1.0],
            [ 3.0,  0.0,  1.0,  2.0],
            [-1.0,  4.0,  2.0,  0.0],
            [ 2.0, -1.0,  3.0,  1.0],
        ]),
    },
    {
        "Nội dung": "Ma trận toàn 0 (tất cả sigma = 0)",
        "Ma trận A": [
            [0.0, 0.0],
            [0.0, 0.0],
        ],
        "expected_sigmas": [0.0, 0.0],
    },
    {
        "Nội dung": "Ma trận 1x1",
        "Ma trận A": [[7.0]],
        "expected_sigmas": [7.0],
    },
]


# ----------------------------------------------------------------------------
# TEST CASES: CHÉO HÓA BẰNG PHƯƠNG PHÁP LẶP QR (diagonalize_with_qr)
# ----------------------------------------------------------------------------
# Chiến lược kiểm chứng:
#   - Tái tạo: A ≈ P * D * P_inv  (sai số tối đa EPSILON)
#   - Trị riêng: D[i][i] so sánh với np.linalg.eig (không phụ thuộc thứ tự)
#   - should_raise: True nếu hàm phải ném ValueError
# ----------------------------------------------------------------------------
DIAGONALIZATION_TEST_CASES = [
    {
        "Nội dung": "Ma trận 2x2 đối xứng cơ bản",
        "Ma trận A": [
            [4.0, 1.0],
            [1.0, 3.0],
        ],
        # Trị riêng: 4.618..., 2.382...  (kết quả np.linalg.eig làm tham chiếu)
        "expected_eigenvalues": [4.618033988749895, 2.381966011250105],
    },
    {
        "Nội dung": "Ma trận 2x2 không đối xứng",
        "Ma trận A": [
            [2.0, 1.0],
            [0.0, 3.0],
        ],
        "expected_eigenvalues": [3.0, 2.0],
    },
    {
        "Nội dung": "Ma trận đường chéo 3x3 (trị riêng = giá trị đường chéo)",
        "Ma trận A": [
            [5.0, 0.0, 0.0],
            [0.0, 3.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        "expected_eigenvalues": [5.0, 3.0, 1.0],
    },
    {
        "Nội dung": "Ma trận 3x3 đối xứng",
        "Ma trận A": [
            [ 4.0, -2.0,  1.0],
            [-2.0,  4.0, -2.0],
            [ 1.0, -2.0,  4.0],
        ],
        "expected_eigenvalues": [7.372281323269014, 3.0, 1.6277186767309864],
    },
    {
        "Nội dung": "Ma trận 3x3 tam giác trên",
        "Ma trận A": [
            [6.0, 1.0, 2.0],
            [0.0, 4.0, 3.0],
            [0.0, 0.0, 2.0],
        ],
        # Trị riêng của ma trận tam giác = các phần tử đường chéo
        "expected_eigenvalues": [6.0, 4.0, 2.0],
    },
    {
        "Nội dung": "Ma trận 3x3 không đối xứng thông thường",
        "Ma trận A": [
            [1.0, 2.0, 0.0],
            [0.0, 3.0, 1.0],
            [0.0, 0.0, 2.0],
        ],
        "expected_eigenvalues": [3.0, 2.0, 1.0],
    },
    {
        "Nội dung": "Ma trận 4x4 đối xứng",
        "Ma trận A": [
            [ 4.0,  1.0, -1.0,  0.0],
            [ 1.0,  3.0,  0.0, -1.0],
            [-1.0,  0.0,  4.0,  1.0],
            [ 0.0, -1.0,  1.0,  3.0],
        ],
        "expected_eigenvalues": [5.618033988749897, 3.618033988749895, 3.381966011250105, 1.3819660112501055],
    },
    {
        "Nội dung": "Ma trận đơn vị 3x3 (tất cả trị riêng = 1)",
        "Ma trận A": [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        "expected_eigenvalues": [1.0, 1.0, 1.0],
    },
    {
        "Nội dung": "Ma trận không vuông — phải ném ValueError",
        "Ma trận A": [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ],
        "should_raise": ValueError,
    },
    {
        "Nội dung": "Ma trận 1x1",
        "Ma trận A": [[9.0]],
        "expected_eigenvalues": [9.0],
    },
]

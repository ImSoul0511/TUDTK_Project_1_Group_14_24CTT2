import numpy as np

def generate_random_system(n: int, force_diagonally_dominant: bool = False):
    """
    Sinh hệ phương trình Ax = b ngẫu nhiên.
    Nếu force_diagonally_dominant=True, ma trận A sẽ có tính chéo trội nghiêm ngặt.
    """
    A = np.random.rand(n, n)
    if force_diagonally_dominant:
        # Tăng giá trị đường chéo chính để đảm bảo tính chéo trội
        diag = np.sum(np.abs(A), axis=1) + 1
        np.fill_diagonal(A, diag)
    
    # Sinh nghiệm x_true ngẫu nhiên trước để tính b = A @ x_true
    x_true = np.random.rand(n)
    b = A @ x_true
    return A, b, x_true

def generate_spd_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận đối xứng xác định dương (Well-conditioned).
    Thuật toán: Sinh ma trận ngẫu nhiên X, tính A = X @ X^T + n * I.
    """
    X = np.random.randn(n, n)
    # n * np.eye(n) giúp ma trận "cách xa" trạng thái suy biến, làm giảm số điều kiện
    A = X @ X.T + n * np.eye(n)
    return A.tolist()

def generate_hilbert_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận Hilbert H_n (Ill-conditioned).
    Công thức: H[i][j] = 1 / (i + j + 1)
    """
    i, j = np.ogrid[:n, :n]
    H = 1.0 / (i + j + 1)
    return H.tolist()

def relative_error(x_approx, x_true):
    """
    Tính sai số tương đối.
    """
    return np.linalg.norm(x_approx - x_true) / np.linalg.norm(x_true)

def calculate_condition_number(A: list[list[float]]) -> float:
    """
    Tính số điều kiện k_2(A) để đối chứng.
    """
    return np.linalg.cond(A, p=2)

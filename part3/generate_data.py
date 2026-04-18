import numpy as np

def generate_random_system(n: int, force_diagonally_dominant: bool = False):
    """
    Sinh hệ phương trình ngẫu nhiên.
    """
    A = np.random.uniform(-10, 10, (n, n))
    b = np.random.uniform(-10, 10, n)

    if force_diagonally_dominant:
        # Tính tổng trị tuyệt đối của từng hàng
        row_sums = np.sum(np.abs(A), axis=1)
        # Ghi đè phần tử trên đường chéo bằng tổng hàng + 1 lượng ngẫu nhiên để đảm bảo trội CHẶT
        np.fill_diagonal(A, row_sums + np.random.uniform(1.0, 5.0, n))

    return A.tolist(), b.tolist()

def generate_spd_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận đối xứng xác định dương (Well-conditioned).
    Thuật toán: Sinh ma trận ngẫu nhiên X, tính A = X @ X^T + n * I.
    """
    X = np.random.uniform(-10, 10, (n, n))
    A = X @ X.T + n * np.eye(n)
    return A.tolist()

def generate_hilbert_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận Hilbert H_n (Ill-conditioned).
    Công thức: H[i][j] = 1 / (i + j + 1)
    """
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = 1.0 / (i + j + 1)
    return H.tolist()

def calculate_condition_number(A: list[list[float]]) -> float:
    """
    Tính số điều kiện k_2(A) để đối chứng.
    """
    A_np = np.array(A)
    cond = np.linalg.cond(A_np)
    return float(cond)
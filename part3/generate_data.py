import numpy as np

def generate_random_system(n: int, force_diagonally_dominant: bool = False):
    """
    Sinh hệ phương trình tuyến tính Ax = b một cách ngẫu nhiên.

    Thuật toán:
    1. Sinh ma trận A và vector b ngẫu nhiên trong khoảng [-10, 10].
    2. Nếu `force_diagonally_dominant=True`, tính tổng hàng và cộng vào đường chéo chính để đảm bảo hội tụ cho các phương pháp lặp.

    Args:
        n (int): Kích thước của ma trận.
        force_diagonally_dominant (bool): Nếu True, cưỡng ép ma trận A là ma trận trội đường chéo hàng.
    
    Returns:
        tuple[list[list[float]], list[float]]: Một cặp gồm ma trận A và vector b.
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
    Sinh ma trận đối xứng xác định dương (Symmetric Positive Definite - SPD).
    
    Thuật toán:
    1. Sinh ma trận ngẫu nhiên X.
    2. Tính A = X @ X^T (đảm bảo tính đối xứng và nửa xác định dương).
    3. Cộng thêm n * I (đảm bảo xác định dương và cải thiện số điều kiện).

    Args:
        n (int): Kích thước của ma trận.

    Returns:
        list[list[float]]: Ma trận SPD kích thước n x n.
    """
    X = np.random.uniform(-10, 10, (n, n))
    A = X @ X.T + n * np.eye(n)
    return A.tolist()

def generate_hilbert_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận Hilbert H_n (Ma trận cực kỳ xấu - Ill-conditioned).
    
    Thuật toán:
    Khởi tạo ma trận n x n và tính từng phần tử theo công thức: $H[i,j] = 1 / (i + j + 1)$ (với i, j bắt đầu từ 0).

    Args:
        n (int): Kích thước của ma trận.

    Returns:
        list[list[float]]: Ma trận Hilbert kích thước n x n.
    """
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = 1.0 / (i + j + 1)
    return H.tolist()

def calculate_condition_number(A: list[list[float]]) -> float:
    """
    Tính số điều kiện (Condition number) k_2(A) của ma trận A để đối chứng.

    Thuật toán:
    Sử dụng thư viện `numpy.linalg.cond` để tính dựa trên tỷ số giữa trị riêng lớn nhất và nhỏ nhất (hoặc giá trị suy biến).

    Args:
        A (list[list[float]]): Ma trận cần tính số điều kiện.

    Returns:
        float: Giá trị số điều kiện.
    """
    A_np = np.array(A)
    cond = np.linalg.cond(A_np)
    return float(cond)
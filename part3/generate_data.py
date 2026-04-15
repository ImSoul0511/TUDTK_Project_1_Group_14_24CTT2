import numpy as np

def generate_random_system(n: int, force_diagonally_dominant: bool = False):
    """
    Sinh hệ phương trình ngẫu nhiên.
    """

def generate_spd_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận đối xứng xác định dương (Well-conditioned).
    Thuật toán: Sinh ma trận ngẫu nhiên X, tính A = X @ X^T + n * I.
    """

def generate_hilbert_matrix(n: int) -> list[list[float]]:
    """
    Sinh ma trận Hilbert H_n (Ill-conditioned).
    Công thức: H[i][j] = 1 / (i + j + 1)
    """

def calculate_condition_number(A: list[list[float]]) -> float:
    """
    Tính số điều kiện k_2(A) để đối chứng.
    """
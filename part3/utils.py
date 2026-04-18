import numpy as np


def compute_l2_error(x_true: list[float], x_pred: list[float]) -> float:
    """
    Tính sai số tương đối chuẩn L2 (Relative L2 Error).
    Công thức: ||x_true - x_pred||_2 / ||x_true||_2
    """
    x_t = np.array(x_true, dtype=float)
    x_p = np.array(x_pred, dtype=float)

    # Tính tử số: ||x_true - x_pred||_2
    numerator = np.linalg.norm(x_t - x_p, 2)

    # Tính mẫu số: ||x_true||_2
    denominator = np.linalg.norm(x_t, 2)

    # Tránh chia cho 0 trong trường hợp x_true là vector 0
    if denominator < 1e-18:
        return float(numerator) if numerator > 1e-18 else 0.0

    return float(numerator / denominator)

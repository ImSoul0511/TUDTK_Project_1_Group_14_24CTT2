import time
import json
import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import compute_l2_error
from part3.solvers import solve_system
from part3.generate_data import generate_random_system, generate_hilbert_matrix, generate_spd_matrix, calculate_condition_number

def measure_execution_metrics():
    """
    Đo thời gian và sai số của 3 thuật toán với n thay đổi.
    """


def measure_condition_stability():
    """
    Đo lường độ ổn định trên ma trận Hilbert và SPD.
    """
    pass 
    
# ===== ĐÂY LÀ ĐOẠN LỆNH ĐỂ XUẤT RA FILE JSON =====
##if __name__ == "__main__":
    

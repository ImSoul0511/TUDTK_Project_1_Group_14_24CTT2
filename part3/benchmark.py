import time
import json
import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from part3.utils import compute_l2_error
from part3.solvers import solve_system
from part3.generate_data import generate_random_system, generate_hilbert_matrix, generate_spd_matrix, calculate_condition_number

def measure_execution_metrics():
    """
    Đo thời gian và sai số của 3 thuật toán với n thay đổi.
    """
    size = [50, 100, 200, 500, 1000]
    methods = ['gauss', 'svd', 'gauss_seidel']
    results = {m : {} for m in methods}

    for n in size:
        # Lấy ma trận A từ hàm sinh ngẫu nhiên
        A, b = generate_random_system(n, force_diagonally_dominant=True)

        # Tự sinh một nghiệm đúng x_true ngẫu nhiên từ -10  đến 10
        x_true = np.random.uniform(-10, 10, n).tolist()

        b = np.dot(np.array(A), np.array(x_true)).tolist()

        for method in methods:
            total_time =0.0
            num_trials = 10
            last_error =0.0
            
            for i in range(num_trials):
                start_time = time.perf_counter()
                x_pred = solve_system(A, b, method)
                end_time = time.perf_counter()
                total_time += (end_time - start_time)*1000  #Đổi s sang ms
                last_error = compute_l2_error(x_true, x_pred)

            avg_time = total_time/num_trials
            results[method][n] = {
                'time_ms': avg_time,
                'relative_error': last_error
            }

            print(f"Method: {method}, Size: {n}, Avg Time: {avg_time:.4f} ms, Error: {last_error:.4e}")

                
    return results


def measure_condition_stability():
    """
    Đo lường độ ổn định trên ma trận Hilbert và SPD.
    """

    sizes = [5, 10, 15, 20, 50] 
    methods = ['gauss', 'svd', 'gauss_seidel']

    results = {
        "hilbert": {str(n): {"condition_number": 0, "errors": {}} for n in sizes},
        "spd": {str(n): {"condition_number": 0, "errors": {}} for n in sizes}
    }

    print("\n=== BẮT ĐẦU ĐO ĐỘ ỔN ĐỊNH SỐ HỌC (ĐỊNH LÝ 3.1) ===")
   
    for n in sizes:
        A_hilbert = generate_hilbert_matrix(n)
        A_spd = generate_spd_matrix(n)

        x_true = [1.0] * n
        b_hilbert = np.dot(np.array(A_hilbert), np.array(x_true)).tolist()
        b_spd = np.dot(np.array(A_spd), np.array(x_true)).tolist()

        results["hilbert"][str(n)]["condition_number"] = calculate_condition_number(A_hilbert)
        results["spd"][str(n)]["condition_number"] = calculate_condition_number(A_spd)

        for method in methods:
            try:
                x_hat_hilbert = solve_system(A_hilbert, b_hilbert, method)
                err_hilbert = compute_l2_error(x_true, x_hat_hilbert)
            except Exception:
                err_hilbert = "FAILED" 
            results["hilbert"][str(n)]["errors"][method] = err_hilbert
            
            try:
                x_hat_spd = solve_system(A_spd, b_spd, method)
                err_spd = compute_l2_error(x_true, x_hat_spd)
            except Exception:
                err_spd = "FAILED"
            results["spd"][str(n)]["errors"][method] = err_spd

    return results    

if __name__ == "__main__":
    final_data = {
        "execution_metrics": measure_execution_metrics(),
        "condition_stability": measure_condition_stability()
    }

    current_dir = os.path.dirname(__file__)
    output_path = os.path.join(current_dir, 'benchmark_results.json')
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)


    

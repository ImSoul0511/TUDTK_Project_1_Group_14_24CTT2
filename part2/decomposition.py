import utils

def update_submatrix_R(R, w, tau, j):
    """
    Cập nhật R theo công thức:
    R(j:end,:) = R(j:end,:)-(tau*w)*(w_T*R(j:end,:));

    Args: 
        R: 
    """
    m = len(R)
    n = len(R[0])

    w_T_R = []
    for col in range(n):
        dot_val = 0
        for row in range(j, m):
            dot_val += w[row - j] * R[row][col]
            w_T_R.append(dot_val)
        
    for row in range(j, m):
        for col in range(n):
            R[row][col] -= tau * w[row - j] * w_T_R[col]
        
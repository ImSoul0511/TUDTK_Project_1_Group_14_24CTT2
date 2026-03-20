def back_substitution(U, c):
    """
    Thực hiện phép thế ngược để giải hệ tam giác trên
    
    Args:
        U: Ma trận tam giác trên
        c: Vector vế phải
    
    Returns:
        Vector nghiệm x
    """
    n = len(U)
    x = [0] * n
    
    for i in range(n - 1, -1, -1):
        x[i] = (c[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def gaussian_eliminate(A, b):
    """
    Thực hiện phép biến đổi Gauss để đưa ma trận A về dạng tam giác trên
    
    Args:
        A: Ma trận hệ số
        b: Vector vế phải
    
    Returns:
        Ma trận sau khi khử, nghiệm x, số lần hoán đổi
    """
    M = [row + [b[i]] for i, row in enumerate(A)]
    row = len(M)
    col = len(M[0])
    max_step = min(row, col - 1)
    s = 0
    EPSILON = 1e-12

    for k in range(max_step):
        p = k 
        for i in range(k + 1, row):
            if abs(M[i][k]) > abs(M[p][k]):
                p = i
        if abs(M[p][k]) < EPSILON: 
            raise ValueError("Ma trận suy biến")
        
        if p != k:
            M[k], M[p] = M[p], M[k]
            s += 1
        
        for i in range(k + 1, row):
            l_ik = M[i][k] / M[k][k]
            for j in range(k, col):
                M[i][j] -= l_ik * M[k][j]

    U = [row[:-1] for row in M]
    c = [row[-1] for row in M]
    x = back_substitution(U, c)

    return M, x, s 


    
EPSILON = 1e-15

def is_zero(x):
    return abs(x) < EPSILON

def make_zero(x):
    return 0.0 if is_zero(x) else x
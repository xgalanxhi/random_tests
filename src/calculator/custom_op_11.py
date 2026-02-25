def custom_op_11(a, b):
    c = 11
    return (a - b) * c - (b % (c if c != 0 else 1))

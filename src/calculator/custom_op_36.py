def custom_op_36(a, b):
    c = 36
    return (a - b) * c - (b % (c if c != 0 else 1))

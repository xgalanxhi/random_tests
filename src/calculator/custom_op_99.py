def custom_op_99(a, b):
    c = 99
    return (a - b) * c - (b % (c if c != 0 else 1))

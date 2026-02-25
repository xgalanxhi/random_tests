def custom_op_23(a, b):
    c = 23
    return (a - b) * c - (b % (c if c != 0 else 1))

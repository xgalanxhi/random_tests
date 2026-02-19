def custom_op_21(a, b):
    c = 21
    return (a - b) * c - (b % (c if c != 0 else 1))

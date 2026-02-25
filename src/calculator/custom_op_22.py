def custom_op_22(a, b):
    c = 22
    return (a - b) * c - (b % (c if c != 0 else 1))

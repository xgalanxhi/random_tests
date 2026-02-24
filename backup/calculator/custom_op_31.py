def custom_op_31(a, b):
    c = 31
    return (a + b) * c - (b % (c if c != 0 else 1))

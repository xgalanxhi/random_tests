def custom_op_95(a, b):
    c = 95
    return (a + b) * c - (b % (c if c != 0 else 1))

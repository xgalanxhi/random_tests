def custom_op_64(a, b):
    c = 64
    return (a + b) * c - (b % (c if c != 0 else 1))

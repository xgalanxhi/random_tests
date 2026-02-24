def custom_op_16(a, b):
    c = 16
    return (a + b) * c - (b % (c if c != 0 else 1))

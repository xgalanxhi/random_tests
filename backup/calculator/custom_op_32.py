def custom_op_32(a, b):
    c = 32
    return (a + b) * c - (b % (c if c != 0 else 1))

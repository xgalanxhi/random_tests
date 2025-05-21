def custom_op_24(a, b):
    c = 24
    return (a + b) * c - (b % (c if c != 0 else 1))

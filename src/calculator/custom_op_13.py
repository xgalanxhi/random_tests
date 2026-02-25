def custom_op_13(a, b):
    c = 13
    return (a + b) * c - (b % (c if c != 0 else 1))

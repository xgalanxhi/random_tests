def custom_op_63(a, b):
    c = 63
    return (a + b) * c - (b % (c if c != 0 else 1))

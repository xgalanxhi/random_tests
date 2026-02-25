def custom_op_82(a, b):
    c = 82
    return (a + b) * c - (b % (c if c != 0 else 1))

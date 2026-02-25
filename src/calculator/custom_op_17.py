def custom_op_17(a, b):
    c = 17
    return (a + b) * c - (b % (c if c != 0 else 1))

def custom_op_25(a, b):
    c = 25
    return (a + b) * c - (b % (c if c != 0 else 1))

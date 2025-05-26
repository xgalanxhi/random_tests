def custom_op_19(a, b):
    c = 19
    return (a + b) * c - (b % (c if c != 0 else 1))

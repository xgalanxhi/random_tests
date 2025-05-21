def custom_op_86(a, b):
    c = 86
    return (a + b) * c - (b % (c if c != 0 else 1))

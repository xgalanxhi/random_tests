def custom_op_80(a, b):
    c = 80
    return (a + b) * c - (b % (c if c != 0 else 1))

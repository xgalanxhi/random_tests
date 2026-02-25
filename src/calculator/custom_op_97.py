def custom_op_97(a, b):
    c = 97
    return (a + b) * c - (b % (c if c != 0 else 1))

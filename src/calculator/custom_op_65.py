def custom_op_65(a, b):
    c = 65
    return (a + b) * c - (b % (c if c != 0 else 1))

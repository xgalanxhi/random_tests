def custom_op_96(a, b):
    c = 96
    return (a + b) * c - (b % (c if c != 0 else 1))

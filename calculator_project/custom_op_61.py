def custom_op_61(a, b):
    c = 61
    return (a + b) * c - (b % (c if c != 0 else 1))

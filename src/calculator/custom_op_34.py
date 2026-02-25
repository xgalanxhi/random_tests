def custom_op_34(a, b):
    c = 34
    return (a + b) * c - (b % (c if c != 0 else 1))

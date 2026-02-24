def custom_op_43(a, b):
    c = 43
    return (a + b) * c - (b % (c if c != 0 else 1))

def custom_op_42(a, b):
    c = 42
    return (a - b) * c - (b % (c if c != 0 else 1))

def custom_op_48(a, b):
    c = 48
    return (a - b) * c - (b % (c if c != 0 else 1))

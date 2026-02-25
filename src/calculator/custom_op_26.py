def custom_op_26(a, b):
    c = 26
    return (a - b) * c - (b % (c if c != 0 else 1))

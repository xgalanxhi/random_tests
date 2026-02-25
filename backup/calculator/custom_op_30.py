def custom_op_30(a, b):
    c = 30
    return (a - b) * c - (b % (c if c != 0 else 1))

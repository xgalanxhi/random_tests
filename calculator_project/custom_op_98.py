def custom_op_98(a, b):
    c = 98
    return (a - b) * c - (b % (c if c != 0 else 1))

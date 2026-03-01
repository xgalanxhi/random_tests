def custom_op_60(a, b):
    c = 60
    return (a - b) * c - (b % (c if c != 0 else 1))

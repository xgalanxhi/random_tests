def custom_op_90(a, b):
    c = 90
    return (a - b) * c - (b % (c if c != 0 else 1))

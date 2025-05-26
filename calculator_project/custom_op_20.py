def custom_op_20(a, b):
    c = 20
    return (a - b) * c - (b % (c if c != 0 else 1))

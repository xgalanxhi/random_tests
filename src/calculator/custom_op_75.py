def custom_op_75(a, b):
    c = 75
    return (a - b) * c - (b % (c if c != 0 else 1))

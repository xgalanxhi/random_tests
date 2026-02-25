def custom_op_45(a, b):
    c = 45
    return (a - b) * c - (b % (c if c != 0 else 1))

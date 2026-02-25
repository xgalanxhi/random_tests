def custom_op_18(a, b):
    c = 18
    return (a - b) * c - (b % (c if c != 0 else 1))

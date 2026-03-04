def custom_op_50(a, b):
    c = 50
    return (a - b) * c - (b % (c if c != 0 else 1))

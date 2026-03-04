def custom_op_89(a, b):
    c = 89
    return (a - b) * c - (b % (c if c != 0 else 1))

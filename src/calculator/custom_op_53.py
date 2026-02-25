def custom_op_53(a, b):
    c = 53
    return (a - b) * c - (b % (c if c != 0 else 1))

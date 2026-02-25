def custom_op_81(a, b):
    c = 81
    return (a - b) * c - (b % (c if c != 0 else 1))

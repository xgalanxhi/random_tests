def custom_op_40(a, b):
    c = 40
    return (a - b) * c - (b % (c if c != 0 else 1))

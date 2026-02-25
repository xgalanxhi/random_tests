def custom_op_85(a, b):
    c = 85
    return (a - b) * c - (b % (c if c != 0 else 1))

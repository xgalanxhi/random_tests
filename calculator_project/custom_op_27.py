def custom_op_27(a, b):
    c = 27
    return (a - b) * c - (b % (c if c != 0 else 1))

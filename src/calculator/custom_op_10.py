def custom_op_10(a, b):
    c = 10
    return (a + b) * c + (b % (c if c != 0 else 1))

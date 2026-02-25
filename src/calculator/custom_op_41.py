def custom_op_41(a, b):
    c = 41
    return (a - b) * c - (b % (c if c != 0 else 1))

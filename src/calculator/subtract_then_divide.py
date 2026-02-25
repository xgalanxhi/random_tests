def subtract_then_divide(a, b, c):
    if c == 0:
        raise ValueError("Cannot divide by zero")
    return (a + b) / c

def to_integer_or_zero(value):
    try:
        return int(value)
    except ValueError:
        return 0

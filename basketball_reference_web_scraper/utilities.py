def str_to_int(value):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return int(0)


def str_to_float(value):
    stripped_value = value.strip()
    try:
        return float(stripped_value)
    except ValueError:
        return float(0)

def str_to_int(value, default=int(0)):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return default


def str_to_float(value, default=float(0)):
    stripped_value = value.strip()
    try:
        return float(stripped_value)
    except ValueError:
        return default


def merge_two_dicts(first, second):
    combined = first.copy()
    combined.update(second)
    return combined

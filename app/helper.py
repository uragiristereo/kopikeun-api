from os.path import split


def format_exception(e: BaseException, f: str):
    return f"{type(e).__name__}: {e} in '{split(f)[1]}', line {e.__traceback__.tb_lineno}"


def to_bool(s):
    if s == "true":
        return True
    elif s == "false":
        return False
    else:
        raise ValueError(f"invalid literal for to_bool(): '{s}'")

"""
Функция для конвертации названия класса Python в название таблицы Postgres
"""


def tablename_converter(input: str) -> str:
    chars = []
    for i_char, char in enumerate(input):
        if i_char and char.isupper():
            n_char = i_char + 1
            p_char = i_char - 1
            point = n_char >= len(input) or input[n_char].isupper()
            if point and input[p_char].isupper():
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)

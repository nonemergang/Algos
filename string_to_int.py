def string_to_int(s):
    # Преобразуем строку в число
    result = 0
    for char in s:
        digit = char_to_digit(char)
        result = result * 10 + digit
    return result
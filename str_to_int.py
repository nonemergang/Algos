def str_to_int(s):
    result = 0
    for char in s:
        # Преобразуем каждый символ в цифру
        if char == '0': digit = 0
        elif char == '1': digit = 1
        elif char == '2': digit = 2
        elif char == '3': digit = 3
        elif char == '4': digit = 4
        elif char == '5': digit = 5
        elif char == '6': digit = 6
        elif char == '7': digit = 7
        elif char == '8': digit = 8
        elif char == '9': digit = 9
        else: continue  # пропускаем не-цифры
        result = result * 10 + digit
    return result
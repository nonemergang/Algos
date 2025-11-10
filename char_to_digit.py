def char_to_digit(char):
    # Создаем строку с цифрами для поиска
    digits = "0123456789"
    # Ищем символ в строке цифр
    for i in range(my_len(digits)):
        if digits[i] == char:
            return i
    return 0    
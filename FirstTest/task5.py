def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def long_calc(num1, op, num2):
    # Проверка, что число отрицательно
    if num1[0] == '-':
        sign1 = -1
    else:
        sign1 = 1
    if num2[0] == '-':
        sign2 = -1
    else:
        sign2 = 1

    # берем число без минуса, если он есть
    if sign1 == -1:
        a = num1[1:]
    else:
        a = num1
    if sign2 == -1:
        b = num2[1:]
    else:
        b = num2

    # СЛОЖЕНИЕ
    if op == '+':
        # 1 случай (оба числа положительные) a + b
        if sign1 == 1 and sign2 == 1:
            return add(a,b)

        # 2 случай (оба отрицательные) -a - b
        if sign1 == -1 and sign2 == -1:
            return '-' + add(a,b)

        # 3 случай (a отриц, b полож) -a + b
        if sign1 == -1 and sign2 == 1:
            if bigger(a,b):
                return '-' + subtract(a,b)
            else:
                return subtract(b, a)

        # 4 случай (a полож, b отриц) a + (-b) = a - b
        if sign1 == 1 and sign2 == -1:
            if bigger(b, a):
                return '-' + subtract(b,a)
            else:
                return subtract(a, b)

    # ВЫЧИТАНИЕ
    else:
        # 1 случай a - b
        if sign1 == 1 and sign2 == 1:
            if bigger(a,b):
                return subtract(a, b)
            else:
                return '-' + subtract(b, a)
        # 2 случай -a - (-b) = b - a
        if sign1 == -1 and sign2 == -1:
            if bigger(b, a):
                return subtract(b, a)
            else:
                return '-' + subtract(a, b)

        # 3 случай - a - b = -(a+b)
        if sign1 == -1 and sign2 == 1:
            return '-' + add(a,b)

        # 4 случай a - (-b) = a + b
        if sign1 == 1 and sign2 == -1:
            return add(a,b)


def bigger(a,b):
    if my_len(a) > my_len(b):
        return True
    if my_len(a) < my_len(b):
        return False

    # Если длины одинаковы, то нужно сравнивать посимвольно слева направо
    for i in range(my_len(a)):
        if a[i] > b[i]:
            return True
        elif a[i] < b[i]:
            return False
    return True


def make_same_length(a,b):
    len_a = my_len(a)
    len_b = my_len(b)

    if len_a > len_b:
        zeros_to_add = len_a - len_b
        b = create_zeros(zeros_to_add) + b
    elif len_b > len_a:
        zeros_to_add = len_b - len_a
        a = create_zeros(zeros_to_add) + a

    return a, b


def create_zeros(count):
    result = ""
    for i in range(count):
        result += '0'
    return result


def char_to_digit(char):
    # Создаем строку с цифрами для поиска
    digits = "0123456789"
    # Ищем символ в строке цифр
    for i in range(my_len(digits)):
        if digits[i] == char:
            return i
    return 0


def digit_to_char(digit):
    # Создаем строку с цифрами
    digits = "0123456789"
    # Возвращаем символ по индексу
    return digits[digit]


def reverse_string(s):
    # Создаем пустую строку для результата
    result = ""
    # Идем по строке с конца к началу
    i = my_len(s) - 1
    while i >= 0:
        result += s[i]
        i -= 1
    return result


def list_to_string(lst):
    # Преобразуем список в строку без использования join
    result = ""
    for char in lst:
        result += char
    return result


def add(a,b):
    a,b = make_same_length(a,b)
    n = my_len(a)

    # Список для хранения цифр результата
    result = []

    # Инициализируем перенос в 0
    carry = 0

    # Идем справа налево по цифрам
    i = n - 1
    while i >= 0:
        # Преобразуем символы в цифры
        digit1 = char_to_digit(a[i])
        digit2 = char_to_digit(b[i])

        # Складываем цифры с переносом
        total = digit1 + digit2 + carry

        # Записываем последнюю цифру результата
        result.append(digit_to_char(total % 10))

        # Вычисляем новый перенос
        carry = total // 10

        i -= 1

    # Если остался перенос, добавляем его
    if carry > 0:
        result.append(digit_to_char(carry))

    # Преобразуем список в строку и переворачиваем
    result_str = list_to_string(result)
    return reverse_string(result_str)


def subtract(a,b):
    a,b = make_same_length(a,b)
    n = my_len(a)

    # Список для хранения цифр результата
    result = []

    # Инициализируем заем в 0
    borrow = 0

    # Идем справа налево по цифрам
    i = n - 1
    while i >= 0:
        # Преобразуем символы в цифры
        digit1 = char_to_digit(a[i])
        digit2 = char_to_digit(b[i])

        # Вычитаем предыдущий заем
        current_digit = digit1 - borrow

        # Проверяем, нужно ли занимать
        if current_digit < digit2:
            # Занимаем из старшего разряда
            current_digit += 10
            borrow = 1
        else:
            borrow = 0

        # Вычисляем цифру результата
        result_digit = current_digit - digit2
        result.append(digit_to_char(result_digit))

        i -= 1

    # Преобразуем список в строку и переворачиваем
    result_str = list_to_string(result)
    reversed_result = reverse_string(result_str)

    # Убираем ведущие нули
    return remove_leading_zeros(reversed_result)


def remove_leading_zeros(s):
    # Если строка пустая, возвращаем "0"
    if my_len(s) == 0:
        return "0"

    # Ищем первую ненулевую цифру
    start_index = 0
    while start_index < my_len(s) and s[start_index] == '0':
        start_index += 1

    # Если все цифры были нули, возвращаем "0"
    if start_index == my_len(s):
        return "0"

    # Собираем подстроку без ведущих нулей
    result = ""
    for i in range(start_index, my_len(s)):
        result += s[i]
    return result


num1 = input().strip()
op = input().strip()
num2 = input().strip()
result = long_calc(num1, op, num2)
print(result)
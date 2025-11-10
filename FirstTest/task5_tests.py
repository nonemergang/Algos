import time
import psutil

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

    # Переворачиваем результат и возвращаем
    return reverse_string(''.join(result))


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

    # Переворачиваем результат
    reversed_result = reverse_string(''.join(result))

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

    # Возвращаем подстроку без ведущих нулей
    return s[start_index:]


# Контейнер с 10 тестами
test_cases = [
    ("123", "+", "456", "579", "Сложение положительных чисел"),
    ("999", "+", "1", "1000", "Сложение с переходом через разряд"),
    ("1000", "-", "1", "999", "Вычитание с заемом"),
    ("50", "-", "100", "-50", "Вычитание с отрицательным результатом"),
    ("-123", "+", "456", "333", "Сложение отрицательного и положительного"),
    ("-100", "-", "50", "-150", "Вычитание отрицательных чисел"),
    ("0", "+", "0", "0", "Сложение нулей"),
    ("123", "-", "123", "0", "Вычитание равных чисел"),
    (f"{'9' * 500}", "+", f"{'9' * 500}", "1" + "9" * 499 + "8", "Большие числа (сложение)"),
    (f"{'9' * 1000}", "-", f"{'9' * 1000}", "0", "Большие числа (вычитание)")
]

print("=" * 120)
print("ТЕСТИРОВАНИЕ ПРОГРАММЫ ДЛЯ РАБОТЫ С БОЛЬШИМИ ЧИСЛАМИ")
print("=" * 120)
print(f"{'Описание':<40} | {'Ожидаемый':<25} | {'Полученный':<25} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
print("-" * 120)

total_tests = my_len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (num1, op, num2, expected, description) in enumerate(test_cases, 1):
    # Измеряем время
    start_time = time.time()

    # Выполняем вычисление
    result = long_calc(num1, op, num2)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # в миллисекундах
    execution_times.append(execution_time)

    # Измеряем память
    memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # в МБ
    memory_usages.append(memory_used)

    # Проверка корректности
    is_correct = result == expected
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    # Обрезаем длинные результаты для красоты таблицы
    expected_display = expected if len(expected) <= 20 else expected[:17] + "..."
    result_display = result if len(result) <= 20 else result[:17] + "..."

    print(f"{description:<40} | {expected_display:<25} | {result_display:<25} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.6f}")

print("-" * 120)

# Проверка ограничений
max_time = max(execution_times)
max_memory = max(memory_usages)
time_ok = max_time < 2000
memory_ok = max_memory < 64

print(f"ИТОГО: {passed_tests}/{total_tests} тестов пройдено успешно")
print(f"ОГРАНИЧЕНИЯ: Время < 2000 мс ({'✓' if time_ok else '✗'}) | Память < 64 Мб ({'✓' if memory_ok else '✗'})")
print("=" * 120)

# Дополнительная информация о производительности
print(f"МАКСИМАЛЬНОЕ ВРЕМЯ: {max_time:.3f} мс")
print(f"МАКСИМАЛЬНАЯ ПАМЯТЬ: {max_memory:.6f} Мб")
print(f"СООТВЕТСТВИЕ ОГРАНИЧЕНИЯМ: {'✓ ВЫПОЛНЕНО' if time_ok and memory_ok else '✗ НЕ ВЫПОЛНЕНО'}")
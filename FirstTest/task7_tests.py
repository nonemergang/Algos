import time
import psutil
import os

def my_abs(x):
    return x if x >= 0 else -x

def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def my_split(text, delimiter=" "):
    parts = []
    current = ""
    for char in text:
        if char == delimiter:
            if current != "":
                parts.append(current)
                current = ""
        else:
            current += char
    if current != "":
        parts.append(current)
    return parts

def char_to_digit(char):
    digits = "0123456789"
    for i in range(my_len(digits)):
        if digits[i] == char:
            return i
    return 0

def string_to_int(s):
    result = 0
    for char in s:
        digit = char_to_digit(char)
        result = result * 10 + digit
    return result

def heap_algorithm(n_str, stones_str):
    # Основная логика вашего алгоритма
    n = string_to_int(n_str)

    stones_list = my_split(stones_str)

    stones = []
    total = 0
    for stone_str in stones_list:
        weight = string_to_int(stone_str)
        stones.append(weight)
        total += weight

    can_make = [False] * (total + 1)
    can_make[0] = True

    for weight in stones:
        for s in range(total, weight - 1, -1):
            if can_make[s - weight]:
                can_make[s] = True

    answer = total
    for s in range(total + 1):
        if can_make[s]:
            diff = my_abs(total - 2 * s)
            if diff < answer:
                answer = diff

    return answer

# Контейнер с 10 тестами
test_cases = [
    ("5", "8 9 6 9 8", 4, "Пример из условия 1"),
    ("6", "14 2 12 9 9 8", 2, "Пример из условия 2"),
    ("2", "5 5", 0, "Минимальный случай"),
    ("3", "1 2 4", 1, "Невозможность идеального разбиения"),
    ("4", "1000 2000 3000 4000", 0, "Большие числа"),
    ("5", "1 3 5 7 9", 1, "Все нечетные"),
    ("4", "1 1 1 100", 97, "Один большой камень"),
    ("6", "1 2 3 4 5 6", 1, "Последовательные числа"),
    ("10", "1 1 1 1 1 1 1 1 1 1", 0, "Все единицы"),
    ("4", "1 2 3 4", 0, "Идеальное разбиение")
]

print("=" * 100)
print("ТЕСТИРОВАНИЕ АЛГОРИТМА 'ДВЕ КУЧИ'")
print("=" * 100)
print(f"{'Описание':<35} | {'Ожидаемый':<10} | {'Полученный':<10} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
print("-" * 100)

total_tests = my_len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (n, stones, expected, description) in enumerate(test_cases, 1):
    # Измеряем время выполнения
    start_time = time.time()

    # Выполняем алгоритм
    result = heap_algorithm(n, stones)

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # в миллисекундах
    execution_times.append(execution_time)

    # Измеряем память
    memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # в МБ
    memory_usages.append(memory_used)

    # Проверка корректности
    is_correct = result == expected
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    print(f"{description:<35} | {expected:<10} | {result:<10} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.6f}")

print("-" * 100)

# Проверка ограничений
max_time = max(execution_times)
max_memory = max(memory_usages)
time_ok = max_time < 2000
memory_ok = max_memory < 64

print(f"ИТОГО: {passed_tests}/{total_tests} тестов пройдено успешно")
print(f"ОГРАНИЧЕНИЯ: Время < 2000 мс ({'✓' if time_ok else '✗'}) | Память < 64 Мб ({'✓' if memory_ok else '✗'})")
print("=" * 100)

# Дополнительная информация о производительности
print(f"МАКСИМАЛЬНОЕ ВРЕМЯ: {max_time:.3f} мс")
print(f"МАКСИМАЛЬНАЯ ПАМЯТЬ: {max_memory:.6f} Мб")
print(f"СООТВЕТСТВИЕ ОГРАНИЧЕНИЯМ: {'✓ ВЫПОЛНЕНО' if time_ok and memory_ok else '✗ НЕ ВЫПОЛНЕНО'}")
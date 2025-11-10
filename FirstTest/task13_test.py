import time
import psutil
import os
import random

def find_max_triple_product(arr, n):
    """
    Находит максимальное произведение трех различных элементов массива.
    """
    max1 = max2 = max3 = -10**18
    min1 = min2 = 10**18

    for i in range(n):
        x = arr[i]

        if x > max1:
            max3 = max2
            max2 = max1
            max1 = x
        elif x > max2:
            max3 = max2
            max2 = x
        elif x > max3:
            max3 = x
        if x < min1:
            min2 = min1
            min1 = x
        elif x < min2:
            min2 = x

    candidate1 = max1 * max2 * max3
    candidate2 = min1 * min2 * max1

    if candidate1 > candidate2:
        return candidate1
    else:
        return candidate2

def get_memory_usage():
    """Возвращает использование памяти текущим процессом в МБ"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

# Тестовые случаи
test_cases = [
    # (массив, ожидаемый_результат, описание)
    ([1, 2, 3, 4, 5], 60, "Только положительные числа"),
    ([-10, -10, 5, 2], 500, "С отрицательными числами"),
    ([-5, -4, -3, -2, -1], -6, "Все отрицательные числа"),
    ([-1, 2, 3, -4, 5], 30, "Смешанный случай 1"),
    ([-10, -5, 0, 5, 10], 500, "Смешанный случай 2"),
    ([1, 2, 3], 6, "Минимальный размер"),
    ([1000000, 1000000, 1000000], 1000000000000000000, "Большие числа"),
    ([0, 0, 0, 1, 2], 0, "С нулями"),
    ([5, 5, 5, 2, 3], 125, "Один элемент повторяется"),
    ([1, 2, 3], 6, "Случай из условия"),
    ([-1, -2, -3, -4, -5], -6, "Все отрицательные (граничный)"),
    ([10, 10, 10], 1000, "Три одинаковых положительных"),
    ([-10, -10, -10], -1000, "Три одинаковых отрицательных"),
    ([1, 1, 1, 1, 1], 1, "Все единицы")
]

# Подготовка больших массивов ДО начала тестирования
print("=" * 100)
print("ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ...")
print("=" * 100)

prep_start = time.time()

# Создаем большой массив
print("Создание большого массива (1M элементов)...", end=" ")
large_array = list(range(1000000))
print("✓")

# Создаем случайный массив
print("Генерация случайного массива (500K элементов)...", end=" ")
random_array = [random.randint(-1000000, 1000000) for _ in range(500000)]
print("✓")

# Вычисляем ожидаемый результат для случайного массива
print("Вычисление ожидаемого результата для случайного массива...", end=" ")
max1 = max2 = max3 = -10**18
min1 = min2 = 10**18
for x in random_array:
    if x > max1:
        max3 = max2
        max2 = max1
        max1 = x
    elif x > max2:
        max3 = max2
        max2 = x
    elif x > max3:
        max3 = x
    if x < min1:
        min2 = min1
        min1 = x
    elif x < min2:
        min2 = x
expected_random = max(max1 * max2 * max3, min1 * min2 * max1)
print("✓")

prep_end = time.time()
prep_time = prep_end - prep_start

print(f"\nПодготовка данных завершена за {prep_time:.2f} секунд")
print("=" * 100)

# ТЕПЕРЬ добавляем большие массивы в test_cases
# Для массива [0, 1, 2, ..., 999999] максимальное произведение: 999999 * 999998 * 999997
expected_large = 999999 * 999998 * 999997
test_cases.append((large_array, expected_large, "Большой массив (1M элементов)"))
test_cases.append((random_array, expected_random, "Случайный массив (500K элементов)"))

print("\nТЕСТИРОВАНИЕ АЛГОРИТМА ПОИСКА МАКСИМАЛЬНОГО ПРОИЗВЕДЕНИЯ ТРЕХ ЭЛЕМЕНТОВ")
print("=" * 100)
print(f"{'Описание':<40} | {'Ожидаемый':<20} | {'Полученный':<20} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
print("-" * 100)

total_tests = len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (arr, expected, description) in enumerate(test_cases, 1):
    # Измеряем время выполнения
    start_memory = get_memory_usage()
    start_time = time.time()

    # Выполняем алгоритм
    result = find_max_triple_product(arr, len(arr))

    end_time = time.time()
    end_memory = get_memory_usage()

    execution_time = (end_time - start_time) * 1000  # в миллисекундах
    memory_used = end_memory - start_memory

    execution_times.append(execution_time)
    memory_usages.append(memory_used if memory_used > 0 else 0.000001)

    # Проверка корректности
    is_correct = result == expected
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    # Форматируем большие числа для отображения
    expected_display = str(expected) if len(str(expected)) <= 15 else f"{expected:.2e}"
    result_display = str(result) if len(str(result)) <= 15 else f"{result:.2e}"

    print(f"{description:<40} | {expected_display:<20} | {result_display:<20} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.6f}")

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

# Статистика по времени
avg_time = sum(execution_times) / len(execution_times)
print(f"\nСТАТИСТИКА:")
print(f"Среднее время: {avg_time:.3f} мс")
print(f"Минимальное время: {min(execution_times):.3f} мс")
print(f"Максимальное время: {max_time:.3f} мс")
print(f"\n(Время подготовки данных: {prep_time:.2f} секунд - не учитывается в тестах)")
print("=" * 100)
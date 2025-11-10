import datetime
import sys

def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def symmetric_difference_original(numbers_str):
    numbers = numbers_str.split()

    zero_count = 0
    a = []
    b = []

    for num in numbers:
        if num == '0':
            zero_count += 1
            continue
        if zero_count == 0:
            a.append(int(num))
        elif zero_count == 1:
            b.append(int(num))

    result = []
    for x in a:
        if x not in b:
            result.append(x)
    for x in b:
        if x not in a:
            result.append(x)

    def sort_bubble(a):
        sorted_flag = False
        n = my_len(a)
        while not sorted_flag:
            sorted_flag = True
            for i in range(n - 1):
                if a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
                    sorted_flag = False

    sort_bubble(result)

    # Подсчет памяти
    memory_containers = sys.getsizeof(a) + sys.getsizeof(b) + sys.getsizeof(result)
    memory_elements = (sum(sys.getsizeof(x) for x in a) +
                       sum(sys.getsizeof(x) for x in b) +
                       sum(sys.getsizeof(x) for x in result))

    total_memory = (memory_containers + memory_elements) / 1024 / 1024  # в Мб

    if result:
        return ' '.join(str(x) for x in result), total_memory
    else:
        return '0', total_memory

# 10 тестовых случаев
test_cases = [
    # (входные данные, описание, ожидаемый результат)
    ("1 2 3 4 5 0 1 7 5 8 0", "Пример из условия 1", "2 3 4 7 8"),
    ("1 2 6 8 7 3 0 4 1 6 2 3 9 0", "Пример из условия 2", "4 7 8 9"),
    ("0 0", "Пустые множества", "0"),
    ("1 2 3 4 5 0 0", "Только множество A", "1 2 3 4 5"),
    ("0 6 7 8 9 10 0", "Только множество B", "6 7 8 9 10"),
    ("10 20 30 40 50 0 10 20 30 40 50 0", "Полностью совпадающие", "0"),
    ("1 3 5 7 9 0 2 4 6 8 10 0", "Непересекающиеся", "1 2 3 4 5 6 7 8 9 10"),
    ("19995 19996 19997 19998 19999 20000 0 19997 19999 0", "Граничные значения", "19995 19996 19998 20000"),
    ("1 2 3 4 5 6 7 8 9 10 0 6 7 8 9 10 11 12 13 14 15 0", "Частичное пересечение", "1 2 3 4 5 11 12 13 14 15"),
    ("1 1 2 2 3 3 0 2 2 4 4 0", "С дубликатами", "1 3 4")
]

print("=" * 100)
print("ТЕСТИРОВАНИЕ ПРОГРАММЫ СИММЕТРИЧЕСКОЙ РАЗНОСТИ")
print("=" * 100)
print(f"{'Описание':<25} | {'Ожидаемый':<20} | {'Полученный':<20} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<12}")
print("-" * 100)

total_tests = my_len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (test_input, description, expected) in enumerate(test_cases, 1):
    start_time = datetime.datetime.now()
    result, memory_used = symmetric_difference_original(test_input)
    end_time = datetime.datetime.now()

    execution_time = (end_time - start_time).total_seconds() * 1000
    execution_times.append(execution_time)
    memory_usages.append(memory_used)

    # Проверка корректности
    is_correct = result == expected
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    # Обрезаем длинные результаты для красоты таблицы
    expected_display = expected if len(expected) <= 18 else expected[:15] + "..."
    result_display = result if len(result) <= 18 else result[:15] + "..."

    print(f"{description:<25} | {expected_display:<20} | {result_display:<20} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<12.6f}")

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
import time
import psutil
import os

def my_split(text, delimiter=" "):
    parts = []
    current = ""
    for char in text:
        if char == delimiter:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts

def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def better(a, b):
    """
    Определяет, должен ли участник a быть ВЫШЕ участника b в рейтинге
    Возвращает True если a лучше b, False в противном случае
    """
    # 1. Сравниваем по количеству решённых задач
    if a[1] != b[1]:
        return a[1] > b[1]
    # 2. Если задачи равны, сравниваем по штрафу
    if a[2] != b[2]:
        return a[2] < b[2]
    # 3. Если и штрафы равны, сравниваем логины лексикографически
    return a[0] < b[0]


def sift_down(arr, n, i):
    """
   Просеивание элемента вниз в куче
   arr - массив участников
   n - текущий размер кучи (сколько элементов сейчас в куче)
   i - индекс элемента, который нужно просеять вниз
   """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Проверяем, существует ли левый потомок и лучше ли он текущего элемента
    if left < n and better(arr[left], arr[largest]):
        largest = left

    # Проверяем, существует ли правый потомок и лучше ли он текущего лучшего
    if right < n and better(arr[right], arr[largest]):
        largest = right

    # Если нашли потомка, который лучше текущего элемента
    if largest != i:
        # Меняем местами текущий элемент с лучшим потомком
        arr[i], arr[largest] = arr[largest], arr[i]
        # Рекурсивно продолжаем для нового положения элемента
        sift_down(arr, n, largest)


def build_heap(arr):
    n = my_len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)


def heap_sort(arr):
    n = my_len(arr)
    # Превращаем массив в кучу
    build_heap(arr)

    # Последовательно извлекаем элементы из кучи
    for i in range(n-1, 0, -1):
        # Меняем местами корень (максимальный элемент) с последним элементом кучи
        # Теперь максимальный элемент находится на своём окончательном месте в конце массива
        arr[0], arr[i] = arr[i], arr[0]
        # Восстанавливаем свойства кучи для оставшейся части (размер i)
        # Просеиваем новый корень вниз, но только до i-го элемента
        sift_down(arr, i, 0)

# Тестовые случаи
test_cases = [
    # (данные, ожидаемый_результат, описание)
    (
        ["alla 4 100", "gena 6 1000", "gosha 2 90", "rita 2 90", "timofey 4 80"],
        ["gena", "timofey", "alla", "gosha", "rita"],
        "Базовый пример из условия"
    ),
    (
        ["user1 10 100", "user2 10 50", "user3 10 200"],
        ["user2", "user1", "user3"],
        "Одинаковые задачи, разные штрафы"
    ),
    (
        ["gamma 5 100", "alpha 5 100", "beta 5 100"],
        ["alpha", "beta", "gamma"],
        "Все параметры одинаковы, сортировка по логинам"
    ),
    (
        ["user3 0 0", "user1 0 0", "user2 0 0"],
        ["user1", "user2", "user3"],
        "Все параметры нулевые"
    ),
    (
        ["max1 1000000000 1000000000", "max2 1000000000 999999999", "max3 999999999 1000000000"],
        ["max2", "max1", "max3"],
        "Граничные значения (10^9)"
    ),
    (
        ["single 100 50"],
        ["single"],
        "Всего один участник"
    ),
    (
        ["user2 50 100", "user1 100 50"],
        ["user1", "user2"],
        "Два участника, обратный порядок"
    ),
    (
        ["abcdefghijklmnopqrst 10 50", "abcdefghijklmnopqrsu 10 50", "abcdefghijklmnopqrss 10 50"],
        ["abcdefghijklmnopqrst", "abcdefghijklmnopqrss", "abcdefghijklmnopqrsu"],
        "Длинные логины (20 символов)"
    ),
    (
        ["a 10 100", "b 10 50", "c 5 10", "d 10 50", "e 5 20"],
        ["b", "d", "a", "c", "e"],
        "Сложная комбинация критериев"
    ),
    (
        ["zzz 100 100", "aaa 100 100", "mmm 100 100"],
        ["aaa", "mmm", "zzz"],
        "Все одинаковые, только логины разные"
    ),
    (
        ["low 10 100", "high 50 100", "mid 30 100"],
        ["high", "mid", "low"],
        "Штрафы одинаковые, сортировка по задачам"
    ),
    (
        ["user5 1 500", "user4 2 400", "user3 3 300", "user2 4 200", "user1 5 100"],
        ["user1", "user2", "user3", "user4", "user5"],
        "Данные в обратном порядке"
    ),
    (
        ["best 100 10", "good 90 20", "average 80 30", "poor 70 40"],
        ["best", "good", "average", "poor"],
        "Данные уже отсортированы"
    ),
    (
        ["x 0 100", "y 0 50", "z 0 200"],
        ["y", "x", "z"],
        "Нет решенных задач, сортировка по штрафу"
    ),
    (
        ["first 5 100", "second 5 100", "third 5 100", "fourth 5 100", "fifth 5 100"],
        ["fifth", "first", "fourth", "second", "third"],
        "Много участников с одинаковыми параметрами"
    )
]

def get_memory_usage():
    """Возвращает использование памяти текущим процессом в МБ"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

print("=" * 100)
print("ТЕСТИРОВАНИЕ АЛГОРИТМА СОРТИРОВКИ УЧАСТНИКОВ")
print("=" * 100)
print(f"{'Описание':<50} | {'Ожидаемый':<25} | {'Полученный':<25} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
print("-" * 100)

total_tests = len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (data, expected, description) in enumerate(test_cases, 1):
    # Подготовка данных
    participants = []
    for line in data:
        parts = my_split(line)
        login = parts[0]
        solved = int(parts[1])
        penalty = int(parts[2])
        participants.append((login, solved, penalty))

    # Измеряем время выполнения
    start_memory = get_memory_usage()
    start_time = time.time()

    # Выполняем сортировку
    heap_sort(participants)

    end_time = time.time()
    end_memory = get_memory_usage()

    execution_time = (end_time - start_time) * 1000  # в миллисекундах
    memory_used = end_memory - start_memory

    execution_times.append(execution_time)
    memory_usages.append(memory_used if memory_used > 0 else 0.000001)

    # Получаем результат (разворачиваем для показа от лучшего к худшему)
    result_logins = [p[0] for p in participants[::-1]]

    # Проверка корректности
    is_correct = result_logins == expected
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    # Форматируем вывод для длинных списков
    expected_display = str(expected) if len(str(expected)) <= 20 else f"{expected[:3]}...({len(expected)} эл.)"
    result_display = str(result_logins) if len(str(result_logins)) <= 20 else f"{result_logins[:3]}...({len(result_logins)} эл.)"

    print(f"{description:<50} | {expected_display:<25} | {result_display:<25} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.6f}")

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
min_time = min(execution_times)
print(f"\nСТАТИСТИКА:")
print(f"Среднее время: {avg_time:.3f} мс")
print(f"Минимальное время: {min_time:.3f} мс")
print(f"Максимальное время: {max_time:.3f} мс")

# Информация о тестах
print(f"\nИНФОРМАЦИЯ О ТЕСТАХ:")
print(f"Всего тестов: {total_tests}")
print(f"Максимальное количество участников в тесте: {max(len(tc[0]) for tc in test_cases)}")
print(f"Минимальное количество участников в тесте: {min(len(tc[0]) for tc in test_cases)}")
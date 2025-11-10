import time
import psutil
import os

def broken_search(nums, target) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # в МБ

# Тестовые случаи
test_cases = [
    # (массив, целевое_число, ожидаемый_результат, описание)
    ([19, 21, 100, 101, 1, 4, 5, 7, 12], 5, 6, "Базовый случай из условия"),
    ([5, 1], 1, 1, "Минимальный сдвиг"),
    ([1], 1, 0, "Один элемент - найден"),
    ([1], 2, -1, "Один элемент - не найден"),
    ([], 5, -1, "Пустой массив"),
    ([1, 2, 3, 4, 5, 6, 7], 4, 3, "Полностью отсортированный массив"),
    ([2, 3, 4, 5, 6, 7, 1], 1, 6, "Сдвиг в начале"),
    ([7, 1, 2, 3, 4, 5, 6], 7, 0, "Сдвиг в конце"),
    ([4, 5, 6, 7, 1, 2, 3], 8, -1, "Элемент не существует"),
    ([4, 5, 6, 7, 1, 2, 3], 1, 4, "Граничный случай - минимальный элемент"),
    ([4, 5, 6, 7, 1, 2, 3], 7, 3, "Граничный случай - максимальный элемент"),
    ([3, 4, 5, 1, 2], 3, 0, "Поиск первого элемента"),
    ([3, 4, 5, 1, 2], 2, 4, "Поиск последнего элемента"),
    ([100, 101, 102, 97, 98, 99], 97, 3, "Все элементы уникальные"),
    ([9998, 9999, 10000, 1, 2], 10000, 2, "Максимальные значения элементов"),
    ([2, 3, 1], 1, 2, "Минимальные значения элементов"),
    ([6, 7, 8, 9, 1, 2, 3, 4, 5], 9, 3, "Точка сдвига в середине"),
    ([7, 8, 9, 1, 2, 3, 4, 5, 6], 3, 5, "Элемент в правой отсортированной части")
]

# Добавляем большие массивы
large_arr = list(range(500, 1000)) + list(range(0, 500))
test_cases.append((large_arr, 750, 250, "Большой массив (1000 элементов)"))

very_large_arr = list(range(5000, 10000)) + list(range(0, 5000))
test_cases.append((very_large_arr, 9999, 4999, "Очень большой массив (10000 элементов)"))

print("=" * 100)
print("ТЕСТИРОВАНИЕ АЛГОРИТМА ПОИСКА В СЛОМАННОМ МАССИВЕ")
print("=" * 100)
print(f"{'Описание':<45} | {'Ожидаемый':<10} | {'Полученный':<10} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
print("-" * 100)

total_tests = len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (arr, target, expected, description) in enumerate(test_cases, 1):
    # Измеряем время выполнения
    start_memory = get_memory_usage()
    start_time = time.time()

    # Выполняем алгоритм
    result = broken_search(arr, target)

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

    # Форматируем вывод массива для длинных случаев
    arr_display = str(arr) if len(str(arr)) <= 30 else f"[...] (длина: {len(arr)})"

    print(f"{description:<45} | {expected:<10} | {result:<10} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.6f}")

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
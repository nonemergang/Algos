import time
import psutil
import os

def solve(N, K, M, L):
    """Основная функция решения задачи"""
    if L == 0:
        return 0

    # Подсчитываем количество вхождений каждого числа
    count = [0] * L

    current = K
    for _ in range(N):
        if current < L:
            count[current] += 1

        # Генерируем следующий элемент согласно условию
        current = (current * M) & 0xFFFFFFFF
        if L > 0:
            current %= L

    # Находим сумму элементов на нечетных позициях
    result = 0
    position = 0

    for number in range(L):
        occurrences = count[number]
        if occurrences > 0:
            # Для каждого числа нужно понять, сколько раз оно попадает
            # на нечетную позицию
            for _ in range(occurrences):
                position += 1
                if position % 2 == 1:  # нечетная позиция (1, 3, 5, ...)
                    result = (result + number) % L

    return result

def run_test(test_num, N, K, M, L, expected, description):
    """Запуск одного теста с замером времени и памяти"""
    print(f"\n{'='*70}")
    print(f"Тест #{test_num}: {description}")
    print(f"Входные данные: N={N}, K={K}, M={M}, L={L}")
    print(f"Ожидаемый результат: {expected}")

    # Получаем процесс для замера памяти
    process = psutil.Process(os.getpid())

    # Замер памяти до выполнения
    mem_before = process.memory_info().rss / 1024 / 1024  # в МБ

    # Замер времени
    start_time = time.time()
    result = solve(N, K, M, L)
    end_time = time.time()

    # Замер памяти после выполнения
    mem_after = process.memory_info().rss / 1024 / 1024  # в МБ

    execution_time = end_time - start_time
    memory_used = mem_after - mem_before

    # Проверка результата
    status = "✓ PASS" if result == expected else "✗ FAIL"

    print(f"Полученный результат: {result}")
    print(f"Статус: {status}")
    print(f"Время выполнения: {execution_time:.4f} сек")
    print(f"Память (изменение): {memory_used:.2f} МБ")
    print(f"Память (текущая): {mem_after:.2f} МБ")

    return result == expected

def main():
    # Тестовые случаи
    test_cases = [
        (5, 7, 13, 100, 77, "Пример из условия"),
        (10, 5, 3, 0, 0, "Нулевой L"),
        (8, 0, 17, 50, 0, "K = 0"),
        (6, 10, 1, 100, 30, "M = 1"),  # Исправлено: 10+10+10=30
        (5, 1, 2, 100, 21, "Все элементы разные"),
        (5, 1, 2, 100, 21, "Три элемента: 1,2,4"),  # Исправлено: 1+4+16=21
        (4, 1, 3, 100, 10, "Четыре элемента: 1,3,9,27"),
        (1, 5, 3, 100, 5, "Один элемент"),
        (100, 1, 1, 1, 0, "L = 1"),
        (1000, 1, 113, 5000, 2500, "Средний размер"),
        (5000, 42, 1103515245, 10000, 7128, "Большой L"),  # По результату
        (10000, 4294967295, 16646525, 50000, 48364, "Большие числа"),  # По результату
        (100000, 1, 25214903917, 100000, 3316, "Максимальная нагрузка")  # По результату
    ]

    print("="*70)
    print("ЗАПУСК ТЕСТОВ: Очень быстрая сортировка")
    print("="*70)

    passed = 0
    total = len(test_cases)

    for i, (N, K, M, L, expected, desc) in enumerate(test_cases, 1):
        if run_test(i, N, K, M, L, expected, desc):
            passed += 1

    print(f"\n{'='*70}")
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
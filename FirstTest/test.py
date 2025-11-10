def solve_with_debug(N, K, M, L):
    """Решение с подробной отладкой"""
    print(f"Входные данные: N={N}, K={K}, M={M}, L={L}")

    if L == 0:
        print("L=0, результат: 0")
        return 0

    # Генерируем последовательность и выводим её
    sequence = []
    current = K
    for i in range(N):
        sequence.append(current)
        # Генерируем следующий элемент согласно условию
        current = (current * M) & 0xFFFFFFFF
        if L > 0:
            current %= L

    print(f"Сгенерированная последовательность: {sequence}")

    # Сортируем
    sorted_seq = sorted(sequence)
    print(f"Отсортированная последовательность: {sorted_seq}")

    # Находим элементы на нечетных позициях (1, 3, 5, ...)
    odd_position_elements = []
    for i in range(len(sorted_seq)):
        if (i + 1) % 2 == 1:  # позиции 1, 3, 5 (индексы 0, 2, 4)
            odd_position_elements.append(sorted_seq[i])

    print(f"Элементы на нечётных позициях (1,3,5,...): {odd_position_elements}")

    # Считаем сумму
    total = sum(odd_position_elements)
    result = total % L

    print(f"Сумма: {total}")
    print(f"Результат (сумма % L): {result}")

    return result

def solve_optimized(N, K, M, L):
    """Оптимизированное решение (текущее)"""
    if L == 0:
        return 0

    # Подсчитываем количество вхождений каждого числа
    count = [0] * L

    current = K
    for _ in range(N):
        if current < L:
            count[current] += 1

        current = (current * M) & 0xFFFFFFFF
        if L > 0:
            current %= L

    # Находим сумму элементов на нечетных позициях
    result = 0
    position = 0

    for number in range(L):
        occurrences = count[number]
        if occurrences > 0:
            for _ in range(occurrences):
                position += 1
                if position % 2 == 1:
                    result = (result + number) % L

    return result

# Тест 1: Пример из условия
print("="*70)
print("ТЕСТ 1: Пример из условия")
print("="*70)
result1 = solve_with_debug(5, 7, 13, 100)
result2 = solve_optimized(5, 7, 13, 100)
print(f"\nРезультат (с debug): {result1}")
print(f"Результат (оптимизированный): {result2}")
print(f"Совпадают: {result1 == result2}")

# Тест 2: M = 1
print("\n" + "="*70)
print("ТЕСТ 2: M = 1 (все элементы одинаковые)")
print("="*70)
result1 = solve_with_debug(6, 10, 1, 100)
result2 = solve_optimized(6, 10, 1, 100)
print(f"\nРезультат (с debug): {result1}")
print(f"Результат (оптимизированный): {result2}")
print(f"Совпадают: {result1 == result2}")

# Тест 3: Маленькая последовательность
print("\n" + "="*70)
print("ТЕСТ 3: Маленькая последовательность")
print("="*70)
result1 = solve_with_debug(4, 1, 3, 100)
result2 = solve_optimized(4, 1, 3, 100)
print(f"\nРезультат (с debug): {result1}")
print(f"Результат (оптимизированный): {result2}")
print(f"Совпадают: {result1 == result2}")

# Тест 4: K=1, M=2
print("\n" + "="*70)
print("ТЕСТ 4: K=1, M=2")
print("="*70)
result1 = solve_with_debug(5, 1, 2, 100)
result2 = solve_optimized(5, 1, 2, 100)
print(f"\nРезультат (с debug): {result1}")
print(f"Результат (оптимизированный): {result2}")
print(f"Совпадают: {result1 == result2}")
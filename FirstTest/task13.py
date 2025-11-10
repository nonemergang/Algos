
def find_max_triple_product(arr, n):
    # Инициализируем 3 максимальных значения
    max1 = max2 = max3 = -10**18

    # Инициализируем 2 минимальных значения
    min1 = min2 = 10**18

    # Проходим по элементам массива
    for i in range(n):
        x = arr[i]
        # Если текущий элемент больше самого большого найденного,
        # сдвигаем все максимумы вправо и обновляем max1
        if x > max1:
            max3 = max2
            max2 = max1
            max1 = x
        # Если текущий элемент больше второго максимума,
        # но не больше первого
        elif x > max2:
            max3 = max2
            max2 = x
        elif x > max3:
            # Если текущий элемент больше третьего максимума,
            # но не больше первых двух
            max3 = x

        # Обновление двух минимальных значений
        if x < min1:
            min2 = min1
            min1 = x
        elif x < min2:
            min2 = x

    # Вычисляем два возможных кандидата на максимальное произведение
    candidate1 = max1*max2*max3
    candidate2 = min1*min2*max1

    if candidate1 > candidate2:
        return candidate1
    else:
        return candidate2


def main():
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    result = find_max_triple_product(arr, n)
    print(result)



if __name__ == "__main__":
    main()

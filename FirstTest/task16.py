def main():
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    M = int(data[2])
    L = int(data[3])

    if L == 0:
        print(0)
        return

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
                if position % 2 == 1:  # нечетная позиция
                    result = (result + number) % L

    print(result)

if __name__ == "__main__":
    main()
def main():
    # Считываем первую строку и разбиваем на элементы
    first_line = input().split()
    # Первое число - количество множеств
    n = int(first_line[0])
    # Второе число - количество элементов в каждом множестве
    m = int(first_line[1])

    # Список для хранения всех множеств
    sets = []

    # Читаем каждое множество
    for i in range(n):
        # Считываем строку с элементами множества
        line = input().split()

        # Создаем хеш-таблицу для текущего множества
        hash_table = {}

        # Заполняем хеш-таблицу элементами множества
        for j in range(m):
            # Берем j-й элемент как строку
            num_str = line[j]
            # Преобразуем в число
            num = int(num_str)
            # Добавляем в хеш-таблицу (значение True - просто маркер наличия элемента)
            hash_table[num] = True

        # Добавляем готовое множество в список
        sets.append(hash_table)

    # Переменная для хранения максимального размера пересечения
    max_intersection = 0

    # Перебираем все пары множеств (i, j) где i < j
    for i in range(n):
        # Берем первое множество пары
        set1 = sets[i]

        # Перебираем все множества после i-го
        for j in range(i + 1, n):
            # Берем второе множество пары
            set2 = sets[j]
            # Счетчик общих элементов
            common_count = 0

            # итерируемся по меньшему множеству для экономии времени
            if len(set1) < len(set2):
                # Если set1 меньше, проверяем его элементы на наличие в set2
                for element in set1:
                    if element in set2:
                        common_count += 1
            else:
                # Если set2 меньше или равен, проверяем его элементы на наличие в set1
                for element in set2:
                    if element in set1:
                        common_count += 1

            # Обновляем максимальное пересечение, если нашли больше
            if common_count > max_intersection:
                max_intersection = common_count

    # максимальный размер пересечения
    print(max_intersection)

if __name__ == '__main__':
    main()
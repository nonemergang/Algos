def main():
    # Чтение входного файла
    input_file = open('../INPUT.txt', 'r')
    all_data = []

    # Читаем все числа
    for line in input_file:
        parts = line.split()
        for part in parts:
            all_data.append(int(part))
    input_file.close()

    pos = 0
    K = all_data[pos]  # количество тестов
    pos += 1
    results = []

    MAX_T = 10000

    for test_case in range(K):
        N = all_data[pos]  # количество охранников
        pos += 1
        guards = []

        # Читаем охранников
        for i in range(N):
            A = all_data[pos]
            pos += 1
            B = all_data[pos]
            pos += 1
            guards.append((A, B))

        # Шаг 1: Проверяем полное покрытие
        full_cover = True
        for t in range(MAX_T):
            found = False
            # Проверяем всех охранников для момента t
            for i in range(N):
                A = guards[i][0]
                B = guards[i][1]
                if A <= t < B:  # охранник работает в момент t
                    found = True
                    break
            if not found:
                full_cover = False
                break

        if not full_cover:
            results.append("Wrong Answer")
            continue

        # Шаг 2: Проверяем минимальность
        all_necessary = True

        for i in range(N):  # проверяем каждого охранника
            necessary = False

            # Проверяем все моменты его смены
            A = guards[i][0]
            B = guards[i][1]
            for t in range(A, B):
                if t >= MAX_T:
                    break

                # Проверяем, единственный ли он в момент t
                only_one = True
                for j in range(N):
                    if j == i:  # пропускаем самого себя
                        continue
                    Aj = guards[j][0]
                    Bj = guards[j][1]
                    if Aj <= t < Bj:  # другой охранник тоже работает
                        only_one = False
                        break

                if only_one:
                    necessary = True
                    break

            if not necessary:
                all_necessary = False
                break

        if all_necessary:
            results.append("Accepted")
        else:
            results.append("Wrong Answer")

    # Запись результата
    output_file = open('OUTPUT.TXT', 'w')
    for res in results:
        output_file.write(res + '\n')
    output_file.close()

if __name__ == "__main__":
    main()
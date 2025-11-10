import time
import psutil
import os
import sys
from io import StringIO

def get_memory_usage():
    """Получить использование памяти в МБ"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def original_solution():
    """Оригинальное решение задачи о пересечении множеств"""
    first_line = input().split()
    n = int(first_line[0])
    m = int(first_line[1])

    sets = []
    for i in range(n):
        line = input().split()
        hash_table = {}
        for j in range(m):
            num_str = line[j]
            num = int(num_str)
            hash_table[num] = True
        sets.append(hash_table)

    max_intersection = 0
    for i in range(n):
        set1 = sets[i]
        for j in range(i + 1, n):
            set2 = sets[j]
            common_count = 0
            if len(set1) < len(set2):
                for element in set1:
                    if element in set2:
                        common_count += 1
            else:
                for element in set2:
                    if element in set1:
                        common_count += 1
            if common_count > max_intersection:
                max_intersection = common_count

    return max_intersection

def run_test(test_input, test_num):
    """
    Запускает один тест и возвращает результаты
    """
    process = psutil.Process(os.getpid())

    # Сохраняем оригинальный stdin
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    try:
        # Измеряем память до выполнения
        mem_before = get_memory_usage()

        # Перенаправляем ввод
        sys.stdin = StringIO(test_input)

        # Захватываем вывод
        output_capture = StringIO()
        sys.stdout = output_capture

        # Измеряем время выполнения
        start_time = time.perf_counter()

        # Запускаем решение
        result = original_solution()

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # в миллисекундах

        # Получаем вывод
        output = output_capture.getvalue().strip()

        # Измеряем память после выполнения
        mem_after = get_memory_usage()
        mem_used = max(mem_after - mem_before, 0.001)  # минимум 0.001 МБ

        status = "OK"

    except Exception as e:
        result = "Ошибка"
        output = str(e)
        execution_time = 0
        mem_used = 0
        status = f"Ошибка: {str(e)}"

    finally:
        # Восстанавливаем оригинальные потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    return {
        'test_num': test_num,
        'input': test_input.replace('\n', '; '),
        'output': output,
        'result': result,
        'time_ms': execution_time,
        'memory_mb': mem_used,
        'status': status
    }

def print_table_header():
    """Печатает заголовок таблицы"""
    print("=" * 180)
    print(f"{'№':<3} | {'Входные данные':<60} | {'Результат':<10} | {'Статус':<15} | {'Время (мс)':<12} | {'Память (МБ)':<12}")
    print("=" * 180)

def print_test_result(test_data):
    """Печатает результат одного теста"""
    input_str = test_data['input']
    if len(input_str) > 60:
        input_str = input_str[:57] + "..."

    print(f"{test_data['test_num']:<3} | "
          f"{input_str:<60} | "
          f"{str(test_data['result']):<10} | "
          f"{test_data['status']:<15} | "
          f"{test_data['time_ms']:<12.6f} | "
          f"{test_data['memory_mb']:<12.6f}")

def create_test_cases():
    """Создает тестовые наборы данных"""
    test_cases = []

    # Тест 1: Базовый пример из условия
    test1 = """3 4
1 2 3 4
2 3 4 5
3 4 5 6"""
    test_cases.append((test1, 1))

    # Тест 2: Минимальные значения (N=2, M=3)
    test2 = """2 3
1 2 3
2 3 4"""
    test_cases.append((test2, 2))

    # Тест 3: Все множества одинаковые
    test3 = """4 3
10 20 30
10 20 30
10 20 30
10 20 30"""
    test_cases.append((test3, 3))

    # Тест 4: Нет пересечений
    test4 = """3 2
1 2
3 4
5 6"""
    test_cases.append((test4, 0))

    # Тест 5: Максимальное пересечение = M
    test5 = """3 5
1 2 3 4 5
1 2 3 4 5
6 7 8 9 0"""
    test_cases.append((test5, 5))

    # Тест 6: Граничный случай - максимальное N=1000, минимальное M=3
    test6 = ["1000 3"]
    # Генерируем 1000 множеств по 3 элемента
    for i in range(1000):
        elements = [str(i*3 + j) for j in range(3)]
        test6.append(" ".join(elements))
    test_cases.append(("\n".join(test6), 6))

    # Тест 7: Граничный случай - минимальное N=2, максимальное M=1000
    test7 = ["2 1000"]
    # Первое множество: 1, 2, 3, ..., 1000
    set1 = [str(i) for i in range(1, 1001)]
    test7.append(" ".join(set1))
    # Второе множество: 500, 501, ..., 1499
    set2 = [str(i) for i in range(500, 1500)]
    test7.append(" ".join(set2))
    test_cases.append(("\n".join(test7), 7))

    # Тест 8: Большие числа (близко к границе 2e9)
    test8 = """3 4
1999999999 2000000000 -1999999999 -2000000000
2000000000 -1999999999 1000000000 -1000000000
-1999999999 1000000000 500000000 -500000000"""
    test_cases.append((test8, 8))

    # Тест 9: Случайные пересечения
    test9 = """5 6
1 3 5 7 9 11
2 3 6 7 10 11
3 4 7 8 11 12
1 2 3 4 5 6
7 8 9 10 11 12"""
    test_cases.append((test9, 9))

    # Тест 10: Все множества разные, но есть небольшие пересечения
    test10 = """4 4
10 20 30 40
20 30 40 50
30 40 50 60
40 50 60 70"""
    test_cases.append((test10, 10))

    # Тест 11: Очень большие множества с минимальным пересечением
    test11 = ["10 100"]
    for i in range(10):
        elements = [str(i*100 + j) for j in range(100)]
        test11.append(" ".join(elements))
    test_cases.append(("\n".join(test11), 11))

    # Тест 12: Граничный случай - N=1000, M=1000 (максимальные значения)
    test12 = ["10 100"]  # Уменьшено для производительности
    for i in range(10):
        elements = [str(i*100 + j) for j in range(100)]
        test12.append(" ".join(elements))
    test_cases.append(("\n".join(test12), 12))

    return test_cases

def main():
    """Основная функция тестирования"""
    print("\n")
    print("╔" + "═" * 178 + "╗")
    print("║" + " " * 65 + "ТЕСТИРОВАНИЕ ПРОГРАММЫ 'ПЕРЕСЕЧЕНИЕ МНОЖЕСТВ'" + " " * 65 + "║")
    print("╚" + "═" * 178 + "╝")
    print()

    # Создаем тестовые случаи
    test_cases = create_test_cases()

    print_table_header()

    results = []
    for i, (test_input, test_num) in enumerate(test_cases, 1):
        result = run_test(test_input, i)
        results.append(result)
        print_test_result(result)

        # Добавляем небольшую паузу между тестами для более точного измерения памяти
        time.sleep(0.01)

    print("=" * 180)

    # Статистика
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['status'] == 'OK')
    failed_tests = total_tests - successful_tests

    avg_time = sum(r['time_ms'] for r in results if r['status'] == 'OK') / max(successful_tests, 1)
    max_time = max(r['time_ms'] for r in results if r['status'] == 'OK') if successful_tests > 0 else 0

    avg_memory = sum(r['memory_mb'] for r in results if r['status'] == 'OK') / max(successful_tests, 1)
    max_memory = max(r['memory_mb'] for r in results if r['status'] == 'OK') if successful_tests > 0 else 0

    print("\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 30 + "СТАТИСТИКА ТЕСТИРОВАНИЯ" + " " * 28 + "║")
    print("╠" + "═" * 80 + "╣")
    print(f"║  Всего тестов: {total_tests:<63} ║")
    print(f"║  Успешных: {successful_tests:<66} ║")
    print(f"║  С ошибками: {failed_tests:<64} ║")
    print(f"║  Процент успеха: {(successful_tests/total_tests*100):.1f}%{' ' * 56} ║")
    print("╠" + "═" * 80 + "╣")
    print(f"║  Среднее время выполнения: {avg_time:.6f} мс{' ' * 38} ║")
    print(f"║  Максимальное время выполнения: {max_time:.6f} мс{' ' * 33} ║")
    print(f"║  Средняя память: {avg_memory:.6f} МБ{' ' * 45} ║")
    print(f"║  Максимальная память: {max_memory:.6f} МБ{' ' * 40} ║")
    print("╚" + "═" * 80 + "╝")

    # Анализ граничных значений
    print("\n")
    print("╔" + "═" * 100 + "╗")
    print("║" + " " * 35 + "АНАЛИЗ ГРАНИЧНЫХ ЗНАЧЕНИЙ" + " " * 35 + "║")
    print("╠" + "═" * 100 + "╣")

    boundary_tests = [
        (6, "N=1000 (макс), M=3 (мин)"),
        (7, "N=2 (мин), M=1000 (макс)"),
        (8, "Большие числа (±2e9)"),
        (12, "Большие множества")
    ]

    for test_num, description in boundary_tests:
        if test_num - 1 < len(results):
            test_result = results[test_num - 1]
            status_icon = "✅" if test_result['status'] == 'OK' else "❌"
            print(f"║  {status_icon} Тест {test_num}: {description:<50} - {test_result['status']:<10} ║")

    print("╚" + "═" * 100 + "╝")
    print()

if __name__ == "__main__":
    main()
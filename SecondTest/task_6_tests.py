import time
import psutil
import os

def can_split(max_pages, chapters, kvolume):
    """
    Проверяет, можно ли разбить главы на kvolume томов так,
    чтобы каждый том содержал не более max_pages страниц
    """
    volumes = 1
    current_sum = 0

    for pages in chapters:
        if pages > max_pages:
            return False
        if current_sum + pages <= max_pages:
            current_sum += pages
        else:
            volumes += 1
            current_sum = pages
            if volumes > kvolume:
                return False

    return volumes <= kvolume

def solve_book_volumes(n, chapters, kvolume):
    """
    Решает задачу о разбиении романа на тома
    """
    left = max(chapters)
    right = sum(chapters)

    while left < right:
        mid = (left + right) // 2
        if can_split(mid, chapters, kvolume):
            right = mid
        else:
            left = mid + 1

    return left

def run_test(test_num, n, chapters, kvolume, expected):
    """
    Запускает один тест и возвращает результаты
    """
    process = psutil.Process(os.getpid())

    # Измеряем память до выполнения
    mem_before = process.memory_info().rss / 1024 / 1024  # в МБ

    # Измеряем время выполнения
    start_time = time.perf_counter()

    try:
        result = solve_book_volumes(n, chapters, kvolume)

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # в миллисекундах

        # Измеряем память после выполнения
        mem_after = process.memory_info().rss / 1024 / 1024  # в МБ
        mem_used = max(mem_after - mem_before, 0.001)  # минимум 0.001 МБ

        is_correct = "ДА" if result == expected else "НЕТ"
        status = "OK"

    except Exception as e:
        result = "Ошибка"
        execution_time = 0
        mem_used = 0
        is_correct = "НЕТ"
        status = f"Ошибка: {str(e)}"

    return {
        'test_num': test_num,
        'n': n,
        'chapters': chapters,
        'kvolume': kvolume,
        'expected': expected,
        'result': result,
        'is_correct': is_correct,
        'time_ms': execution_time,
        'memory_mb': mem_used,
        'status': status
    }

def print_table_header():
    """
    Печатает заголовок таблицы
    """
    print("=" * 150)
    print(f"{'№':<4} | {'N':<4} | {'Главы (страницы)':<35} | {'K':<4} | {'Ожид.':<7} | {'Результат':<10} | {'Верно':<6} | {'Время (мс)':<12} | {'Память (МБ)':<12}")
    print("=" * 150)

def print_test_result(test_data):
    """
    Печатает результат одного теста
    """
    chapters_str = str(test_data['chapters'])
    if len(chapters_str) > 35:
        chapters_str = chapters_str[:32] + "..."

    print(f"{test_data['test_num']:<4} | "
          f"{test_data['n']:<4} | "
          f"{chapters_str:<35} | "
          f"{test_data['kvolume']:<4} | "
          f"{test_data['expected']:<7} | "
          f"{str(test_data['result']):<10} | "
          f"{test_data['is_correct']:<6} | "
          f"{test_data['time_ms']:<12.6f} | "
          f"{test_data['memory_mb']:<12.6f}")

def main():
    # Определение тестовых наборов данных
    tests = [
        # Тест 1: Базовый пример
        (1, 3, [100, 200, 300], 2, 300, "Базовый тест"),

        # Тест 2: Все главы в один том
        (2, 5, [10, 20, 30, 40, 50], 1, 150, "Все главы в один том"),

        # Тест 3: Каждая глава в отдельный том
        (3, 4, [100, 200, 300, 400], 4, 400, "Каждая глава - отдельный том"),

        # Тест 4: Минимальный случай - одна глава
        (4, 1, [500], 1, 500, "Одна глава"),

        # Тест 5: Равномерное распределение
        (5, 6, [50, 50, 50, 50, 50, 50], 3, 100, "Равномерное распределение"),

        # Тест 6: Неравномерное распределение
        (6, 5, [1, 2, 3, 4, 100], 2, 100, "Неравномерное распределение"),

        # Тест 7: Большое количество глав (близко к граничному N=100)
        (7, 50, [10] * 50, 5, 100, "50 глав по 10 страниц"),

        # Тест 8: Граничный случай - максимальное N
        (8, 100, [100] * 100, 10, 1000, "100 глав по 100 страниц"),

        # Тест 9: Граничный случай - близко к максимуму страниц (32767)
        (9, 10, [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3767], 5, 6767, "Близко к максимуму страниц"),

        # Тест 10: Одна очень большая глава
        (10, 5, [1, 1, 1, 32000, 1], 3, 32000, "Одна очень большая глава"),

        # Тест 11: K = N (максимальное количество томов)
        (11, 7, [10, 20, 30, 40, 50, 60, 70], 7, 70, "K равно N"),

        # Тест 12: Минимальные значения
        (12, 2, [1, 1], 2, 1, "Минимальные значения"),

        # Тест 13: Максимальное N=100, все главы по 1 странице
        (13, 100, [1] * 100, 50, 2, "Максимальное N, минимальные страницы"),

        # Тест 14: Максимальные страницы - одна глава в 32767 страниц
        (14, 1, [32767], 1, 32767, "Одна глава с максимумом страниц"),

        # Тест 15: Максимальное N и большие главы
        (15, 100, [300] * 100, 10, 3000, "Максимальное N, равные главы"),

        # Тест 16: Максимальное N с максимальной суммой страниц
        (16, 10, [32767 // 10] * 10, 5, 6552, "Близко к максимуму суммы"),

        # Тест 17: N=100, K=1 (все в один том)
        (17, 100, [100] * 100, 1, 10000, "Максимальное N в один том"),

        # Тест 18: N=100, K=100 (каждая глава - отдельный том)
        (18, 100, list(range(1, 101)), 100, 100, "Максимальное N=K"),

        # Тест 19: Чередование больших и малых глав
        (19, 50, [5000 if i % 2 == 0 else 1 for i in range(50)], 25, 5001, "Чередование больших и малых"),

        # Тест 20: Граничный - одна глава близка к максимуму
        (20, 5, [10000, 10000, 10000, 2767, 1], 2, 20000, "Две большие главы в один том"),

        # Тест 21: Максимальное N=100, максимальные страницы в каждой главе
        (21, 100, [32767] * 100, 100, 32767, "Максимум глав и страниц, K=N"),

        # Тест 22: Максимальное N=100, максимальные страницы, K=50
        (22, 100, [32767] * 100, 50, 65534, "Максимум глав и страниц, K=50"),

        # Тест 23: Максимальное N=100, максимальные страницы, K=1
        (23, 100, [32767] * 100, 1, 3276700, "Максимум всего, один том"),

        # Тест 24: Максимальное N=100, все главы по 32767, K=10
        (24, 100, [32767] * 100, 10, 327670, "Максимум страниц, 10 томов"),

        # Тест 25: N=100, смешанные максимальные главы
        (25, 100, [32767, 1] * 50, 50, 32768, "Чередование макс и мин"),
    ]

    print("\n")
    print("╔" + "═" * 148 + "╗")
    print("║" + " " * 50 + "ТЕСТИРОВАНИЕ ПРОГРАММЫ 'РОМАН В ТОМАХ'" + " " * 60 + "║")
    print("╚" + "═" * 148 + "╝")
    print()

    print_table_header()

    results = []
    for test_data in tests:
        test_num, n, chapters, kvolume, expected, description = test_data
        result = run_test(test_num, n, chapters, kvolume, expected)
        results.append(result)
        print_test_result(result)

    print("=" * 150)

    # Статистика
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['is_correct'] == "ДА")
    avg_time = sum(r['time_ms'] for r in results) / total_tests
    max_time = max(r['time_ms'] for r in results)
    avg_memory = sum(r['memory_mb'] for r in results) / total_tests
    max_memory = max(r['memory_mb'] for r in results)

    print("\n")
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 30 + "СТАТИСТИКА ТЕСТИРОВАНИЯ" + " " * 28 + "║")
    print("╠" + "═" * 80 + "╣")
    print(f"║  Всего тестов: {total_tests:<63} ║")
    print(f"║  Пройдено: {passed_tests:<68} ║")
    print(f"║  Не пройдено: {total_tests - passed_tests:<64} ║")
    print(f"║  Процент успеха: {(passed_tests/total_tests*100):.1f}%{' ' * 56} ║")
    print("╠" + "═" * 80 + "╣")
    print(f"║  Среднее время выполнения: {avg_time:.6f} мс{' ' * 38} ║")
    print(f"║  Максимальное время выполнения: {max_time:.6f} мс{' ' * 33} ║")
    print(f"║  Средняя память: {avg_memory:.6f} МБ{' ' * 45} ║")
    print(f"║  Максимальная память: {max_memory:.6f} МБ{' ' * 40} ║")
    print("╚" + "═" * 80 + "╝")
    print()

if __name__ == "__main__":
    main()
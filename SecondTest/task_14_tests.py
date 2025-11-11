import time
import psutil
import os

def is_match(text, pattern):
    """
    Проверяет, соответствует ли текст шаблону с метасимволами * и ?
    """
    dp = [[False] * (len(pattern) + 1) for _ in range(len(text) + 1)]
    dp[0][0] = True

    for j in range(1, len(pattern) + 1):
        if pattern[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, len(text) + 1):
        for j in range(1, len(pattern) + 1):
            if pattern[j-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif pattern[j-1] == '?' or pattern[j-1] == text[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[len(text)][len(pattern)]

def run_test(test_num, text, pattern, expected, description):
    """
    Запускает один тест и возвращает результаты
    """
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024

    start_time = time.perf_counter()

    try:
        result = "YES" if is_match(text, pattern) else "NO"
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000

        mem_after = process.memory_info().rss / 1024 / 1024
        mem_used = max(mem_after - mem_before, 0.001)

        is_correct = "ДА" if result == expected else "НЕТ"
        status = "OK"

    except Exception as e:
        result = "ERROR"
        execution_time = 0
        mem_used = 0
        is_correct = "НЕТ"
        status = f"Ошибка: {str(e)}"

    return {
        'test_num': test_num,
        'text': text,
        'pattern': pattern,
        'expected': expected,
        'result': result,
        'is_correct': is_correct,
        'time_ms': execution_time,
        'memory_mb': mem_used,
        'status': status,
        'description': description
    }

def print_table_header():
    print("=" * 160)
    print(f"{'№':<4} | {'Текст':<25} | {'Шаблон':<25} | {'Ожид.':<6} | {'Результат':<10} | {'Верно':<6} | {'Время (мс)':<12} | {'Память (МБ)':<12} | {'Описание':<20}")
    print("=" * 160)

def print_test_result(test_data):
    text_str = test_data['text']
    if len(text_str) > 25:
        text_str = text_str[:22] + "..."

    pattern_str = test_data['pattern']
    if len(pattern_str) > 25:
        pattern_str = pattern_str[:22] + "..."

    print(f"{test_data['test_num']:<4} | "
          f"{text_str:<25} | "
          f"{pattern_str:<25} | "
          f"{test_data['expected']:<6} | "
          f"{test_data['result']:<10} | "
          f"{test_data['is_correct']:<6} | "
          f"{test_data['time_ms']:<12.6f} | "
          f"{test_data['memory_mb']:<12.6f} | "
          f"{test_data['description']:<20}")

def main():
    tests = [
        # Базовые тесты (3 теста)
        (1, "ABC", "ABC", "YES", "Точное совпадение"),
        (2, "ABC", "XYZ", "NO", "Полное несовпадение"),
        (3, "", "", "YES", "Обе пустые строки"),

        # Тесты с ? (3 теста)
        (4, "ABC", "A?C", "YES", "? посередине"),
        (5, "ABC", "???", "YES", "Все ?"),
        (6, "ABC", "A?", "NO", "? не хватает символов"),

        # Тесты с * (3 теста)
        (7, "ABC", "*", "YES", "Только *"),
        (8, "", "*", "YES", "Пустая строка и *"),
        (9, "ABCDEF", "A*F", "YES", "* охватывает много"),

        # Комбинации ? и * (3 теста)
        (10, "ABCD", "A?*D", "YES", "A, ?, *, D"),
        (11, "AC", "A*C", "YES", "* = пустая строка"),
        (12, "ABCDEFGH", "A*?*H", "YES", "Сложная комбинация"),

        # Реальные примеры (2 теста)
        (13, "SOMETEXT", "S*T", "YES", "SOMETEXT: S*T"),
        (14, "FILENAME", "FILE*", "YES", "FILENAME: FILE*"),

        # Специальные паттерны (2 теста)
        (15, "AAAA", "A*A", "YES", "A*A на AAAA"),
        (16, "ABCD", "*A*B*C*D*", "YES", "* между всеми"),

        # ГРАНИЧНЫЕ ТЕСТЫ - максимум 700 символов (9 тестов)
        (17, "A" * 700, "A" * 700, "YES", "ГРАНИЦА: 700A = 700A"),
        (18, "A" * 700, "?" * 700, "YES", "ГРАНИЦА: 700A = 700?"),
        (19, "A" * 700, "*", "YES", "ГРАНИЦА: 700A = *"),
        (20, "A" * 700, "A" * 699, "NO", "ГРАНИЦА: 699 ≠ 700"),
        (21, "A" * 350 + "B" * 350, "A*B*", "YES", "ГРАНИЦА: 350A+350B"),
        (22, "ABC", "*" * 700, "YES", "ГРАНИЦА: шаблон 700*"),
        (23, "C" * 700, "?" * 350 + "*", "YES", "ГРАНИЦА: 350? + *"),
        (24, "ABCDEFGHIJ" * 70, "ABC*", "YES", "ГРАНИЦА: 70 повторов"),
        (25, "Z" * 700, "*Z*Z*Z*", "YES", "ГРАНИЦА ФИНАЛ: *Z*Z*"),
    ]

    print("\n")
    print("╔" + "═" * 158 + "╗")
    print("║" + " " * 45 + "ТЕСТИРОВАНИЕ ЗАДАЧИ 'СОПОСТАВЛЕНИЕ ПО ОБРАЗЦУ'" + " " * 68 + "║")
    print("╚" + "═" * 158 + "╝")
    print()

    print_table_header()

    results = []
    for test_data in tests:
        test_num, text, pattern, expected, description = test_data
        result = run_test(test_num, text, pattern, expected, description)
        results.append(result)
        print_test_result(result)

    print("=" * 160)

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
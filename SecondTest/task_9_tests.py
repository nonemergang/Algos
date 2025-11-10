import time
import psutil
import os
import sys

def phone_book_solution(commands):
    """
    Решение задачи телефонной книги
    """
    phone_book = {}
    result = []

    for command in commands:
        parts = command.split()
        cmd_type = parts[0]

        if cmd_type == "ADD":
            user, number = parts[1], parts[2]
            if user in phone_book:
                result.append("ERROR")
            else:
                phone_book[user] = number

        elif cmd_type == "DELETE":
            user = parts[1]
            if user not in phone_book:
                result.append("ERROR")
            else:
                del phone_book[user]

        elif cmd_type == "EDITPHONE":
            user, number = parts[1], parts[2]
            if user not in phone_book:
                result.append("ERROR")
            else:
                phone_book[user] = number

        elif cmd_type == "PRINT":
            user = parts[1]
            if user not in phone_book:
                result.append("ERROR")
            else:
                result.append(f"{user} {phone_book[user]}")

    return result

def run_phone_book_test(test_num, n, commands, expected_output, description):
    """
    Запускает один тест для телефонной книги и возвращает результаты
    """
    process = psutil.Process(os.getpid())

    # Измеряем память до выполнения
    mem_before = process.memory_info().rss / 1024 / 1024  # в МБ

    # Измеряем время выполнения
    start_time = time.perf_counter()

    try:
        result = phone_book_solution(commands)

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # в миллисекундах

        # Измеряем память после выполнения
        mem_after = process.memory_info().rss / 1024 / 1024  # в МБ
        mem_used = max(mem_after - mem_before, 0.001)  # минимум 0.001 МБ

        # Проверяем корректность
        is_correct = "ДА" if result == expected_output else "НЕТ"
        status = "OK"

    except Exception as e:
        result = f"Ошибка: {str(e)}"
        execution_time = 0
        mem_used = 0
        is_correct = "НЕТ"
        status = f"Ошибка: {str(e)}"

    return {
        'test_num': test_num,
        'n': n,
        'commands': commands,
        'expected': expected_output,
        'result': result,
        'is_correct': is_correct,
        'time_ms': execution_time,
        'memory_mb': mem_used,
        'status': status,
        'description': description
    }

def print_phone_book_table_header():
    """
    Печатает заголовок таблицы для телефонной книги
    """
    print("=" * 120)
    print(f"{'№':<3} | {'N':<3} | {'Описание':<25} | {'Ожидаемый':<20} | {'Результат':<20} | {'Верно':<6} | {'Время (мс)':<12} | {'Память (МБ)':<12}")
    print("=" * 120)

def print_phone_book_test_result(test_data):
    """
    Печатает результат одного теста для телефонной книги
    """
    # Обрезаем длинные описания
    desc = test_data['description']
    if len(desc) > 25:
        desc = desc[:22] + "..."

    # Обрезаем ожидаемый результат для отображения
    expected_str = str(test_data['expected'])
    if len(expected_str) > 20:
        expected_str = expected_str[:17] + "..."

    # Обрезаем фактический результат для отображения
    result_str = str(test_data['result'])
    if len(result_str) > 20:
        result_str = result_str[:17] + "..."

    print(f"{test_data['test_num']:<3} | "
          f"{test_data['n']:<3} | "
          f"{desc:<25} | "
          f"{expected_str:<20} | "
          f"{result_str:<20} | "
          f"{test_data['is_correct']:<6} | "
          f"{test_data['time_ms']:<12.6f} | "
          f"{test_data['memory_mb']:<12.6f}")

def calculate_expected_output(commands):
    """
    Вычисляет ожидаемый вывод для заданного списка команд
    """
    phone_book = {}
    expected = []

    for command in commands:
        parts = command.split()
        cmd_type = parts[0]

        if cmd_type == "ADD":
            user, number = parts[1], parts[2]
            if user in phone_book:
                expected.append("ERROR")
            else:
                phone_book[user] = number
                # Успешное ADD не дает вывода

        elif cmd_type == "DELETE":
            user = parts[1]
            if user not in phone_book:
                expected.append("ERROR")
            else:
                del phone_book[user]
                # Успешное DELETE не дает вывода

        elif cmd_type == "EDITPHONE":
            user, number = parts[1], parts[2]
            if user not in phone_book:
                expected.append("ERROR")
            else:
                phone_book[user] = number
                # Успешное EDITPHONE не дает вывода

        elif cmd_type == "PRINT":
            user = parts[1]
            if user not in phone_book:
                expected.append("ERROR")
            else:
                expected.append(f"{user} {phone_book[user]}")

    return expected

def generate_large_test(n):
    """
    Генерирует большой тест с N командами и правильными ожидаемыми результатами
    """
    commands = []

    # 1. Добавляем пользователей (40%)
    add_count = n * 4 // 10
    for i in range(add_count):
        commands.append(f"ADD USER{i} {1000000 + i}")

    # 2. Пытаемся добавить существующих (10%)
    error_add_count = n // 10
    for i in range(error_add_count):
        commands.append(f"ADD USER{i} {2000000 + i}")  # Эти пользователи уже существуют

    # 3. Выводим пользователей (15%)
    print_count = n * 15 // 100
    for i in range(print_count):
        commands.append(f"PRINT USER{i}")

    # 4. Редактируем телефоны (10%)
    edit_count = n // 10
    for i in range(edit_count):
        commands.append(f"EDITPHONE USER{i} {3000000 + i}")

    # 5. Выводим после редактирования (10%)
    print_after_edit = n // 10
    for i in range(print_after_edit):
        commands.append(f"PRINT USER{i}")

    # 6. Удаляем пользователей (10%)
    delete_count = n // 10
    for i in range(delete_count):
        commands.append(f"DELETE USER{i}")

    # 7. Ошибки с удаленными пользователями (5%)
    error_count = n - len(commands)
    for i in range(error_count):
        # Чередуем разные команды с удаленными пользователями
        if i % 3 == 0:
            commands.append(f"PRINT USER{i}")
        elif i % 3 == 1:
            commands.append(f"DELETE USER{i}")
        else:
            commands.append(f"EDITPHONE USER{i} {4000000 + i}")

    # Обрезаем до точного n
    commands = commands[:n]

    # Вычисляем ожидаемый вывод
    expected = calculate_expected_output(commands)

    return commands, expected

def main():
    # Определение тестовых наборов данных для телефонной книги
    tests = [
        # Тест 1: Базовый пример из условия
        (1, 9, [
            "ADD IVAN 1178927",
            "PRINT PETER",
            "ADD EGOR 123412",
            "PRINT IVAN",
            "EDITPHONE IVAN 112358",
            "PRINT IVAN",
            "PRINT EGOR",
            "DELETE EGOR",
            "EDITPHONE EGOR 123456"
        ], [
             "ERROR",
             "IVAN 1178927",
             "IVAN 112358",
             "EGOR 123412",
             "ERROR"
         ], "Базовый тест из условия"),

        # Тест 2: Граничный случай - 0 команд
        (2, 0, [], [], "0 команд"),

        # Тест 3: Только добавления
        (3, 5, [
            "ADD ALICE 1111111",
            "ADD BOB 2222222",
            "ADD CHARLIE 3333333",
            "ADD DAVE 4444444",
            "ADD EVE 5555555"
        ], [], "Только добавления"),

        # Тест 4: Только вывод несуществующих
        (4, 3, [
            "PRINT UNKNOWN1",
            "PRINT UNKNOWN2",
            "PRINT UNKNOWN3"
        ], ["ERROR", "ERROR", "ERROR"], "Только ошибки PRINT"),

        # Тест 5: Многократные операции с одним пользователем
        (5, 6, [
            "ADD USER1 1111111",
            "EDITPHONE USER1 2222222",
            "EDITPHONE USER1 3333333",
            "PRINT USER1",
            "DELETE USER1",
            "PRINT USER1"
        ], ["USER1 3333333", "ERROR"], "Многократные операции"),

        # Тест 6: Попытка добавить существующего
        (6, 3, [
            "ADD USER1 1111111",
            "ADD USER1 2222222",
            "PRINT USER1"
        ], ["ERROR", "USER1 1111111"], "Добавление существующего"),

        # Тест 7: Удаление несуществующего
        (7, 2, [
            "DELETE UNKNOWN",
            "ADD USER1 1234567"
        ], ["ERROR"], "Удаление несуществующего"),

        # Тест 8: Редактирование несуществующего
        (8, 2, [
            "EDITPHONE UNKNOWN 8888888",
            "ADD USER1 7777777"
        ], ["ERROR"], "Редактирование несуществующего"),

        # Тест 9: Смешанные операции
        (9, 8, [
            "ADD USER1 1111111",
            "ADD USER2 2222222",
            "DELETE USER1",
            "ADD USER1 3333333",
            "PRINT USER2",
            "EDITPHONE USER2 4444444",
            "PRINT USER2",
            "PRINT USER1"
        ], ["USER2 2222222", "USER2 4444444", "USER1 3333333"], "Смешанные операции"),

        # Тест 10: Длинные имена
        (10, 4, [
            "ADD VERYLONGUSERNAME 1234567890",
            "PRINT VERYLONGUSERNAME",
            "EDITPHONE VERYLONGUSERNAME 9876543210",
            "PRINT VERYLONGUSERNAME"
        ], ["VERYLONGUSERNAME 1234567890", "VERYLONGUSERNAME 9876543210"], "Длинные имена"),

        # Тест 11: Граничный случай - максимальное N=1000
        (11, 1000, [], [], "Максимальное N=1000"),

        # Тест 12: Все команды с ошибками
        (12, 4, [
            "DELETE UNKNOWN1",
            "EDITPHONE UNKNOWN2 1234567",
            "PRINT UNKNOWN3",
            "ADD UNKNOWN4 1234567"
        ], ["ERROR", "ERROR", "ERROR"], "Все команды с ошибками"),

        # Тест 13: Чередование добавлений и удалений
        (13, 6, [
            "ADD USER1 1111111",
            "DELETE USER1",
            "ADD USER1 2222222",
            "DELETE USER1",
            "ADD USER1 3333333",
            "PRINT USER1"
        ], ["USER1 3333333"], "Чередование операций"),

        # Тест 14: Дублирование команд
        (14, 5, [
            "ADD USER1 1111111",
            "ADD USER1 2222222",
            "DELETE USER1",
            "DELETE USER1",
            "ADD USER1 3333333"
        ], ["ERROR", "ERROR"], "Дублирование команд"),

        # Тест 15: Комплексный тест
        (15, 10, [
            "ADD A 1111111",
            "ADD B 2222222",
            "PRINT A",
            "EDITPHONE A 3333333",
            "PRINT A",
            "DELETE B",
            "PRINT B",
            "ADD C 4444444",
            "EDITPHONE C 5555555",
            "PRINT C"
        ], ["A 1111111", "A 3333333", "ERROR", "C 5555555"], "Комплексный тест"),
    ]

    print("\n")
    print("╔" + "═" * 118 + "╗")
    print("║" + " " * 40 + "ТЕСТИРОВАНИЕ ПРОГРАММЫ 'ТЕЛЕФОННАЯ КНИГА'" + " " * 40 + "║")
    print("╚" + "═" * 118 + "╝")
    print()

    print_phone_book_table_header()

    results = []

    for test_data in tests:
        test_num, n, commands, expected, description = test_data

        # Генерируем большой тест для N=1000
        if test_num == 11:
            commands, expected = generate_large_test(1000)

        result = run_phone_book_test(test_num, n, commands, expected, description)
        results.append(result)
        print_phone_book_test_result(result)

        # Для больших тестов показываем сокращенный вывод
        if test_num == 11:
            if result['is_correct'] == "ДА":
                print(f"   ✓ Большой тест с {n} командами выполнен успешно!")
                if result['result']:
                    print(f"   Первые 3 результата: {result['result'][:3]}")
                    print(f"   Всего результатов: {len(result['result'])}")
            else:
                print(f"   ✗ Тест не пройден!")
                print(f"   Ожидалось результатов: {len(expected)}")
                print(f"   Получено результатов: {len(result['result']) if result['result'] else 0}")

    print("=" * 120)

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

    # Детальная информация о самом долгом тесте
    if max_time > 0:
        longest_test = max(results, key=lambda x: x['time_ms'])
        print(f"\nСамый долгий тест: №{longest_test['test_num']} - {longest_test['description']}")
        print(f"Время выполнения: {longest_test['time_ms']:.6f} мс")

    print()

if __name__ == "__main__":
    main()
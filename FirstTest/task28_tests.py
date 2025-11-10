import time
import psutil
import os

def count_comments_and_strings(text):
    """
    Основная функция для тестирования
    """
    count1 = 0  # (* *)
    count2 = 0  # { }
    count3 = 0  # //
    string_count = 0  # '...'

    i = 0
    n = len(text)

    while i < n:
        # Обработка строковых литералов
        if text[i] in ["'", "‘", "’"]:
            string_count += 1
            i += 1
            while i < n and text[i] not in ["'", "‘", "’"]:
                i += 1
            if i < n:
                i += 1
            continue

        # Комментарии (* *)
        elif i + 1 < n and text[i] == '(' and text[i+1] == '*':
            count1 += 1
            i += 2
            while i + 1 < n:
                if text[i] == '*' and text[i+1] == ')':
                    i += 2
                    break
                i += 1
            continue

        # Комментарии { }
        elif text[i] == '{':
            count2 += 1
            i += 1
            while i < n and text[i] != '}':
                i += 1
            if i < n:
                i += 1
            continue

        # Комментарии //
        elif i + 1 < n and text[i] == '/' and text[i+1] == '/':
            count3 += 1
            i += 2
            while i < n and text[i] != '\n':
                i += 1
            continue

        else:
            i += 1

    return count1, count2, count3, string_count

# Тестовые данные
test_cases = [
    # Базовые тесты
    {
        "input": "program test; (* comment *) begin end.",
        "expected": (1, 0, 0, 0),
        "description": "Базовый тест с одним комментарием (* *)"
    },
    {
        "input": "program test; { comment } begin end.",
        "expected": (0, 1, 0, 0),
        "description": "Базовый тест с одним комментарием { }"
    },
    {
        "input": "program test; // comment\nbegin end.",
        "expected": (0, 0, 1, 0),
        "description": "Базовый тест с одним комментарием //"
    },
    {
        "input": "program test; write('hello'); begin end.",
        "expected": (0, 0, 0, 1),
        "description": "Базовый тест с одной строкой"
    },

    # Граничные случаи
    {
        "input": "",
        "expected": (0, 0, 0, 0),
        "description": "Пустой вход"
    },
    {
        "input": "''''",
        "expected": (0, 0, 0, 2),
        "description": "Несколько строк подряд"
    },

    # Сложные случаи
    {
        "input": "write('(* not comment *)'); // real comment",
        "expected": (0, 0, 1, 1),
        "description": "Комментарий в строке и реальный комментарий"
    },
    {
        "input": "(* { nested } *) // test",
        "expected": (1, 0, 1, 0),
        "description": "Комментарии разных типов"
    },
    {
        "input": "program test;\n(* multi\nline\ncomment *)\nbegin end.",
        "expected": (1, 0, 0, 0),
        "description": "Многострочный комментарий"
    },

    # Большие данные (граничные по размеру)
    {
        "input": "//" + "\n//" * 1000,
        "expected": (0, 0, 1001, 0),
        "description": "1001 комментарий //"
    },
    {
        "input": "(*" + "x" * 10000 + "*)",
        "expected": (1, 0, 0, 0),
        "description": "Большой комментарий (* *)"
    },
    {
        "input": "'" + "a" * 5000 + "'",
        "expected": (0, 0, 0, 1),
        "description": "Длинная строка"
    },

    # Специальные случаи
    {
        "input": "(* unfinished comment",
        "expected": (1, 0, 0, 0),
        "description": "Незавершенный комментарий"
    }
]

def run_tests():
    """
    Запуск всех тестов и вывод результатов в табличном формате
    """
    print("=" * 120)
    print(f"{'№':<3} | {'Описание':<40} | {'Ожидаемый':<15} | {'Полученный':<15} | {'Корректность':<12} | {'Время (мс)':<10} | {'Память (Мб)':<10}")
    print("=" * 120)

    process = psutil.Process(os.getpid())

    for i, test in enumerate(test_cases, 1):
        # Измеряем память до теста
        memory_before = process.memory_info().rss / 1024 / 1024

        # Измеряем время выполнения
        start_time = time.time()

        try:
            result = count_comments_and_strings(test["input"])
            execution_time = (time.time() - start_time) * 1000  # в миллисекундах
        except Exception as e:
            result = f"Ошибка: {e}"
            execution_time = 0

        # Измеряем память после теста
        memory_after = process.memory_info().rss / 1024 / 1024
        memory_used = memory_after - memory_before

        # Проверяем корректность
        if isinstance(result, tuple) and result == test["expected"]:
            correctness = "✓ Корректно"
        elif isinstance(result, tuple):
            correctness = "✗ Неверно"
        else:
            correctness = "✗ Ошибка"

        # Форматируем вывод
        expected_str = str(test["expected"])
        result_str = str(result)

        # Обрезаем длинные строки для красивого вывода
        if len(expected_str) > 13:
            expected_str = expected_str[:10] + "..."
        if len(result_str) > 13:
            result_str = result_str[:10] + "..."

        print(f"{i:<3} | {test['description']:<40} | {expected_str:<15} | {result_str:<15} | {correctness:<12} | {execution_time:<10.3f} | {memory_used:<10.3f}")

    print("=" * 120)

def detailed_test_report():
    """
    Подробный отчет по каждому тесту
    """
    print("\n" + "=" * 80)
    print("ПОДРОБНЫЙ ОТЧЕТ ПО ТЕСТАМ")
    print("=" * 80)

    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Тест {i}: {test['description']} ---")
        print(f"Входные данные: {repr(test['input'][:100])}{'...' if len(test['input']) > 100 else ''}")

        start_time = time.time()
        result = count_comments_and_strings(test["input"])
        execution_time = (time.time() - start_time) * 1000

        print(f"Ожидаемый результат: {test['expected']}")
        print(f"Полученный результат: {result}")
        print(f"Время выполнения: {execution_time:.3f} мс")

        if result == test["expected"]:
            print("✅ ТЕСТ ПРОЙДЕН")
        else:
            print("❌ ТЕСТ НЕ ПРОЙДЕН")

if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ ПРОГРАММЫ ПОДСЧЕТА КОММЕНТАРИЕВ И СТРОК")
    print("В Object Pascal")

    # Запуск компактных тестов
    run_tests()

    # Запуск подробного отчета
    detailed_test_report()

    # Итоговая статистика
    print("\n" + "=" * 50)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 50)

    passed = 0
    total_time = 0

    for test in test_cases:
        start_time = time.time()
        result = count_comments_and_strings(test["input"])
        total_time += (time.time() - start_time) * 1000

        if result == test["expected"]:
            passed += 1

    print(f"Пройдено тестов: {passed}/{len(test_cases)}")
    print(f"Общее время выполнения: {total_time:.3f} мс")
    print(f"Среднее время на тест: {total_time/len(test_cases):.3f} мс")

    # Использование памяти
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024
    print(f"Использование памяти: {memory_usage:.2f} МБ")
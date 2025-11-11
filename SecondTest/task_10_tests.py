
import time
import psutil
import os
import sys
from io import StringIO

def create_boundary_test_cases():
    """Создает граничные тестовые случаи для оптимизированного алгоритма"""
    test_cases = []

    # Тест 1: Максимальные значения - N=100000, L=10000 (все одинаковые слова)
    print("Подготовка теста 1: N=100000, L=10000...")
    n = 100000
    l = 10000
    word = "A" * l
    input_data = f"{n}\n{word}"
    test_cases.append((1, input_data, "1", f"N={n}, L={l}, все одинаковые"))

    # Тест 2: Максимальные значения - N=100000, L=10000 (разные слова)
    print("Подготовка теста 2: N=100000, L=100...")
    n = 100000
    l = 100
    input_lines = [str(n)]
    # Создаем 100 уникальных слов
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    unique_words = []
    for i in range(100):
        word = ""
        for j in range(l):
            word += chars[(i + j) % 26]
        unique_words.append(word)

    for i in range(n):
        input_lines.append(unique_words[i % 100])
    input_data = "\n".join(input_lines)
    test_cases.append((2, input_data, "100", f"N={n}, L={l}, 100 комплектов"))

    # Тест 3: Длинные слова - L=10000
    print("Подготовка теста 3: N=1000, L=10000...")
    n = 1000
    l = 10000
    word = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * (l // 26)
    word = word[:l]
    input_data = f"{n}\n{word}"
    test_cases.append((3, input_data, "1", f"N={n}, L={l}, все одинаковые"))

    # Тест 4: Смешанные анаграммы
    print("Подготовка теста 4: N=50000, L=500...")
    n = 50000
    l = 500
    groups = [
        "A" * 200 + "B" * 200 + "C" * 100,
        "D" * 250 + "E" * 250,
        "F" * 100 + "G" * 100 + "H" * 100 + "I" * 100 + "J" * 100
    ]
    input_lines = [str(n)]
    for i in range(n):
        input_lines.append(groups[i % len(groups)])
    input_data = "\n".join(input_lines)
    test_cases.append((4, input_data, str(len(groups)), f"N={n}, L={l}, {len(groups)} комплектов"))

    # Тест 5: Минимальные значения
    test_cases.append((5, "3\nABC\nBAC\nCAB", "1", "N=3, L=3, анаграммы"))

    # Тест 6: Все слова разные
    test_cases.append((6, "5\nABC\nDEF\nGHI\nJKL\nMNO", "5", "N=5, L=3, все разные"))

    return test_cases

def run_optimized_algorithm(input_data):
    """Запускает оптимизированный алгоритм и возвращает результат"""
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    try:
        # Перенаправляем ввод/вывод
        sys.stdin = StringIO(input_data)
        output_capture = StringIO()
        sys.stdout = output_capture

        # Измеряем память до выполнения
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024

        start_time = time.perf_counter()

        # Выполняем оптимизированный алгоритм
        exec("""
def main():
    n = int(input().strip())
    complexes = {}
    unique_count = 0
    
    for i in range(n):
        word = input().strip()
        freq = [0] * 26
        for char in word:
            if char == 'A': idx = 0
            elif char == 'B': idx = 1
            elif char == 'C': idx = 2
            elif char == 'D': idx = 3
            elif char == 'E': idx = 4
            elif char == 'F': idx = 5
            elif char == 'G': idx = 6
            elif char == 'H': idx = 7
            elif char == 'I': idx = 8
            elif char == 'J': idx = 9
            elif char == 'K': idx = 10
            elif char == 'L': idx = 11
            elif char == 'M': idx = 12
            elif char == 'N': idx = 13
            elif char == 'O': idx = 14
            elif char == 'P': idx = 15
            elif char == 'Q': idx = 16
            elif char == 'R': idx = 17
            elif char == 'S': idx = 18
            elif char == 'T': idx = 19
            elif char == 'U': idx = 20
            elif char == 'V': idx = 21
            elif char == 'W': idx = 22
            elif char == 'X': idx = 23
            elif char == 'Y': idx = 24
            else: idx = 25
            freq[idx] += 1
        
        freq_key = (
            freq[0], freq[1], freq[2], freq[3], freq[4], freq[5], freq[6], freq[7], freq[8], freq[9],
            freq[10], freq[11], freq[12], freq[13], freq[14], freq[15], freq[16], freq[17], freq[18], freq[19],
            freq[20], freq[21], freq[22], freq[23], freq[24], freq[25]
        )
        
        if freq_key not in complexes:
            complexes[freq_key] = True
            unique_count += 1
    
    print(unique_count)

main()
""")

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000

        result = output_capture.getvalue().strip()

        # Измеряем память после выполнения
        mem_after = process.memory_info().rss / 1024 / 1024
        mem_used = max(mem_after - mem_before, 0.1)

        return result, execution_time, mem_used, "OK"

    except Exception as e:
        return f"Ошибка: {str(e)}", 0, 0, f"Ошибка выполнения"
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout

def run_boundary_test(test_num, input_data, expected, description):
    """Запускает один граничный тест"""
    print(f"🔍 Тест {test_num}: {description}")

    result, execution_time, mem_used, status = run_optimized_algorithm(input_data)

    # Проверяем корректность
    try:
        result_int = int(result)
        expected_int = int(expected)
        is_correct = "ДА" if result_int == expected_int else "НЕТ"
    except:
        is_correct = "НЕТ"

    return {
        'test_num': test_num,
        'description': description,
        'input_data': f"N={len(input_data.splitlines())-1}",
        'expected': expected,
        'result': result,
        'is_correct': is_correct,
        'time_ms': execution_time,
        'memory_mb': mem_used,
        'status': status
    }

def print_results_table(results):
    """Печатает таблицу с результатами"""
    print("\n" + "=" * 130)
    print(f"{'№':<3} | {'Тест':<30} | {'Ожид.':<6} | {'Результат':<10} | {'Верно':<6} | {'Время (мс)':<12} | {'Память (МБ)':<12} | {'Статус':<10}")
    print("=" * 130)

    for result in results:
        result_str = str(result['result'])
        if len(result_str) > 10:
            result_str = result_str[:7] + "..."

        print(f"{result['test_num']:<3} | "
              f"{result['description']:<30} | "
              f"{result['expected']:<6} | "
              f"{result_str:<10} | "
              f"{result['is_correct']:<6} | "
              f"{result['time_ms']:<12.1f} | "
              f"{result['memory_mb']:<12.1f} | "
              f"{result['status']:<10}")

def analyze_performance(results):
    """Анализирует производительность алгоритма"""
    print("\n📊 ДЕТАЛЬНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("=" * 80)

    time_limit = 500  # 0.5 секунды
    memory_limit = 256  # 256 МБ

    total_tests = len(results)
    passed_correctness = 0
    passed_time = 0
    passed_memory = 0

    print("\n🧪 РЕЗУЛЬТАТЫ ПО ТЕСТАМ:")
    for result in results:
        time_ok = result['time_ms'] <= time_limit
        memory_ok = result['memory_mb'] <= memory_limit
        correct_ok = result['is_correct'] == "ДА"

        if correct_ok:
            passed_correctness += 1
        if time_ok:
            passed_time += 1
        if memory_ok:
            passed_memory += 1

        status_icon = "✅" if correct_ok and time_ok and memory_ok else "⚠️" if correct_ok else "❌"

        print(f"{status_icon} Тест {result['test_num']}: {result['description']}")
        if correct_ok:
            print(f"   ✓ Корректность: {result['result']} = {result['expected']}")
        else:
            print(f"   ✗ Корректность: {result['result']} ≠ {result['expected']}")

        if not time_ok:
            print(f"   ⚠️  Время: {result['time_ms']:.1f} мс > {time_limit} мс")
        else:
            print(f"   ✓ Время: {result['time_ms']:.1f} мс")

        if not memory_ok:
            print(f"   ⚠️  Память: {result['memory_mb']:.1f} МБ > {memory_limit} МБ")
        else:
            print(f"   ✓ Память: {result['memory_mb']:.1f} МБ")
        print()

def main():
    """Основная функция тестирования"""
    print("🚀 ГРАНИЧНОЕ ТЕСТИРОВАНИЕ ОПТИМИЗИРОВАННОГО АЛГОРИТМА")
    print("Алгоритм с хэш-таблицей и кортежами частот")
    print("=" * 70)

    # Создаем тестовые случаи
    test_cases = create_boundary_test_cases()

    results = []
    for test_num, input_data, expected, description in test_cases:
        result = run_boundary_test(test_num, input_data, expected, description)
        results.append(result)

    # Выводим результаты
    print_results_table(results)
    analyze_performance(results)

    # Итоговая статистика
    total_tests = len(results)
    passed_correctness = sum(1 for r in results if r['is_correct'] == "ДА")
    passed_time = sum(1 for r in results if r['time_ms'] <= 500)
    passed_memory = sum(1 for r in results if r['memory_mb'] <= 256)

    print("🎯 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"Всего тестов: {total_tests}")
    print(f"Корректность: {passed_correctness}/{total_tests} ({passed_correctness/total_tests*100:.1f}%)")
    print(f"Время (≤500мс): {passed_time}/{total_tests} ({passed_time/total_tests*100:.1f}%)")
    print(f"Память (≤256МБ): {passed_memory}/{total_tests} ({passed_memory/total_tests*100:.1f}%)")

    # Заключение
    if passed_correctness == total_tests and passed_time == total_tests and passed_memory == total_tests:
        print("\n🎉 АЛГОРИТМ ПРОШЕЛ ВСЕ ТЕСТЫ! Готов к использованию с N=100000, L=10000")
    elif passed_correctness == total_tests:
        print("\n💡 АЛГОРИТМ КОРРЕКТЕН, но требует оптимизации времени/памяти")
    else:
        print("\n❌ АЛГОРИТМ ТРЕБУЕТ ИСПРАВЛЕНИЯ ОШИБОК")

if __name__ == "__main__":
    main()
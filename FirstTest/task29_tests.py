import time
import psutil
import os

# Глобальные переменные для хранения данных дерева
adj = []        # Список смежности
dist = []       # Расстояние от корня
depth = []      # Глубина вершины
up = []         # Таблица предков для Binary Lifting
LOG = 0         # Максимальная степень двойки


def add_edge(u, v, w):
    """Добавляет ребро между вершинами u и v с весом w"""
    adj[u].append((v, w))
    adj[v].append((u, w))


def dfs(v, parent, d, dist_from_root):
    """
    DFS для построения дерева и вычисления расстояний
    v - текущая вершина
    parent - родитель вершины v
    d - глубина вершины v
    dist_from_root - расстояние от корня до v
    """
    depth[v] = d
    dist[v] = dist_from_root
    up[v][0] = parent

    # Заполняем таблицу предков (Binary Lifting)
    for i in range(1, LOG):
        if up[v][i-1] != -1:
            up[v][i] = up[up[v][i-1]][i-1]

    # Обходим всех соседей
    for neighbor, weight in adj[v]:
        if neighbor != parent:
            dfs(neighbor, v, d + 1, dist_from_root + weight)


def get_lca(u, v):
    """
    Находит наименьшего общего предка (LCA) вершин u и v
    """
    if depth[u] < depth[v]:
        u, v = v, u

    # Поднимаем u на уровень v
    diff = depth[u] - depth[v]
    for i in range(LOG):
        if (diff >> i) & 1:
            u = up[u][i]

    if u == v:
        return u

    # Поднимаем обе вершины одновременно
    for i in range(LOG - 1, -1, -1):
        if up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]

    return up[u][0]


def get_distance(u, v):
    """
    Вычисляет расстояние между вершинами u и v
    """
    if u == v:
        return 0
    lca = get_lca(u, v)
    return dist[u] + dist[v] - 2 * dist[lca]


def initialize_tree(n, edges):
    """Инициализирует дерево с заданными параметрами"""
    global adj, dist, depth, up, LOG

    # Вычисляем LOG
    LOG = 1
    while (1 << LOG) < n:
        LOG += 1
    LOG += 1

    # Инициализируем массивы
    adj = [[] for _ in range(n)]
    dist = [0] * n
    depth = [0] * n
    up = [[-1] * LOG for _ in range(n)]

    # Добавляем рёбра
    for u, v, w in edges:
        add_edge(u, v, w)

    # Строим дерево с корнем в вершине 0
    if n > 0:
        dfs(0, -1, 0, 0)


def get_memory_usage():
    """Возвращает использование памяти текущим процессом в МБ"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


# Тестовые случаи
test_cases = [
    # (n, edges, queries, expected_results, description)
    (
        3,
        [(0, 1, 5), (1, 2, 3)],
        [(0, 1), (0, 2), (1, 2)],
        [5, 8, 3],
        "Простая цепочка из 3 вершин"
    ),
    (
        4,
        [(1, 0, 3), (1, 2, 7), (1, 3, 5)],
        [(0, 3), (2, 3), (0, 2), (1, 1)],
        [3 + 5, 7 + 5, 3 + 7, 0],
        "Звездообразное дерево"
    ),
    (
        6,
        [(0, 1, 10), (1, 2, 20), (2, 3, 5), (3, 4, 8), (4, 5, 3)],
        [(0, 5), (1, 4), (2, 3), (0, 2)],
        [46, 33, 5, 30],
        "Длинная цепочка"
    ),
    (
        4,
        [(0, 1, 1), (0, 2, 1), (0, 3, 1)],
        [(1, 2), (1, 3), (2, 3)],
        [2, 2, 2],
        "Звезда с равными рёбрами"
    ),
    (
        7,
        [(0, 1, 5), (0, 2, 3), (1, 3, 2), (1, 4, 7), (2, 5, 4), (2, 6, 6)],
        [(3, 5), (4, 6), (3, 4), (5, 6)],
        [14, 21, 9, 10],
        "Сбалансированное бинарное дерево"
    ),
    (
        2,
        [(0, 1, 100)],
        [(0, 1)],
        [100],
        "Минимальное дерево (2 вершины)"
    ),
    (
        8,
        [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (6, 7, 1)],
        [(0, 7), (1, 6), (2, 5), (3, 4)],
        [7, 5, 3, 1],
        "Цепочка максимальной длины"
    ),
    (
        5,
        [(0, 1, 10), (0, 2, 15), (1, 3, 20), (2, 4, 25)],
        [(3, 4), (0, 3), (1, 4)],
        [70, 30, 50],
        "Дерево с большими весами"
    ),
    (
        1,
        [],
        [(0, 0)],
        [0],
        "Дерево с одной вершиной"
    ),
    (
        10,
        [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 4), (4, 5, 2),
         (5, 6, 3), (6, 7, 1), (7, 8, 5), (8, 9, 2)],
        [(0, 9), (1, 8), (2, 7), (3, 6), (4, 5)],
        [23, 19, 11, 9, 2],
        "Большая цепочка с разными весами"
    )
]

print("=" * 120)
print("ТЕСТИРОВАНИЕ АЛГОРИТМА РАССТОЯНИЯ В ДЕРЕВЕ")
print("=" * 120)
print(f"{'Описание':<40} | {'Ожидаемый':<15} | {'Полученный':<15} | {'Корректность':<15} | {'Время (мс)':<12} | {'Память (Мб)'}")
print("-" * 120)

total_tests = len(test_cases)
passed_tests = 0
execution_times = []
memory_usages = []

for i, (n, edges, queries, expected_results, description) in enumerate(test_cases, 1):
    # Измеряем память и время
    start_memory = get_memory_usage()
    start_time = time.time()

    # Инициализируем дерево
    initialize_tree(n, edges)

    # Выполняем запросы
    results = []
    for u, v in queries:
        result = get_distance(u, v)
        results.append(result)

    end_time = time.time()
    end_memory = get_memory_usage()

    execution_time = (end_time - start_time) * 1000  # в миллисекундах
    memory_used = end_memory - start_memory

    execution_times.append(execution_time)
    memory_usages.append(memory_used if memory_used > 0 else 0.000001)

    # Проверка корректности
    is_correct = results == expected_results
    correctness = "✓ Корректно" if is_correct else "✗ Ошибка"

    if is_correct:
        passed_tests += 1

    # Форматируем вывод
    expected_display = str(expected_results)
    result_display = str(results)

    # Сокращаем длинные списки
    if len(expected_display) > 15:
        expected_display = f"{expected_results[:2]}...({len(expected_results)} запр.)"
    if len(result_display) > 15:
        result_display = f"{results[:2]}...({len(results)} запр.)"

    print(f"{description:<40} | {expected_display:<15} | {result_display:<15} | {correctness:<15} | {execution_time:<12.3f} | {memory_used:<10.6f}")

print("-" * 120)

# Итоговая статистика
max_time = max(execution_times)
max_memory = max(memory_usages)
time_ok = max_time < 2000
memory_ok = max_memory < 64

print(f"ИТОГО: {passed_tests}/{total_tests} тестов пройдено успешно")
print(f"ОГРАНИЧЕНИЯ: Время < 2000 мс ({'✓' if time_ok else '✗'}) | Память < 64 Мб ({'✓' if memory_ok else '✗'})")
print("=" * 120)

# Дополнительная статистика
avg_time = sum(execution_times) / len(execution_times)
min_time = min(execution_times)

print(f"\nСТАТИСТИКА ПРОИЗВОДИТЕЛЬНОСТИ:")
print(f"Среднее время: {avg_time:.3f} мс")
print(f"Минимальное время: {min_time:.3f} мс")
print(f"Максимальное время: {max_time:.3f} мс")
print(f"Максимальная память: {max_memory:.6f} Мб")

# Информация о тестах
max_vertices = max(tc[0] for tc in test_cases)
max_queries = max(len(tc[2]) for tc in test_cases)
total_queries = sum(len(tc[2]) for tc in test_cases)

print(f"\nИНФОРМАЦИЯ О ТЕСТАХ:")
print(f"Всего тестов: {total_tests}")
print(f"Максимальное количество вершин: {max_vertices}")
print(f"Максимальное количество запросов в одном тесте: {max_queries}")
print(f"Общее количество запросов: {total_queries}")

print(f"\nРЕЗУЛЬТАТ: {'✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if passed_tests == total_tests else f'✗ ОШИБОК: {total_tests - passed_tests}'}")
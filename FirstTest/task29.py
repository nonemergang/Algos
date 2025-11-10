adj = []        # Список смежности
dist = []       # Расстояние от корня
depth = []      # Глубина вершины
up = []         # Таблица предков
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
    # Сохраняем данные для текущей вершины
    depth[v] = d
    dist[v] = dist_from_root
    up[v][0] = parent

    # Заполняем таблицу предков
    # up[v][i] = предок вершины v на расстоянии 2^i
    for i in range(1, LOG):
        if up[v][i-1] != -1:
            # Предок на 2^i = предок предка на 2^(i-1)
            up[v][i] = up[up[v][i-1]][i-1]

    # Обходим всех соседей
    for neighbor, weight in adj[v]:
        if neighbor != parent:  # Не идём обратно к родителю
            dfs(neighbor, v, d + 1, dist_from_root + weight)


def get_lca(u, v):
    """
    Находит наименьшего общего предка вершин u и v
    Возвращает номер вершины-предка
    """
    # Делаем так, чтобы u была глубже
    if depth[u] < depth[v]:
        u, v = v, u

    # Поднимаем u на уровень v
    diff = depth[u] - depth[v]

    # Разбиваем diff на степени двойки и прыгаем
    for i in range(LOG):
        if (diff >> i) & 1:  # Проверяем i-й бит числа diff
            u = up[u][i]

    # Если вершины совпали, одна была предком другой
    if u == v:
        return u

    # Поднимаем обе вершины одновременно
    # Идём от больших прыжков к маленьким
    for i in range(LOG - 1, -1, -1):
        if up[u][i] != up[v][i]:  # Если предки разные
            u = up[u][i]           # Прыгаем!
            v = up[v][i]

    return up[u][0]


def get_distance(u, v):
    """
    Вычисляет расстояние между вершинами u и v
    Формула: dist[u] + dist[v] - 2 * dist[lca]
    """
    if u == v:
        return 0
    lca = get_lca(u, v)
    return dist[u] + dist[v] - 2 * dist[lca]


def main():
    global adj, dist, depth, up, LOG

    # Читаем количество вершин
    n = int(input())

    # Вычисляем LOG (максимальная степень двойки)
    LOG = 1
    while (1 << LOG) < n:  # 1 << LOG это 2^LOG
        LOG += 1
    LOG += 1

    # Инициализируем массивы
    adj = [[] for _ in range(n)]
    dist = [0] * n
    depth = [0] * n
    up = [[-1] * LOG for _ in range(n)]

    # Читаем рёбра
    for _ in range(n - 1):
        line = input().split()
        u = int(line[0])
        v = int(line[1])
        w = int(line[2])
        add_edge(u, v, w)

    # Строим дерево с корнем в вершине 0
    dfs(0, -1, 0, 0)

    # Читаем количество запросов
    m = int(input())

    # Обрабатываем запросы
    for _ in range(m):
        line = input().split()
        u = int(line[0])
        v = int(line[1])
        print(get_distance(u, v))


if __name__ == "__main__":
    main()
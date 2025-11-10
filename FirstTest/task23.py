def my_split(text, delimiter=" "):
    parts = []
    current = ""
    for char in text:
        if char == delimiter:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts

def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def better(a, b):
    # 1. Сравниваем по количеству решённых задач
    if a[1] != b[1]:
        return a[1] > b[1]
    # 2. Если задачи равны,ф сравниваем по штрафу
    if a[2] != b[2]:
        return a[2] < b[2]
    # 3. Если и штрафы равны, сравниваем логины лексикографически
    return a[0] < b[0]


def sift_down(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Проверяем, существует ли левый потомок и лучше ли он текущего элемента
    if left < n and better(arr[left], arr[largest]):
        largest = left

    # Проверяем, существует ли правый потомок и лучше ли он текущего лучшего
    if right < n and better(arr[right], arr[largest]):
        largest = right

    # Если нашли потомка, который лучше текущего элемента
    if largest != i:
        # Меняем местами текущий элемент с лучшим потомком
        arr[i], arr[largest] = arr[largest], arr[i]
        # Рекурсивно продолжаем для нового положения элемента
        sift_down(arr, n, largest)





def build_heap(arr):
    n = my_len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)


def heap_sort(arr):
    n = my_len(arr)
    # Превращаем массив в кучу
    build_heap(arr)

    # Последовательно извлекаем элементы из кучи
    for i in range(n-1, 0, -1):
        # Меняем местами корень (максимальный элемент) с последним элементом кучи
        # Теперь максимальный элемент находится на своём окончательном месте в конце массива
        arr[0], arr[i] = arr[i], arr[0]
        # Восстанавливаем свойства кучи для оставшейся части (размер i)
        # Просеиваем новый корень вниз, но только до i-го элемента
        sift_down(arr, i, 0)

def main():
    n = int(input())
    particians = [] # Создаём пустой список для хранения участников
    for i in range(n):
        line = my_split(input())
        login = line[0] # Логин
        solved = int(line[1]) # Решенные задачи
        penalty = int(line[2]) # Штрафы

        particians.append((login, solved,penalty))
    # Сортируем массив участников пирамидальной сортировкой
    heap_sort(particians)
    # После heap_sort массив отсортирован от худшего к лучшему
    # Но нам нужно вывести от лучшего к худшему, поэтому идём с концп
    for i in range(n-1, -1, -1):
        print(particians[i][0])

if __name__ == "__main__":
    main()
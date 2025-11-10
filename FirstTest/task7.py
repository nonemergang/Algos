
def my_abs(x):
    return x if x >= 0 else -x

def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

def my_split(text, delimiter=" "):
    parts = []
    current = ""
    for char in text:
        if char == delimiter:
            if current != "":
                parts.append(current)
                current = ""
        else:
            current += char
    if current != "":
        parts.append(current)
    return parts


def heap_algorithm():
    # Основная логика алгоритма
    n = int(input())
    stones_str = input()

    stones_list = my_split(stones_str)

    stones = []
    total = 0
    for stone_str in stones_list:
        weight = int(stone_str)
        stones.append(weight)
        total += weight

    can_make = [False] * (total + 1)
    can_make[0] = True

    for weight in stones:
        for s in range(total, weight - 1, -1):
            if can_make[s - weight]:
                can_make[s] = True

    answer = total
    for s in range(total + 1):
        if can_make[s]:
            diff = my_abs(total - 2 * s)
            if diff < answer:
                answer = diff

    return answer

print(heap_algorithm())

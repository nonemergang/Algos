def get_char_index(char):
    """получение индекса буквы"""
    if char == 'A': return 0
    if char == 'B': return 1
    if char == 'C': return 2
    if char == 'D': return 3
    if char == 'E': return 4
    if char == 'F': return 5
    if char == 'G': return 6
    if char == 'H': return 7
    if char == 'I': return 8
    if char == 'J': return 9
    if char == 'K': return 10
    if char == 'L': return 11
    if char == 'M': return 12
    if char == 'N': return 13
    if char == 'O': return 14
    if char == 'P': return 15
    if char == 'Q': return 16
    if char == 'R': return 17
    if char == 'S': return 18
    if char == 'T': return 19
    if char == 'U': return 20
    if char == 'V': return 21
    if char == 'W': return 22
    if char == 'X': return 23
    if char == 'Y': return 24
    return 25


def counting_sort(arr):
    """сортировка подсчетом"""
    count = [0] * 26

    for char in arr:
        count[get_char_index(char)] += 1

    # Собираем строку вручную
    result_chars = []
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Проходим по всем буквам алфавита
    for i in range(26):
        cnt = count[i]
        # Пропускаем нулевые значения
        if cnt > 0:
            char_str = chars[i]
            for j in range(cnt):
                result_chars.append(char_str)

    # Собираем строку
    result = ''

    for char in result_chars:
        result += char
    return result

def main():
    # Ввод данных
    n = int(input().strip())
    words = []
    # Считываем слова
    for i in range(n):
        words.append(input().strip())

    complexes = {}
    count = 0

    for word in words:
        sorted_word = counting_sort(word)

        # Проверяем есть ли уже такой ключ
        key_exists = False
        # Проходим по словарю и ищем ключ
        for key in complexes:
            # Если ключ уже есть, увеличиваем значение на 1
            if key == sorted_word:
                complexes[key] += 1
                key_exists = True
                break
        # Если ключа нет, добавляем его
        if not key_exists:
            complexes[sorted_word] = 1
            count += 1

    print(count)

if __name__ == '__main__':
    main()
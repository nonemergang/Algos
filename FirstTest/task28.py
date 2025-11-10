def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count


def count_comments_and_strings(text):
    count1 = 0  # Комментарии (* *)
    count2 = 0  # Комментарии { }
    count3 = 0  # Комментарии //
    string_count = 0  # Строковые литералы

    i = 0
    n = my_len(text)

    while i < n:
        # Обработка строковых литералов
        if text[i] in ["'", "‘", "’", "`", "´"]:  # Разные типы кавычек
            string_count += 1
            i += 1
            # Пропускаем всё до следующей кавычки
            while i < n and text[i] not in ["'", "‘", "’", "`", "´"]:
                i += 1
            if i < n:
                i += 1
            continue

        # Комментарии (* *)
        elif i + 1 < n and text[i] == '(' and text[i+1] == '*':
            count1 += 1
            i += 2

            # Ищем конец комментария *)
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

        # Обычный символ
        else:
            i += 1

    return count1, count2, count3, string_count


def main():
    print("ctrl+d, чтобы завершить ввод")

    input_text = ""

    try:
        while True:
            line = input()
            input_text += line + "\n"
    except EOFError:
        pass

    result = count_comments_and_strings(input_text)
    print(f"{result[0]} {result[1]} {result[2]} {result[3]}")


if __name__ == "__main__":
    main()
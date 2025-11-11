def is_match(text, pattern):
    # Создаем таблицу dp[i][j] - соответствует ли text[0:i] pattern[0:j]
    dp = [[False] * (len(pattern) + 1) for _ in range(len(text) + 1)]

    # Пустая строка соответствует пустому шаблону
    dp[0][0] = True

    # Обрабатываем случай, когда шаблон начинается с *
    for j in range(1, len(pattern) + 1):
        if pattern[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, len(text) + 1):
        for j in range(1, len(pattern) + 1):
            if pattern[j-1] == '*':
                # * может соответствовать 0 символов или 1+ символов
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif pattern[j-1] == '?' or pattern[j-1] == text[i-1]:
                # ? соответствует любому одному символу
                # обычный символ должен совпадать
                dp[i][j] = dp[i-1][j-1]

    return dp[len(text)][len(pattern)]

# Чтение входных данных
text = input().strip()
pattern = input().strip()

# Проверка и вывод результата
if is_match(text, pattern):
    print("YES")
else:
    print("NO")
def sin_approx(degrees):
    """Приближенное вычисление синуса через ряд Тейлора"""
    # Переводим градусы в радианы
    radians = degrees * 3.14159 / 180

    # Ряд Тейлора для синуса
    result = 0
    term = radians
    for n in range(10):
        result += term
        term = -term * radians * radians / ((2*n + 2) * (2*n + 3))

    return result

# Вывод таблицы
print("Таблица синусов:")
print("=" * 20)
for degrees in range(0, 91, 5):
    sin_value = sin_approx(degrees)
    print(f"sin({degrees}°) = {sin_value:.4f}")

print(sum([ord(s) for s in "DanilMannanov"])%10)
import random
from typing import List, Tuple

def fractional_knapsack(items: List[Tuple[float, float]], max_weight: float) -> Tuple[List[Tuple], float, float]:

    # Создаём список с удельной стоимостью: (вес, стоимость, удельная_стоимость)
    sorted_items = []
    for weight, value in items:
        if weight == 0:
            # Избегаем деления на ноль
            specific_value = float('inf')
        else:
            specific_value = value / weight
        sorted_items.append((weight, value, specific_value))

    # Сортируем по убыванию удельной стоимости
    sorted_items.sort(key=lambda x: x[2], reverse=True)

    total_weight = 0.0
    total_value = 0.0
    result = []

    for w, v, s in sorted_items:
        if total_weight + w <= max_weight:
            # Берём весь предмет
            result.append((w, v, s))
            total_weight += w
            total_value += v
        else:
            # Берём часть (только для дробной задачи)
            available_weight = max_weight - total_weight
            if w > 0:
                fractional_value = v * (available_weight / w)
                result.append((available_weight, fractional_value, s))  # часть предмета
                total_weight += available_weight
                total_value += fractional_value
            break  # Рюкзак заполнен

    return result, total_weight, total_value

# === Пример использования ===
if __name__ == "__main__":
    # Генерация случайных предметов: (вес, стоимость)
    random.seed(42)  # Для воспроизводимости
    backpack_items: List[Tuple[float, float]] = [
        (random.randint(1, 20), random.randint(10, 100)) for _ in range(10)
    ]

    max_capacity = 50

    print("Предметы (вес, стоимость):")
    for i, (w, v) in enumerate(backpack_items):
        print(f"{i+1}: вес={w}, стоимость={v}, уд.стоимость={v/w:.2f}")

    selected, total_w, total_v = fractional_knapsack(backpack_items, max_capacity)

    print(f"\nРюкзак заполнен на {total_w:.2f} из {max_capacity}")
    print(f"Общая стоимость: {total_v:.2f}")
    print("Выбранные предметы (вес, стоимость, уд.стоимость):")
    for item in selected:
        print(f"  Вес: {item[0]:.2f}, Стоимость: {item[1]:.2f}, Уд.стоимость: {item[2]:.2f}")
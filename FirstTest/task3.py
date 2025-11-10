#Считываем всю строку
numbers = input()


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

numbers = my_split(numbers)


#Находим, где находится A и заканчивается B
zero_count = 0
a = []
b = []


def my_len(collection):
    count = 0
    for _ in collection:
        count += 1
    return count

for num in numbers:
    if num == '0':
        zero_count += 1
        continue
    if zero_count == 0:
        a.append(int(num)) #Добавляем до тех пор, пока не увидели 0
    elif zero_count == 1:
        b.append(int(num)) #Увидели 0, начинаем добавлять в список B

result = []
for x in a:
    if x not in b: #Проверяем, есть ли элемент списка A в списке B
        result.append(x)
for x in b:
    if x not in a: #Аналогично, проверяем начилие элемента списка B в списке A
        result.append(x)

#Сортировка пузырьком
def sort_bubble(a):
    sorted_flag = False # флаг, отсортирован ли массив
    n = my_len(a)
    while not sorted_flag:
        sorted_flag = True # Перед каждым проходом предполагаем, что массив уже отсортирован
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
sort_bubble(result)
if result:
    output = str(result[0])
    for i in range(1, my_len(result)):
        output += " " + str(result[i])
    print(output)
else:
    print('0')
n = int(input())
phone_book = {}
for _ in range(n):
    command = input().split()

    # Добавление пользователя
    if command[0] == 'ADD':
        user, number = command[1], command[2]
        if user in phone_book:
            print('ERROR')
        else:
            phone_book[user] = number

    #Удаление пользователя
    if command[0] == 'DELETE':
        user = command[1]
        if user not in phone_book:
            print('ERROR')
        else:
            del phone_book[user]

    #Редактирование номера телефона
    if command[0] == 'EDITHPHONE':
        user, number = command[1], command[2]
        if user not in phone_book:
            print('ERROR')
        else:
            phone_book[user] = number

    #Вывод номера телефона
    elif command[0] == 'PRINT':
        user = command[1]
        if user not in phone_book:
            print('ERROR')
        else:
            print(f"{user} {phone_book[user]}")





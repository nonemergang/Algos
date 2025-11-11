"""
Задача 9. Телефонная книга
Ограничение по времени: 2 секунды
Ограничение по памяти: 64 мегабайта
Необходимо разработать программу, которая является промежуточным звеном в
реализации телефонной книги. На вход подается N ≤  1000 команд вида
ADD User Number
DELETE User
EDITPHONE User Number
PRINT User
Согласно этим командам нужно соответственно добавить пользователя в
телефонную книгу, удалить пользователя, изменить его номер и вывести на экран его
данные. В случае невозможности выполнить действие, необходимо вывести ERROR.
Добавлять пользователя, уже существующего в телефонной книге, нельзя.
Необходимо вывести протокол работы телефонной книги
"""


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





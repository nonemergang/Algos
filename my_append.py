from my_len import my_len as my_len

def my_append(lst, element):
    lst[my_len(lst):] = [element]
    return lst


my_list = [1, 2, 3]
my_append(my_list, 4)
print(my_list)  # [1, 2, 3, 4]
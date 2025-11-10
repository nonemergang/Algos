from my_len import my_len as my_len

def broken_search():
    target = int(input())
    numss = input().split()
    nums = []
    for i in numss:
        nums += [int(i)]
    left = 0
    right = my_len(nums) - 1
    while left <= right:
        mid = (left + right) // 2


        # Если нашли элемент - возвращаем индекс
        if nums[mid] == target:
            return mid

        # Проверяем, какая половина отсортирована
        if nums[left] <= nums[mid]:
            # Левая половина отсортирована
            if nums[left] <= target < nums[mid]:
                # Искомый элемент в отсортированной левой половине
                right = mid - 1
            else:
                # Искомый элемент в правой половине
                left = mid + 1
        else:
            # Правая половина отсортирована
            if nums[mid] < target <= nums[right]:
                # Искомый элемент в отсортированной правой половине
                left = mid + 1
            else:
                # Искомый элемент в левой половине
                right = mid - 1

    return -1

print(broken_search())


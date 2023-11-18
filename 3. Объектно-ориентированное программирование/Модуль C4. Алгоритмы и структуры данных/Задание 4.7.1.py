def find(array_, element_):
    for i, a in enumerate(array_):
        if a == element_:
            return i
    return False


array = [x for x in range(15)]
element = int(input())

print(find(array, element))


def count(array_, element_):
    count_ = 0
    for a in array_:
        if a == element_:
            count_ += 1
    return count_


# Двоичный поиск
def binary_search(array_, element_, left, right):
    if left > right:  # если левая граница превысила правую,
        return False  # значит, элемент отсутствует

    middle = (right + left) // 2  # находим середину
    if array_[middle] == element_:  # если элемент в середине
        return middle  # возвращаем этот индекс
    elif element_ < array_[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return binary_search(array_, element_, left, middle - 1)
    else:  # иначе в правой
        return binary_search(array_, element_, middle + 1, right)


element = int(input())
array = [i for i in range(1, 100)]  # 1,2,3,4,...

# запускаем алгоритм на левой и правой границе
print(binary_search(array, element, 0, 99))

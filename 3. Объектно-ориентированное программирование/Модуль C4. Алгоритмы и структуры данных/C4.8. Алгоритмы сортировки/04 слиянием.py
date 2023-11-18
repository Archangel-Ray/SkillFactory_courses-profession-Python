array = [2, 3, 1, 4, 6, 5, 9, 8, 7]


def merge_sort(piece):  # «разделяй»
    if len(piece) < 2:  # если кусок массива равен 2,
        return piece[:]  # выходим из рекурсии
    else:
        middle = len(piece) // 2  # ищем середину
        left = merge_sort(piece[:middle])  # рекурсивно делим левую часть
        right = merge_sort(piece[middle:])  # и правую
        return merge(left, right)  # выполняем слияние


def merge(left, right):  # «властвуй»
    result = []  # результирующий массив
    i, j = 0, 0  # указатели на элементы

    # пока указатели не вышли за границы
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # добавляем хвосты
    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


print(array)

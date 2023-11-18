from random import choice
array = [2, 3, 1, 4, 6, 5, 9, 8, 7]


def qsort(array_, left, right):
    p = choice(array_[left:right + 1])
    i, j = left, right
    while i <= j:
        while array_[i] < p:
            i += 1
        while array_[j] > p:
            j -= 1
        if i <= j:
            array_[i], array_[j] = array_[j], array_[i]
            i += 1
            j -= 1

    if j > left:
        qsort(array_, left, j)
    if right > i:
        qsort(array_, i, right)


qsort(array, 0, len(array) - 1)
print(array)

def binary(a, b):
    """Каждый элемент меньшего массива ищем бинарным поиском в большем.
    Время O(M log N), память O(1)."""
    if len(a) > len(b):
        a, b = b, a
    for x in a:
        l = 0
        r = len(b) - 1
        while l <= r:
            m = (l + r) // 2
            if b[m] == x:
                return True
            if b[m] < x:
                l = m + 1
            else:
                r = m - 1
    return False

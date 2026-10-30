def exponential(a, b):
    """Как два указателя, но по большему массиву идём экспоненциальным поиском.
    Время O(M log(2N/M)), память O(1)."""
    if len(a) > len(b):
        a, b = b, a
    start = 0                      # всё, что левее start в b, уже меньше текущего x
    for x in a:
        if start >= len(b):
            return False
        # 1) прыжки 1, 2, 4, 8, ... от start, пока b[start + step] < x
        step = 1
        while start + step < len(b) and b[start + step] < x:
            step *= 2
        # 2) x может лежать только между start + step//2 и start + step
        l = start + step // 2
        r = min(start + step, len(b) - 1)
        # 3) обычный бинарный поиск на этом маленьком отрезке
        while l <= r:
            m = (l + r) // 2
            if b[m] == x:
                return True
            if b[m] < x:
                l = m + 1
            else:
                r = m - 1
        start = l                  # l = место x в b, следующий x будет не меньше
    return False

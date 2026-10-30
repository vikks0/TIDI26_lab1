def double_binary(a, b):
    """Бинарный поиск с разделением.
    Время O(M log(2N/M)), память O(log M) (стек рекурсии)."""
    if len(a) > len(b):
        a, b = b, a

    def check(a_l, a_r, b_l, b_r):
        # кусок a или кусок b пустой: общих элементов нет
        if a_l > a_r or b_l > b_r:
            return False

        md = (a_l + a_r) // 2      # середина куска a
        x = a[md]

        # обычный бинарный поиск x в куске b
        l = b_l
        r = b_r
        while l <= r:
            m = (l + r) // 2
            if b[m] == x:
                return True
            if b[m] < x:
                l = m + 1
            else:
                r = m - 1

        # x не нашли, l = место x в b: слева меньшие, справа большие
        if check(a_l, md - 1, b_l, l - 1):
            return True
        if check(md + 1, a_r, l, b_r):
            return True
        return False

    return check(0, len(a) - 1, 0, len(b) - 1)

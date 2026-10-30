def two_pointers(a, b):
    """Два указателя. Время O(M+N), память O(1)."""
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            return True
        if a[i] < b[j]:
            i += 1
        else:
            j += 1
    return False

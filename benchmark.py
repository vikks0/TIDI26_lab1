import csv
import time

from algorithms import ALGORITHMS
from generate import worst_case

REPEATS = 5   # сколько раз измеряем; берём минимум, он меньше всего зависит от шума


def measure(f, a, b):
    best = None
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        f(a, b)
        t = time.perf_counter() - t0
        if best is None or t < best:
            best = t
    return best


def scenarios():
    """Список (название серии, M, N)."""
    result = []
    # 1) массивы одного размера
    n = 64
    while n <= 262144:
        result.append(("equal", n, n))
        n *= 2
    # 2) M фиксировано, N растёт
    n = 64
    while n <= 1048576:
        result.append(("fixed_m", 50, n))
        n *= 2
    # 3) N = M * ratio, M фиксировано
    ratio = 1
    while ratio <= 1024:
        result.append(("ratio", 1000, 1000 * ratio))
        ratio *= 2
    return result


def run(path="data/results.csv"):
    rows = []
    for series, m, n in scenarios():
        a, b = worst_case(m, n)
        for name, f in ALGORITHMS.items():
            t = measure(f, a, b)
            rows.append([series, m, n, name, t])
            print(f"{series:8} M={m:<8} N={n:<9} {name:14} {t:.6f} c")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["series", "M", "N", "algorithm", "seconds"])
        w.writerows(rows)


if __name__ == "__main__":
    run()

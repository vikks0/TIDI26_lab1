import random
import unittest

from algorithms import ALGORITHMS


def expected(a, b):
    """Эталон: самый простой способ через множества."""
    return len(set(a) & set(b)) > 0


class TestExamples(unittest.TestCase):
    """Примеры и крайние случаи, посчитанные вручную."""

    CASES = [
        ([1, 2, 3], [3, 4, 5], True),          # пример из задания
        ([2, 4, 6], [3, 5, 7], False),         # пример из задания
        ([], [], False),                       # пример из задания
        ([], [1, 2], False),                   # один пустой
        ([1, 2], [], False),
        ([5], [5], True),                      # по одному элементу
        ([5], [6], False),
        ([1], [1, 2, 3, 4, 5], True),          # совпадение в начале
        ([5], [1, 2, 3, 4, 5], True),          # совпадение в конце
        ([3], [1, 2, 3, 4, 5], True),          # совпадение в середине
        ([1, 2, 3, 4, 5], [5], True),          # первый массив длиннее
        ([1, 1, 1], [1], True),                # повторы
        ([1, 1, 2], [3, 3], False),
        ([-5, -3, 0], [-3, 7], True),          # отрицательные числа
        ([-5, -4], [-3, -2], False),
        ([1, 3, 5, 7], [2, 4, 6, 8], False),   # чётные и нечётные
        ([1, 3, 5, 7], [2, 4, 6, 7], True),
        ([10**18, 10**18 + 2], [10**18 + 1, 10**18 + 3], False),   # огромные
        ([10**18, 10**18 + 2], [10**18 + 2, 10**30], True),
        ([1, 2, 3], [1, 2, 3], True),          # массивы полностью совпадают
        ([7], [1, 3, 5, 7, 9, 11, 13], True),  # общих элементов ровно один в конце
        ([1, 3, 5], [2, 4, 6, 8, 10], False),  # нечётные против чётных, границы рядом
    ]

    def test_cases(self):
        for name, f in ALGORITHMS.items():
            for a, b, want in self.CASES:
                with self.subTest(algorithm=name, a=a, b=b):
                    self.assertEqual(f(a, b), want)


class TestRandom(unittest.TestCase):
    """Много случайных массивов: сравниваем с эталоном через множества."""

    def make(self, rng, max_len, max_val):
        m = rng.randint(0, max_len)
        n = rng.randint(0, max_len)
        a = sorted(rng.randint(-max_val, max_val) for _ in range(m))
        b = sorted(rng.randint(-max_val, max_val) for _ in range(n))
        return a, b

    def test_random_small_values(self):
        # маленький диапазон значений: совпадения и повторы встречаются часто
        rng = random.Random(1)
        for _ in range(3000):
            a, b = self.make(rng, 12, 15)
            for name, f in ALGORITHMS.items():
                with self.subTest(algorithm=name, a=a, b=b):
                    self.assertEqual(f(a, b), expected(a, b))

    def test_random_big_values(self):
        # большой диапазон: совпадений мало, больше ответов False
        rng = random.Random(2)
        for _ in range(1500):
            a, b = self.make(rng, 60, 10**18)
            for name, f in ALGORITHMS.items():
                with self.subTest(algorithm=name):
                    self.assertEqual(f(a, b), expected(a, b))

    def test_random_unbalanced(self):
        # очень разные длины: M мало, N много
        rng = random.Random(3)
        for _ in range(500):
            m = rng.randint(1, 5)
            n = rng.randint(100, 400)
            a = sorted(rng.randint(0, 1000) for _ in range(m))
            b = sorted(rng.randint(0, 1000) for _ in range(n))
            for name, f in ALGORITHMS.items():
                with self.subTest(algorithm=name):
                    self.assertEqual(f(a, b), expected(a, b))
                    self.assertEqual(f(b, a), expected(a, b))   # и наоборот


    def test_random_large(self):
        # крупные массивы (1000 и 100 000 элементов), как в замерах
        rng = random.Random(4)
        for _ in range(5):
            a = sorted(rng.randint(0, 10**6) for _ in range(1000))
            b = sorted(rng.randint(0, 10**6) for _ in range(100000))
            want = expected(a, b)
            for name, f in ALGORITHMS.items():
                with self.subTest(algorithm=name):
                    self.assertEqual(f(a, b), want)
                    self.assertEqual(f(b, a), want)   # и наоборот


class TestInputs(unittest.TestCase):
    """Алгоритмы не должны менять входные массивы."""

    def test_inputs_unchanged(self):
        rng = random.Random(5)
        for _ in range(200):
            a = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 30)))
            b = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 30)))
            for name, f in ALGORITHMS.items():
                aa, bb = list(a), list(b)           # копии на вход
                f(aa, bb)
                with self.subTest(algorithm=name):
                    self.assertEqual(aa, a)          # исходные не изменились
                    self.assertEqual(bb, b)


class TestWorstCase(unittest.TestCase):
    """Тестовые данные для замеров: общих элементов нет, ответ всегда False."""

    def test_generated(self):
        from generate import worst_case
        for m, n in [(1, 1), (1, 1000), (50, 50), (50, 5000), (1000, 1000)]:
            a, b = worst_case(m, n)
            self.assertEqual(a, sorted(a))
            self.assertEqual(b, sorted(b))
            self.assertFalse(expected(a, b))
            for name, f in ALGORITHMS.items():
                with self.subTest(algorithm=name, m=m, n=n):
                    self.assertFalse(f(a, b))


if __name__ == "__main__":
    unittest.main()

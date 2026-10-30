import unittest

import benchmark
import plot

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise SystemExit("Тесты не прошли, замеры не запускаем")
    benchmark.run()
    plot.make_plots()

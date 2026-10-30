import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(path="data/results.csv"):
    data = defaultdict(lambda: defaultdict(list))   # series -> algorithm -> [(M, N, t)]
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            data[row["series"]][row["algorithm"]].append(
                (int(row["M"]), int(row["N"]), float(row["seconds"])))
    return data


def draw(series_data, x_index, xlabel, title, out, ratio=False):
    plt.figure(figsize=(8, 5))
    for name, pts in series_data.items():
        if ratio:
            xs = [n / m for m, n, _ in pts]
        else:
            xs = [p[x_index] for p in pts]
        ys = [p[2] for p in pts]
        plt.plot(xs, ys, marker="o", label=name)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(xlabel)
    plt.ylabel("время, с")
    plt.title(title)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()


def make_plots():
    data = load()
    draw(data["equal"], 1, "N = M", "Массивы одинакового размера", "plots/equal_sizes.png")
    draw(data["fixed_m"], 1, "N (M = 50)", "M фиксировано, N растёт", "plots/fixed_m.png")
    draw(data["ratio"], 1, "N / M (M = 1000)", "Зависимость от соотношения N / M",
         "plots/varying_ratio.png", ratio=True)


if __name__ == "__main__":
    make_plots()

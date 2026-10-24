import sys
import os
import csv

if len(sys.argv) < 2:
    print("Usage: python render_plot.py <file.csv>")
    sys.exit(1)

fname = sys.argv[1]

if not os.path.exists(fname):
    print(f"File not found: {fname}")
    print(f"cwd = {os.getcwd()}")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed. Run: py -3 -m pip install matplotlib")
    sys.exit(1)

tau, u, y = [], [], []
with open(fname, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tau.append(int(row["tau"]))
        u.append(float(row["u"]))
        y.append(float(row["y"]))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tau, y, "b-o", markersize=3, linewidth=1.5, label="y(tau)")
ax.set_xlabel("tau")
ax.set_ylabel("y", color="b")
ax.tick_params(axis="y", labelcolor="b")
ax.grid(True, alpha=0.3)
ax.set_title(os.path.basename(fname))

ax2 = ax.twinx()
ax2.plot(tau, u, "r--", linewidth=1.2, label="u(tau)")
ax2.set_ylabel("u", color="r")
ax2.tick_params(axis="y", labelcolor="r")

plt.tight_layout()

base_png = fname.replace(".csv", ".png")
out_png = base_png

try:
    plt.savefig(out_png, dpi=150)
except PermissionError:
    stem, ext = os.path.splitext(base_png)
    for i in range(1, 100):
        candidate = f"{stem}_{i}{ext}"
        try:
            plt.savefig(candidate, dpi=150)
            out_png = candidate
            break
        except PermissionError:
            continue
    else:
        print(f"Cannot save PNG next to {base_png}")
        plt.close()
        sys.exit(1)

plt.close()

abs_png = os.path.abspath(out_png)
print(f"Saved: {abs_png}")

if not os.path.exists(abs_png):
    print("ERROR: file was not created")
    sys.exit(1)
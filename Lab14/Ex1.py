import importlib
import os

packages = ["scipy", "statsmodels", "matplotlib"]
print("=== Package Check ===")
for pkg in packages:
    try:
        mod = importlib.import_module(pkg)
        print(f"  {pkg}: INSTALLED (version {mod.__version__})")
    except ImportError:
        print(f"  {pkg}: NOT INSTALLED")
print()

import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6]
y = [150, 200, 180, 250, 300, 275]

x2 = [1, 2, 3, 4, 5, 6]
y2 = [100, 160, 210, 230, 260, 310]

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color="steelblue", label="Dataset 1")
plt.plot(x2, y2, color="coral", label="Dataset 2")
plt.title("Sample Data")
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
chart_path = os.path.join(os.path.dirname(__file__), "sales_chart.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")

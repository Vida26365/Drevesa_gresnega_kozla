# benchmark.py
import time
import math

INPUT_FILE = "testcase2.txt"
OUTPUT_FILE = "results2.csv"

from kozel import GresniKozel,Node
# ---------- LOAD OPERATIONS ----------
def load_ops():
    ops = []
    with open(INPUT_FILE, "r") as f:
        n = int(f.readline())
        for _ in range(n):
            op, val = f.readline().split()
            ops.append((op, int(val)))
    return ops

# ---------- RUN BENCHMARK ----------
def run():
    ops = load_ops()

    with open(OUTPUT_FILE, "w") as out:
        out.write("alpha,time_seconds\n")
        alpha = 0.6
        while alpha <= 0.99:
            tree = GresniKozel(alfa=alpha)

            start = time.perf_counter()

            for op, val in ops:
                if op == "insert":
                    tree.insert(val)
                elif op == "remove":
                    tree.remove(val)
                elif op == "find":
                    tree.find(val)

            end = time.perf_counter()
            elapsed = end - start

            print(f"alpha={alpha:.2f} -> {elapsed:.4f}s")
            out.write(f"{alpha:.2f},{elapsed}\n")

            alpha += 0.01

if __name__ == "__main__":
    run()
# generator.py
import random

OUTPUT_FILE = "testcase2.txt"
NUM_OPS = 1_000_000
VALUE_RANGE = 1_000_000

OPS = ["insert", "remove", "find"]

def generate():
    with open(OUTPUT_FILE, "w") as f:
        f.write(str(NUM_OPS) + "\n")
        for _ in range(NUM_OPS):
            op = random.choice(OPS)
            val = random.randint(1, VALUE_RANGE)
            f.write(f"{op} {val}\n")

if __name__ == "__main__":
    generate()
    print(f"Generated {NUM_OPS} operations into {OUTPUT_FILE}")
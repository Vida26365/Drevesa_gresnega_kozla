# plot.py
import matplotlib.pyplot as plt
import csv

INPUT_FILE = "results2.csv"

alphas = []
times = []

with open(INPUT_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        alphas.append(float(row[0]))
        times.append(float(row[1]))

plt.figure()
plt.plot(alphas, times)
plt.xlabel("Alfa")
plt.ylabel("Čas (sekunde)")
plt.title("Drevo grešnega kozla glede na alfo")
plt.grid()

plt.savefig("plot.png")
plt.show()
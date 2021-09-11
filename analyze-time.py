import sys
import json
import matplotlib.pyplot as plt
from numpy.lib.function_base import average

print("cstimer.net time analyzer by @d4rckh")

def log(c, d):
    print(f"[Log] {d}")

try:
    exportName = sys.argv[1]
except IndexError:
    log("e", "Syntax Error; Usage: python analyze-time.py export-name.txt")
    exit()

log('i', f"Reading {exportName} file")
f = open(exportName,)
data = json.load(f)
chartData = []
times = []
chartIndexes = []

sessions = list(filter(lambda key: key.startswith("session"),dict.keys(data)))

sessionNum = input(f"[?] Found {len(sessions)} sessions, which one do you want to analyze? ")
sessionName = 'session'+sessionNum
if not (sessionName in sessions):
    print("Session does not exist")
    exit()
for entry in data[sessionName]:
    times.append(entry[0][1] / 1000)
log('i', f'Found {len(times)} entries, making averages')

doMean=input("[?] Do mean instead of average? (y/n) ")
n=int(input("[?] Chunks of: "))
if doMean == "y" and n<=2:
    log("e", "Can't do mean and have chunks of less or equal than 2")
    exit()
chunks=[times[i:i + n] for i in range(0, len(times), n)]
for chunk in chunks:
    if len(chunk) >= n:
        toAverage = chunk
        if doMean == "y":
            toAverage.remove(max(toAverage))
            toAverage.remove(min(toAverage))
        average = round(sum(toAverage) / len(toAverage), 2)
        
        chartData.append(average)

chartIndexes = list(range(1, len(chartData) + 1))
log('i', 'Generated ' + str(len(chartIndexes)) + ' dots! Plotting data..')
f.close()

plt.plot(chartIndexes,chartData)
plt.title(f"Speed over time (Chunks of {str(n)}; Mean: {doMean})")
plt.xlabel('Index')
plt.ylabel('Time')
log('i', 'Showing table...')
plt.show()

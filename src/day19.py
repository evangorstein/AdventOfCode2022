## Followed the approach of HyperNeutrino (see https://www.youtube.com/watch?v=H3PSODv4nf0)


import sys
import re
from math import ceil


def dfs(bp, maxspend, cache, time, bots, amt):
    
    if time == 0:
        return amt[3]
    
    key = tuple([time, *bots, *amt])
    if key in cache.keys():
        return cache[key]
    
    maxval = amt[3] + bots[3] * time 

    

    for btype, recipe in enumerate(bp):

        if btype  != 3 and bots[btype] >= maxspend[btype]:
            continue 

        wtime = 0
        for r_amt, r_type in recipe:
            if bots[r_type] == 0:
                break
            wtime = max(wtime, ceil((r_amt - amt[r_type]) / bots[r_type]))
        else:
            remtime = time - wtime - 1
            if remtime <= 0:
                continue
            bots_ = bots[:]
            bots_[btype] += 1
            amt_ = [x + (wtime + 1) * y for x, y in zip(amt, bots)]
            for r_amt, r_type in recipe:
                amt_[r_type] -= r_amt
            for i in range(3):
                amt_[i] = min(amt_[i], remtime * maxspend[i])
            maxval = max(maxval, dfs(bp, maxspend, cache, remtime, bots_, amt_))

    cache[key] = maxval
    return maxval


INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day19.txt"
print(f"Data is from {INPUT_PATH}")
print("Now solving part 1...")
total = 0
for i, line in enumerate(open(INPUT_PATH)):
    bp = []
    maxspend = [0, 0, 0]
    for section in line.split(": ")[1].split(". "):
        recipe = []
        for x, y in re.findall(r"(\d+) (\w+)", section):
            x = int(x)
            y = ["ore", "clay", "obsidian"].index(y)
            recipe.append((x, y))
            maxspend[y] = max(x, maxspend[y])
        bp.append(recipe)
    v = dfs(bp, maxspend, {}, 24, [1, 0, 0, 0], [0, 0, 0, 0])
    total += v * (i + 1)
print("Solution to part 1 is", total)
print("Now solving part 2...")
total = 1
for line in list(open(INPUT_PATH))[:3]:
    bp = []
    maxspend = [0, 0, 0]
    for section in line.split(": ")[1].split(". "):
        recipe = []
        for x, y in re.findall(r"(\d+) (\w+)", section):
            x = int(x)
            y = ["ore", "clay", "obsidian"].index(y)
            recipe.append((x, y))
            maxspend[y] = max(x, maxspend[y])
        bp.append(recipe)
    v = dfs(bp, maxspend, {}, 32, [1, 0, 0, 0], [0, 0, 0, 0])
    print("number of geodes for this bp is", v)
    total *= v 
print("Solution to part 2 is", total)
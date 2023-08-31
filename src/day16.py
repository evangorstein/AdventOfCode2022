# Solution shamelessly pieced together from https://pastebin.com/u4crb1Fm
# and https://github.com/mebeim/aoc/blob/master/2022/solutions/day16.py

import sys
import time
from dataclasses import dataclass

INF = int(1e9)
INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day16.txt"

@dataclass
class Valve:
    flow_rate : int
    children : list[str]

def parse_input(puzzle_input: list[str]) -> dict[str, Valve]:

    valves = {}

    for line in puzzle_input:
        split = line.split()
        name = split[1]
        flow_rate = int(split[4].split("=")[1][:-1])
        children = [split[-1]] + [token[:-1] for token in split if token.endswith(",")]
        valves[name] = Valve(flow_rate, children)

    return(valves)

def floid_warshall(valves: dict[str, Valve]) -> dict[str, dict[str, int]]:
    """
    Returns valve-valve distance matrix in the form of a dictionary of dictionaries. 
    Uses floid_warshall algorithm to compute shortest paths.
    """

    dist = {v: {u: INF for u in valves} for v in valves}
 
    for v in valves:
        dist[v][v] = 0
        for u in valves[v].children:
            dist[v][u] = 1
 
    for k in valves:
        for i in valves:
            for j in valves:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
 
    return dist

def gen_options(dist: dict[str, dict[str, int]], all_valve_names: set[str], 
                cur: str, opened: dict[str, int], time: int):
    """
    Iterator over all possible options.
    Doing DFS over a complete graph.
    Each option is a dictionary whose keys are the names of all valves opened for that option. 
    The values are the time remaining when that valve was opened.
    For example, an option could be {"AA" : 30, "BB" : 15}
    This means that "AA" was opened with 30 minutes to go and "BB" was opened with 15 minutes to go
    """
    yield opened 

    for nxt in all_valve_names - opened.keys(): # iterate through all unopened valves
        # get time remaining after traveling to nxt and opening it
        new_time = time - dist[cur][nxt] - 1 
        if new_time <= 0: # no time to open nxt
            continue

        new_cur = nxt
        new_opened = opened.copy()
        new_opened[nxt] = new_time 
        yield from gen_options(dist, all_valve_names, new_cur, new_opened, new_time)

def get_score(option: dict[str, int], valves: dict[str, Valve]) -> int:
    return(sum([option[v]*valves[v].flow_rate for v in option]))

if __name__ == "__main__":  
    print(f"Data is from {INPUT_PATH}")

    with open(INPUT_PATH) as f:
        puzzle_input = f.readlines()
    
    valves = parse_input(puzzle_input)
    dist = floid_warshall(valves)
    nz_valve_names = set([v for v in valves if valves[v].flow_rate > 0])
    all_options = gen_options(dist, nz_valve_names, "AA", {}, 30)
    best = max(get_score(option, valves) for option in all_options)
    print(best)




    
     


import sys
import pathlib
from dataclasses import dataclass

INF = int(1e9)
INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "..data/ex_day16.txt"

@dataclass
class Valve:
    name : str
    flow_rate : int
    children : list[str]


def parse_input(puzzle_input):

    valves = {}

    for line in puzzle_input:
        split = line.split()
        name = split[1]
        flow_rate = int(split[4].split("=")[1][:-1])
        children = [split[-1]] + [token[:-1] for token in split if token.endswith(",")]
        valves[name] = Valve(name, flow_rate, children)

    return(valves)


def floid_warshall(valves):
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



if __name__ == "__main__":  
    print(f"\nData is from {INPUT_PATH}")

    with open(INPUT_PATH) as f:
        puzzle_input = f.readlines()
    
    valves = parse_input(puzzle_input)
    dist = floid_warshall(valves)
    print(dist)
    
     


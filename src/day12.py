#AOC2022/day12.py
import sys
import networkx as nx
import re


def build_graph(lines):
    graph = nx.DiGraph()
    
    for i in range(n):
        for j in range(m):
            
            if (i > 0) and (ord(lines[i][j]) >= ord(lines[i-1][j]) - 1):
                graph.add_edge((i, j), (i-1, j))
            
            if (i < n-1) and (ord(lines[i][j]) >= ord(lines[i+1][j]) - 1):
                graph.add_edge((i, j), (i+1, j))
            
            if (j > 0) and (ord(lines[i][j]) >= ord(lines[i][j-1]) - 1):
                graph.add_edge((i, j), (i, j-1))
            
            if (j < m-1) and (ord(lines[i][j]) >= ord(lines[i][j+1]) - 1):
                graph.add_edge((i, j), (i, j+1))
    
    return graph

def short_path_handle(G, s, e):
    try: 
        return nx.shortest_path(G, s, e)
    except nx.NetworkXNoPath:
        return None

if __name__ == "__main__":

    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day12.txt" 
    print(f"\n{path}:")

    #Get input
    with open(path) as file:
        input = file.read().strip()

    end = input.index("E")
    input = input.replace("E", "z")
    start1 = input.index("S")
    input = input.replace("S", "a")
    starts2 = [ind.start() for ind in re.finditer('a', input)]

    lines = input.split("\n")
    n = len(lines)
    m = len(lines[0])
    end = (end // (m+1), end % (m+1))
    start1 = (start1 // (m+1), start1 % (m+1))
    starts2 = [(ind // (m+1), ind % (m+1)) for ind in starts2]

    graph = build_graph(lines)

    sh_path1 = short_path_handle(graph, start1, end)
    sh_paths2 = [short_path_handle(graph, start, end) for start in starts2]

    print(f"Solution to part 1 is {len(sh_path1) - 1}")
    print(f"Solution to part 2 is {min([len(path) for path in sh_paths2 if path is not None]) -1}")




    






    





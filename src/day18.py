import sys
import numpy as np

def solve_part1(puzzle_input: list[str]):

    sa = 0
    cubes = np.empty((0,3), int)
    for line in puzzle_input:
        new_cube = np.array([int(coord) for coord in line.split(",")])

        # check for adjacent cubes 
        diff = abs(new_cube - cubes)
        adj = (np.sum(diff, axis=1) == 1)
        # add to surface area
        sa += (6 - 2*sum(adj))

        # add new cube to log
        cubes = np.vstack([cubes, new_cube])
            
    #print(cubes)
    return sa
    
def solve_part2(puzzle_input: list[str]):

    cubes = [tuple(map(int, line.split(","))) for line in puzzle_input]
    max_coords = tuple(max(cube[i] for cube in cubes) + 1 for i in range(3))
    min_coords = tuple(min(cube[i] for cube in cubes) -1 for i in range(3))

    def get_nbrs(cube):
        return [tuple(cube[i] + adj[i] for i in range(3)) for adj in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]]

    def in_bounds(cube):
        return all(min_coords[i] <= cube[i] <= max_coords[i] for i in range(3))

    sa = 0 #external surface area
    queue = [max_coords] 
    seen = set()
    while queue:
        cur_cube = queue.pop(0)
        if cur_cube in cubes:
            sa += 1
        elif cur_cube not in seen:
            seen.add(cur_cube)
            for nbr in get_nbrs(cur_cube):
                if in_bounds(nbr):
                    queue.append(nbr)
    return sa 


if __name__ == "__main__":  
    
    INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day18.txt"
    print(f"Data is from {INPUT_PATH}")
    with open(INPUT_PATH) as f:
        puzzle_input = f.readlines()
    print("Now solving part 1...")
    sa = solve_part1(puzzle_input)
    print(sa)
    print("Now solving part 2...")
    sa = solve_part2(puzzle_input)
    print(sa)
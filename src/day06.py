#AOC2022/day06.py
import pathlib 
import sys

def solution():
    
    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1]
    #path = "data/ex_day06.txt"
    print(f"\n{path}:")

    puzzle_input = pathlib.Path(path).read_text().strip()


    for ind in range(14, len(puzzle_input)):
        substr = puzzle_input[(ind-14):ind]
        if len(set(substr)) == 14:
            x = ind
            break
    print(f"Solution is {x}")




if __name__ == "__main__":
    solution()

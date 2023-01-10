#AOC2022/day04.py
import sys


def check(pair: str):
    first, second = pair.split(",")
    
    first = first.split("-")
    second = second.split("-")

    if int(first[0]) > int(second[0]):
        contain = int(first[1]) <= int(second[1])
    elif int(first[0]) < int(second[0]):
        contain = int(first[1]) >= int(second[1])
    else: 
        contain = True

    if int(first[0]) > int(second[1]) or int(first[1]) < int(second[0]):
        overlap = False
    else:
        overlap = True
    
    return contain, overlap

def solution():
    
    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1]
    #path = "data/day04.txt"
    print(f"\n{path}:")
    
    part1 = 0
    #Compute solutions to part1 and part2
    part1, part2 = 0, 0
    with open(path, 'r') as file:

        for line in file:
            contain, overlap = check(line.strip())
            part1 += contain
            part2 += overlap
    
    print(part1)
    print(part2)

if __name__ == "__main__":
    
    solution()





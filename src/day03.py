#AOC2022/day03.py
import sys
from itertools import islice

def ord_to_priority(ord):
    """Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52."""
    
    if common_item < 91: #Capital letters (65-90)
        priority = common_item - 38
    else: #lower case letter (97-122)
        priority = common_item - 96


def get_priority1(rucksack: str):
    len_comp = len(rucksack)//2
    comp1 = rucksack[:len_comp]
    comp2 = rucksack[len_comp:]

    #Get common character, should be a singleton
    common_item = set(comp1) & set(comp2) 
    
    #Converts to ACSI value
    common_item = ord(list(common_item)[0])

    return ord_to_priority(ord)


def get_priority2(rucksacks: list[str]):

    #Get rid of the newline character at the end of each rucksack
    rucksacks = [rucksack.strip() for rucksack in rucksacks]

    #Get common character among the three rucksacks, should be singleton
    common_item = set(rucksacks[0]) & set(rucksacks[1]) & set(rucksacks[2])

    #Converts to ACSI value
    common_item = ord(list(common_item)[0])

    return ord_to_priority(ord)


def solution():
    
    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1]
    #path = "data/day03.txt"
    print(f"\n{path}:")
    
    #Compute solutions to part1 and part2
    part1, part2 = 0, 0
    with open(path, 'r') as file:

        while True:
            
            #Get list of next three lines from file
            rucksacks = list(islice(file, 3))

            #When we reach the end of file, break
            if not rucksacks:
                break
            
            #Add part 1 priorities from each rucksack to part1 solution
            for rucksack in rucksacks:
                part1 += get_priority1(rucksack.strip())
            
            #Add part 2 priority from list of three rucksacks to part2 solution
            part2 += get_priority2(rucksacks)        

    print(f"Part 1 answer is {part1}")
    print(f"Part 2 answer is {part2}")


if __name__ == "__main__":
    
    solution()
            


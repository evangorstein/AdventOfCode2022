#AOC2022/day01.py
import pathlib
import sys

def get_cals(elves_string):
    """From raw input string, return list of total calories of each elf, 
    i.e. list of ints of length the number of elves)"""

    #Create list of strings with "\n" separating different foods 
    elves_list = elves_string.split("\n\n") 
    #Create list of list of ints
    elves_list_int = [map(int, elf.split()) for elf in elves_list] 
    
    cals = [sum(elf) for elf in elves_list_int]
    return cals

def solve_part1(elves_string):
    """Solve part 1."""

    cals = get_cals(elves_string)
    return max(cals)

def solve_part2(elves_string):
    """Solves part 2"""

    cals = get_cals(elves_string)
    cals.sort(reverse=True)
    return sum(cals[0:3])


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        max_cals = solve_part1(puzzle_input)
        max_top3_cals = solve_part2(puzzle_input)
        print(f"Part 1 answer is {max_cals}")
        print(f"Part 2 answer is {max_top3_cals}")
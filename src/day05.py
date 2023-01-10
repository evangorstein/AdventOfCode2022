#AOC2022/day05.py
import sys #Command line arguments
import pathlib #For reading entire string from a file path
import re #Regular expressions
import copy #For copying objects instead of just creating referrences 

class Stacks:

    def __init__(self, num_stacks: int, crates: list[list[str]]):

        if len(crates) != num_stacks:
            raise ValueError("Length of stacks not equal to num_stacks")

        self.num_stacks = num_stacks 
        self.crates = crates

    def add(self, which, letter):
        self.crates[which].append(letter)
    
    def move(self, frm, to, many, sticky:bool):
        lst = self.crates[frm-1][-many:]
        if not sticky:
            lst.reverse()
        self.crates[to-1] = self.crates[to-1] + lst
        self.crates[frm-1] = self.crates[frm-1][:-many] 

    def follow_instruction(self, instructions, sticky:bool):
        """Follows instructions given by instructions, moving crates around in the Stacks object
        """

        for line in instructions.split('\n'):
            
            #Line is of the form "move x from y to z"
            many, frm, to = [int(i) for i in re.findall(r'\b\d+\b', line)]

            #Make the move
            self.move(frm, to, many, sticky)


def create_init_stacks(init_string):
    """Creates the initial Stacks object, i.e. the stacks before any of the 
    instructions get followed
    
    Input: init_string is string with the lines of the file giving the initial configuration of the stacks.
    Output: Stacks object with this configuration
    
    The input string is in "fixed-width" form with its last line a header.
    See Advent of Code for examples
    """

    #Find the number of stacks as the last number in the last line of the string
    num_stacks = int(re.findall(r"(\d) $", init_string)[0])
    #Initialize empty stacks 
    crates = [[] for i in range(num_stacks)]
    #Initialize crates object
    stacks = Stacks(num_stacks, crates)

    #Reverse lines of the string 
    init_list = init_string.split("\n")[:-1]
    init_list.reverse()

    #Go through each line, picking out letters to be added with the positions index
    #For each letter to be added, add it to the correct stack
    positions = [4*i+1 for i in range(num_stacks)] 
    for line in init_list:
        letters = [line[pos] for pos in positions]
        for (stack, letter) in enumerate(letters):
            if letter == " ":
                continue
            else: 
                stacks.add(stack, letter)
    
    return stacks

def solution():
    
    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1]
    #path = "data/ex_day05.txt"
    print(f"\n{path}:")
    
    part1 = 0

    puzzle_input = pathlib.Path(path).read_text().rstrip()

    init_string, instructions = puzzle_input.split('\n\n')

    stacks1 = create_init_stacks(init_string)
    stacks2 = copy.deepcopy(stacks1)

    stacks1.follow_instruction(instructions, sticky=False)
    stacks2.follow_instruction(instructions, sticky=True)

    print("Solution to part 1 is " + "".join([stack.pop() for stack in stacks1.crates]))
    print("Solution to part 2 is " + "".join([stack.pop() for stack in stacks2.crates]))


if __name__ == "__main__":
    solution()





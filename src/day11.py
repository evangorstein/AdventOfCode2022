#AOC2022/day11.py
import sys

class Monkey:
    
    def __init__(self, items, op, test):
        self.items = items
        self.op = op
        self.test = test
        self.inspect_count = 0

    def __str__(self):
        return f"Monkey with items {self.items}, operation {self.op}, test {self.test} and count {self.inspect_count}"

if __name__ == "__main__":

    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day11.txt" 
    print(f"\n{path}:")

    #Get input
    with open(path) as file:
        input = file.read().strip()
        monkey_texts = input.split("\n\n")

    #Save monkeys
    monkeys = []
    for m in monkey_texts:
        lines = m.split("\n")
        
        #Saves numbers from line 1 of monkey text as list
        items = [int(item.replace(",", "")) for item in lines[1].split()[2:]] 
        
        #Saves operation from line 2 of monkey text as tuple 
        #First element is the operation (+ or *)
        #Second element is what will be added or multiplied 
        op = tuple(lines[2].split()[4:]) 
        #Saves test data. 
        # "test" is number to check divisibility
        # "true" is monkey to send to if divisible
        # "false" is monkey to send to if not divisible
        test = { 
            "test" : int(lines[3].split()[-1]), 
            "true" : int(lines[4].split()[-1]),
            "false" : int(lines[5].split()[-1])
            }
        
        monkeys.append(Monkey(items, op, test))
    
    
    test_prod = 1
    for monk in monkeys:
        test_prod *= monk.test["test"]

    # Go through 20 rounds
    for _ in range(10_000):
        print(_)
        for monk in monkeys:
            monk.inspect_count += len(monk.items)
            
            for item in monk.items:
                arg = int(monk.op[1]) if (monk.op[1] != "old") else item
                
                if monk.op[0] == "+":
                    item += arg
                else:  
                    item *= arg   
                
                item = item % test_prod #Modulo math

                if item % monk.test["test"] == 0: 
                    monkeys[monk.test["true"]].items.append(item)
                else:
                    monkeys[monk.test["false"]].items.append(item)
                
            monk.items = []
    
    counts = sorted([monkey.inspect_count for monkey in monkeys])
    
    print(counts[-1]*counts[-2])
        

    
            







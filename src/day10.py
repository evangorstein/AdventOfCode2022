#AOC2022/day10.py
import sys

def solution1():
    
    x = 1 
    cyc = 1
    sig = []

    for line in input:
        
        if cyc % 40 == 20:
                sig.append(cyc*x)
        
        if line == "noop":
            cyc += 1
            continue
        
        num = int(line.split()[1])
        cyc += 1
        if cyc % 40 == 20:
            sig.append(cyc*x)
        
        cyc += 1
        x += num 
    
    print(sum(sig))
    

def solution2():
    
    x = 1 
    crt = 0
    st = ""
    
    for line in input:
        
        if crt == 40:
            st += "\n"
            crt = 0

        if line == "noop":
            st += "#" if x-1 <= crt <= x+1 else "."
            crt += 1
            continue
        
        num = int(line.split()[1])
        st += "#" if x-1 <= crt <= x+1 else "."  
        crt += 1
        if crt == 40:
            st += "\n"
            crt = 0
        st += "#" if x-1 <= crt <= x+1 else "."
        crt += 1
        x += num
    
    print(st)

if __name__ == "__main__":

    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "data/ex_day10.txt" 
    print(f"\n{path}:")

    #Get input as list of lines
    with open(path) as file:
        input = [line.strip() for line in file.readlines()]
    
    solution1()
    solution2()
#AOC2022/day07.py
import sys

def solution():
    
    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1]
    #path = "data/day07.txt"
    print(f"\n{path}:")

    with open(path) as file:
        
        #Don't include first line as it's just cd-ing into root directory, aka \
        lines = [line.strip() for line in file.readlines()][1:] 
        
        all_ds = {"root" : 0}
        cur_ds = ["root"]

        for (ind, line) in enumerate(lines):
            if line[:4] == "$ cd":
                if line[5:7] == "..":
                    cur_ds.pop() #Remove most nested directory from list of current directories
                else:
                    cur_ds.append(line[5:]) #Append directory to list of current directories
            elif line[:4] == "$ ls":
                continue #Do nothing
            elif line[:3] == "dir":
                dir = line[4:]
                
                #Make sure not adding a repeat
                while (dir in all_ds):
                    dir = dir + "+" 

                #Change line in file where this directory will be cd-ed into to match new name for the directory
                cd_string = "$ cd " + line[4:]
                cd_ind = lines.index(cd_string, ind+1)
                lines[cd_ind] = "$ cd " + dir
                all_ds[dir] = 0 #Add directory to dictionary of all directories

            else: #In this case, the line is a file, and the first part of the line is the file size
                fsize = int(line.split()[0])
                #Add file size to all current directories 
                for dir in cur_ds:
                    all_ds[dir] += fsize
        
        #Solution to part 1
        sol1 = 0 
        sizes = all_ds.values()
        for size in sizes:
            if size <= 100_000:
                sol1 += size

        #Solution to part 2
        unused = 70_000_000 - all_ds["root"]
        to_delete = 30_000_000 - unused 
        filt_sizes = [size for size in sizes if size > to_delete]
        sol2 = min(filt_sizes)

        #Print solution
        print(f"Solution to part 1 is {sol1}")
        print(f"Solution to part 2 is {sol2}")
                
if __name__ == "__main__":
    solution()
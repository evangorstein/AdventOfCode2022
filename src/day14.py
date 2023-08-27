#AOC2022/day14.py
import sys

if __name__ == "__main__":

    # Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day14.txt" 
    print(f"\n{path}:")

    # Get input
    with open(path) as file:
        input = file.read().strip()

    # Extract rock coordinates from paths
    rock_coordinates = set()
    for path in input.split("\n"):

        coordinates = path.strip().split(" -> ")
        for i in range(len(coordinates) - 1):
            start_x, start_y = map(int, coordinates[i].split(","))
            end_x, end_y = map(int, coordinates[i + 1].split(","))

            if start_x == end_x:  # Vertical path
                
                ys = [start_y, end_y]
                small_y, large_y = min(ys), max(ys)
                for y in range(small_y, large_y + 1):
                    rock_coordinates.add((start_x, y))

            elif start_y == end_y:  # Horizontal path

                xs = [start_x, end_x]
                small_x, large_x = min(xs), max(xs)
                for x in range(small_x, large_x + 1):
                    rock_coordinates.add((x, start_y))

            else:  # Diagonal path (unsupported in this context)
                raise ValueError("Diagonal paths are not supported.")
    
    lowest_rock = max([tup[1] for tup in rock_coordinates])
    
    # Problem 1
    # Simulate falling sand
    num_sand = 0
    sand_coordinates = set()
    source = (500, 0)
    bottom_flow = False
    while not bottom_flow:

        resting = False
        new_sand_coordinates = source

        while not resting:
            (x,y) = new_sand_coordinates

            # Check whether sand has reached layer of rock at the bottom and will therefore fall indefinitely
            if y == lowest_rock:
                bottom_flow = True
                break

            # Check if sand can fall down
            if (x, y + 1) not in rock_coordinates and (x, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x, y+1)

            # Check if sand can move down-left
            elif (x - 1, y + 1) not in rock_coordinates and (x - 1, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x - 1, y + 1) 

            # Check if sand can move down-right
            elif (x + 1, y + 1) not in rock_coordinates and (x + 1, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x + 1, y + 1)

            # Resting achieved    
            else:
                sand_coordinates.add(new_sand_coordinates)
                num_sand += 1
                resting = True
                
    print(f"Solution to part 1 is {num_sand}")


    # Problem 2
    # Simulate falling sand
    num_sand = 0
    sand_coordinates = set()
    source = (500, 0)
    while True:
        #Check whether source is blocked 
        if source in sand_coordinates:
            break 

        #Since source is not blocked, send a new sand falling
        resting = False
        new_sand_coordinates = source

        while not resting:
            (x,y) = new_sand_coordinates

            # Check whether sand has reached floor layer and will therefore come to rest 
            if y == lowest_rock + 1:
                sand_coordinates.add(new_sand_coordinates)
                num_sand += 1
                resting = True
                break

            # Check if sand can fall down
            if (x, y + 1) not in rock_coordinates and (x, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x, y+1)

            # Check if sand can move down-left
            elif (x - 1, y + 1) not in rock_coordinates and (x - 1, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x - 1, y + 1) 

            # Check if sand can move down-right
            elif (x + 1, y + 1) not in rock_coordinates and (x + 1, y + 1) not in sand_coordinates:
                new_sand_coordinates = (x + 1, y + 1)

            # Resting achieved    
            else:
                sand_coordinates.add(new_sand_coordinates)
                num_sand += 1
                resting = True
            
                
    print(f"Solution to part 2 is {num_sand}")








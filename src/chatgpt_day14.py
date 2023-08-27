def calculate_resting_sand(rock_paths):
    rock_coordinates = set()

    # Extract rock coordinates from paths
    for path in rock_paths.split("\n"):
        coordinates = path.strip().split(" -> ")
        for i in range(len(coordinates) - 1):
            start_x, start_y = map(int, coordinates[i].split(","))
            end_x, end_y = map(int, coordinates[i + 1].split(","))

            if start_x == end_x:  # Vertical path
                for y in range(start_y, end_y + 1):
                    rock_coordinates.add((start_x, y))
            elif start_y == end_y:  # Horizontal path
                for x in range(start_x, end_x + 1):
                    rock_coordinates.add((x, start_y))
            else:  # Diagonal path (unsupported in this context)
                raise ValueError("Diagonal paths are not supported.")

    # Calculate resting sand units
    resting_sand = 0
    sand_coordinates = set()
    source = (500, 0)
    sand_coordinates.add(source)

    while sand_coordinates:
        new_sand_coordinates = set()

        for sand in sand_coordinates:
            x, y = sand

            # Check if sand can fall down
            if (x, y + 1) not in rock_coordinates and (x, y + 1) not in sand_coordinates:
                new_sand_coordinates.add((x, y + 1))

            # Check if sand can move down-left
            elif (x - 1, y + 1) not in rock_coordinates and (x - 1, y + 1) not in sand_coordinates:
                new_sand_coordinates.add((x - 1, y + 1))

            # Check if sand can move down-right
            elif (x + 1, y + 1) not in rock_coordinates and (x + 1, y + 1) not in sand_coordinates:
                new_sand_coordinates.add((x + 1, y + 1))
                sand_coordinates = new_sand_coordinates
            #Resting achieved    
            else:
                resting_sand += 1
                

        sand_coordinates = new_sand_coordinates

    return resting_sand

# Example input
rock_paths = "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9"

resting_sand_units = calculate_resting_sand(rock_paths)
print("Resting Sand Units:", resting_sand_units)
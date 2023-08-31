#AOC2022/day15.py

# The solution to part 2 is brute force and will burn your laptop CPU if run on the full input,
# but works well for the example input.
import sys
import re
import time

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve_part_1(important_row, entries):
    
    #Set of all coordinates that cannot have a beacon
    no_beacon = set()
    for entry in entries:
            
        matches = re.findall(coord_extract_pattern, entry)
        
        sensor = (int(matches[0][0]), int(matches[0][1]))
        beacon = (int(matches[1][0]), int(matches[1][1]))
    
        dist = manhattan_distance(sensor, beacon)
        dist_to_row = abs(important_row - sensor[1])
        
        # If the important row is within the radius defined by dist, add to set of disallowed
        # coordinates in this important row
        if dist_to_row <= dist:
            slack = dist - dist_to_row
            #print(f"Slack for {entry} is {slack}")
            for x in range(sensor[0] - slack, sensor[0] + slack + 1):
                no_beacon.add(x)
        #Remove beacon from set of coordinates where there is no beacon
        if beacon[1] == important_row:
            no_beacon.remove(beacon[0]) 
    
    print("Solution to part 1 is", len(no_beacon))

class SearchSpace:
    """
    We use this class only for part 2. To solve part 1, we use the function `solve_part_1` defined above
    """

    def __init__(self, min_x=0, max_x=20, min_y=0, max_y=20):
        """
        Initialize the set of points where the beacon cannot be as a list of lists, 
        where each list represents a row. The list at index y contains tuples of the form (x1, x2), 
        representing ranges of x-values where the beacon cannot be in row y.
        """
        SearchSpace.no_beacon = [[] for i in range(min_y, max_y+1)]
        SearchSpace.x_range = (min_x, max_x)
        SearchSpace.y_range = (min_y, max_y)

    def process(self, sensor, dist):
        """
        Example: beacon is at (100,75) and dist is 50
        Then we want to eliminate all coordinates within Manhattan distance 50 of (100,75).

        Strategy:
        Iterate from row 25 to 125. 
            - In row 25, we only eliminate the point (100, 25). 
            - In row 26, we elimiminate (99:101, 26).
            - Etc
        """
        min_row_to_eliminate = max(sensor[1] - dist, self.y_range[0])
        max_row_to_eliminate = min(sensor[1] + dist, self.y_range[1])
        for y in range(min_row_to_eliminate, max_row_to_eliminate+1):
            slack = dist - abs(sensor[1] - y)
            min_x_to_eliminate = max(sensor[0] - slack, self.x_range[0])
            max_x_to_eliminate = min(sensor[0] + slack, self.x_range[1])
            x_range = (min_x_to_eliminate, max_x_to_eliminate)
            self.eliminate(y, x_range)

    def eliminate(self, y, x_range):
        """
        Add x_range to SearchSpace.no_beacon[y]
        """
        
        #print(f"Eliminating {x_range} from row {y}")
        # add x_range to the list of tuples at index y of no_beacon 
        ranges = self.no_beacon[y]
        ranges.append(x_range)

        # merge overlapping ranges: see https://stackoverflow.com/questions/15273693/union-of-multiple-ranges
        b = []
        for begin,end in sorted(ranges):
            if not b or b[-1][1] < begin - 1:
                b.append((begin, end))
            elif b[-1][1] < end:
                b[-1] = (b[-1][0], end)
            
        self.no_beacon[y] = b
        #print(f"Result: {self.no_beacon[y]}")

    def solve_part_2(self):
        filter = [(x_ranges, y) for (y, x_ranges) in enumerate(self.no_beacon) if x_ranges[0] != self.x_range]
        beacon_location = (filter[0][0][0][1]+1, filter[0][1])
        print("Beacon location is", beacon_location)

if __name__ == "__main__":

    # Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day15.txt" 
    print(f"Data is from {path}")

    # Get input
    with open(path) as file:
        input = file.read().strip()
    
    entries = input.split("\n")
    # Define the regular expression pattern to extract the coordinates
    coord_extract_pattern = r"x=(-?\d+),\s*y=(-?\d+)"
    
    ### Part 1
    important_row = 10
    solve_part_1(important_row, entries)
    ### Part 2
    search_space = SearchSpace(0)
    for (i, entry) in enumerate(entries):
        matches = re.findall(coord_extract_pattern, entry)
    
        sensor = (int(matches[0][0]), int(matches[0][1]))
        beacon = (int(matches[1][0]), int(matches[1][1]))
        dist = manhattan_distance(sensor, beacon)
        
        # print(f"Processing entry {i} with dist {dist}")
        # time.sleep(3)
        search_space.process(sensor, dist)
    
    search_space.solve_part_2()
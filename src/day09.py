#AOC2022/day09.py
import sys

def get_new_pos(old_pos_h, old_pos_t, dir):
    """
    ARGUMENTS
    - old_pos_h: coordinates of head
    - old_pos_t: coordinates of tail
    - dir: One of "D", "U", "L", "R" giving direction that head is moving in

    VALUE
    - Tuple of new positions (first entry is position of head, second is position of tail)
    """

    #Get new position of head
    if dir == "D":
        new_pos_h = (old_pos_h[0], old_pos_h[1]-1)
    elif dir == "U":
         new_pos_h = (old_pos_h[0], old_pos_h[1]+1)
    elif dir == "L":
        new_pos_h = (old_pos_h[0]-1, old_pos_h[1])
    else:
        new_pos_h = (old_pos_h[0]+1, old_pos_h[1])
    
    #Get new position of tail
    if abs(new_pos_h[0]-old_pos_t[0]) <= 1 and abs(new_pos_h[1]-old_pos_t[1]) <= 1:
        #Tail still adjacent to head so no need to move
        new_pos_t = old_pos_t
    else:
        #Tail should be moved to old position of head
        new_pos_t = old_pos_h
    
    return new_pos_h, new_pos_t

def get_new_pos_chain(cur_pos, front):
    """
    ARGUMENTS:
    - cur_pos: Current position of the focus knot
    - front: Position of the knot in front of the focus knot

    VALUE:
    - New position of the focus knot
    """
    
    difx = front[0] - cur_pos[0]
    dify = front[1] - cur_pos[1]

    if abs(difx) <=1 and abs(dify) <=1: 
        new_pos = cur_pos
    elif abs(difx) >= 2 and abs(dify) >= 2:
        new_pos = (cur_pos[0] + 1 if difx > 0 else cur_pos[0] - 1, cur_pos[1] + 1 if dify > 0 else cur_pos[1] - 1) 
    elif abs(difx) >= 2:
        new_pos = (cur_pos[0] + 1 if difx > 0 else cur_pos[0] - 1, front[1])
    else:
        new_pos = (front[0], cur_pos[1] + 1 if dify > 0 else cur_pos[1] - 1)
    return new_pos
    
def solution():
    chain_len = 10
    coords = [(0,0)] * chain_len
    short_tail_record = set()
    long_tail_record = set()
    
    #Perform movemenets
    for line in input:
        line.strip()
        moves = int(line[2:])
        dir = line[0]
        for _ in range(moves):
            
            #First perform movement of head and knot immediately after it, i.e. knot H and knot 1
            pos_h, pos_t = get_new_pos(coords[0], coords[1], dir)
            coords[:2] = [pos_h, pos_t]
            short_tail_record.add(pos_t) #Record coords of short tail

            #Now perform movement of knots 2 through 9
            for i in range(1, chain_len-1):
                new_pos = get_new_pos_chain(coords[i+1], coords[i])
                coords[i+1] = new_pos
            long_tail_record.add(coords[-1]) #Record coords of long tail

    print(len(short_tail_record), len(long_tail_record))

if __name__ == "__main__":

    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "data/ex_day09.txt" 
    print(f"\n{path}:")

    #Get input as list of lines
    with open(path) as file:
        input = file.readlines()
    
    solution()




    




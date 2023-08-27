#AOC2022/day13.py
import sys
import ast


def convert_to_list(item):
    if isinstance(item, int):
        return [item]
    elif isinstance(item, list):
        return item

def check_order(left, right):

    #Iterate from 0 to the lenght of the shorter list
    for i in range(min([len(left), len(right)])):

        #If either entry is a list, recursively call check_order 
        if isinstance(left[i], list) or isinstance(right[i], list):
            
            inner_left = convert_to_list(left[i])
            inner_right = convert_to_list(right[i])
            inner_result = check_order(inner_left, inner_right)
            
            if inner_result == "Equal":
                continue
            else: 
                return inner_result
        
        #Otherwise, both entries are ints and we can check which is larger
        if left[i] < right[i]:
            return "Right"
        elif left[i] > right[i]:
            return "Wrong"
        
        #If we've gotten this far, left[i] == right[i], so proceed to next input

    #If we've reached the end of the for loop w/o returning, then we just want to check to see which list is longer
    if len(left) < len(right):
        return "Right"
    elif len(left) > len(right):
        return "Wrong"
    else: 
        return "Equal"

##Quicksort code from https://www.geeksforgeeks.org/quick-sort/
# Function to find the partition position
def partition(array, low, high):
 
    # Choose the rightmost element as pivot
    pivot = array[high]
 
    # Pointer for greater element
    i = low - 1
 
    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if check_order(array[j], pivot) == "Right":
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
 
    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
 
# Function to perform quicksort
def quicksort(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)
 
        # Recursive call on the left of pivot
        quicksort(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quicksort(array, pi + 1, high)


if __name__ == "__main__":

    #Get file path of puzzle input as command-line argument and print
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day13.txt" 
    print(f"\n{path}:")

    #Get input
    with open(path) as file:
        input = file.read().strip()

    ######### Part 1  ###########
    #Get pairs of packets
    pairs = input.split(sep = "\n\n")
    count = 0
    #Go through each pair of packets, checking whether it's in right order
    for (i, pair) in enumerate(pairs):

        #Get pair of packets as list of length 2
        packets = pair.split("\n")

        #Parse each packet, which is given as a string representation of a Python list, as an actual Python list.
        left = ast.literal_eval(packets[0])
        right = ast.literal_eval(packets[1])

        #Check order and add to count if it's the right order
        if check_order(left, right) == "Right":
            count += (i+1) #Want 1 instead of 0 indexing


    print(f"Solution to part 1 is {count}")

    packets = [ast.literal_eval(packet) for packet in input.split("\n") if packet != ""]
    packets.extend([[[2]], [[6]]])
    N = len(packets)
    quicksort(packets, 0, N-1)
    ind_2 = packets.index([[2]])
    ind_6 = packets.index([[6]])
    sol2 = (ind_2+1)*(ind_6+1)
    print(f"Solution to part 2 is {sol2}")





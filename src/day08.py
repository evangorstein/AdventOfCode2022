#AOC2022/day08.py
import sys
import numpy as np

#Get file path of puzzle input as command-line argument and print
path = sys.argv[1] if len(sys.argv) > 1 else "data/ex_day08.txt" 
print(f"\n{path}:")

#Create array of integers from input file
with open(path) as file:
    ary = np.array([[int(char) for char in line.strip()] for line in file.readlines()])
    
#Save some important variables
nrow = np.shape(ary)[0]
ncol = np.shape(ary)[1]


def solution1():

    #From left
    from_left_high = np.repeat(-1, nrow)
    from_left_visible = np.empty((nrow, ncol), bool)
    
    for j in range(ncol):
        from_left_visible[:,j] = ary[:,j] > from_left_high 
        from_left_high = np.maximum(ary[:,j], from_left_high)

    #From right
    from_right_high = np.repeat(-1, nrow)
    from_right_visible = np.empty((nrow, ncol), bool)
    
    for j in range(ncol - 1, 0, -1):
        from_right_visible[:,j] = ary[:,j] > from_right_high 
        from_right_high = np.maximum(ary[:,j], from_right_high)
    
    #From top 
    from_top_high = np.repeat(-1, ncol)
    from_top_visible = np.empty((nrow, ncol), bool)

    for i in range(nrow):
        from_top_visible[i,:] = ary[i,:] > from_top_high
        from_top_high = np.maximum(ary[i,:], from_top_high)

    #From bottom 
    from_bottom_high = np.repeat(-1, ncol)
    from_bottom_visible = np.empty((nrow, ncol), bool)

    for i in range(nrow - 1, 0, -1):
        from_bottom_visible[i,:] = ary[i,:] > from_bottom_high
        from_bottom_high = np.maximum(ary[i,:], from_bottom_high)


    #Combine results
    visible = np.any((from_left_visible, from_right_visible, from_top_visible, from_bottom_visible), axis = 0)
    total_visible = visible.sum()

    print(total_visible)


def solution2():
    
    right_vis = np.empty((nrow, ncol), int)
    left_vis = np.empty((nrow, ncol), int)
    down_vis = np.empty((nrow, ncol), int)
    up_vis = np.empty((nrow, ncol), int)

    for i in range(nrow):
        for j in range(ncol):
            
            cur_tree = ary[i,j]

            right_line = ary[i,(j+1):] 
            right_ind = np.nonzero(right_line >= cur_tree)[0]
            right_vis[i,j] = right_ind[0] + 1 if right_ind.size > 0 else right_line.size

            left_line = ary[i,(j-1)::-1] if j > 0 else np.array([])
            left_ind = np.nonzero(left_line >= cur_tree)[0]
            left_vis[i,j] = left_ind[0] + 1 if left_ind.size > 0 else left_line.size

            down_line = ary[(i+1):,j]
            down_ind = np.nonzero(down_line >= cur_tree)[0]
            down_vis[i,j] = down_ind[0] + 1 if down_ind.size > 0 else down_line.size

            up_line = ary[(i-1)::-1,j] if i > 0 else np.array([])
            up_ind = np.nonzero(up_line >= cur_tree)[0]
            up_vis[i,j] = up_ind[0] + 1 if up_ind.size > 0 else up_line.size
            
    scene = right_vis*left_vis*down_vis*up_vis

    print(np.max(scene))


if __name__ == "__main__":
    solution1()
    solution2()
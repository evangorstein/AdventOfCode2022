import sys
import numpy as np
from itertools import cycle

INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day17.txt"

# tetris shapes
SHAPE_A = np.zeros((1,7))
SHAPE_A[0,2:6] = 1
SHAPE_B = np.zeros((3, 7))
SHAPE_B[[0,1,1,1,2],[3,2,3,4,3]] = 1
SHAPE_C = np.zeros((3, 7))
SHAPE_C[[0,1,2,2,2],[4,4,2,3,4]] = 1
SHAPE_D = np.zeros((4, 7))
SHAPE_D[:, 2] = 1
SHAPE_E = np.zeros((2, 7))
SHAPE_E[:, [2,3]] = 1
SHAPES = [SHAPE_A, SHAPE_B, SHAPE_C, SHAPE_D, SHAPE_E]

class Game:
    """
    Class for the game

    Attributes:
        wind: iterator of wind directions
        shapes: iterator of shapes
        board: numpy array representing the board
        fs: numpy array representing the falling shape
        idx_t: index of top row of falling shape
        long: boolean indicating whether we have a lot of rocks and wish to expedite (as in part 2) 
        If long: 
            idx_wind: index of current wind direction
            wd: logged information in the form of dictionary 
                with list of (board states, heights, number of rocks) tuples for each wind direction index
            n_rock_cur: number of rocks that have fallen so far
    """
    def __init__(self, input, shapes, height = 4000, width = 7, long = False):
        self.shapes = cycle(shapes)
        self.board = np.zeros((height, width), dtype=int)
        self.board[-1,:] = 1 #bottom row is ground, so we fill it with ones
        self.long = long
        if self.long:
            self.wind = input
            self.idx_wind = 0
            self.wd = {i:[] for i in range(len(input))}
            self.n_rock_cur = 0
        else: 
            self.wind = cycle(input)

    def game_height(self):
        """
        Returns height of tower
        """
        return self.board.shape[0] - (np.where(self.board.any(axis=1))[0][0]+1)

    def add_shape(self):
        """
        Adds shape to board, updating board, fs, and idx_t attributes.
        If long, additionally logs information in wd.
        """
        if self.long:
            # first occurrence of rock in each column
            idx_first_rock = self.board.argmax(axis=0)
            # want relative vertical positions of rocks in each column so subtract the minimum
            cur_bs =  idx_first_rock - min(idx_first_rock)
            # current board state
            cur_bs = tuple(cur_bs)
            # log information
            self.wd[self.idx_wind].append((cur_bs, self.game_height(), self.n_rock_cur))

        shp = next(self.shapes)
        ht_shp = shp.shape[0]
        # Find top row that has non-zero entries
        idx_ground = np.where(self.board.any(axis=1))[0][0]
        idx_b = idx_ground - 3
        idx_t = idx_b - ht_shp
        self.board[idx_t:idx_b,:] = shp.copy()
        self.fs = shp.copy()
        self.idx_t = idx_t
    
    def blow(self, dir, ht_shp):
        
        idx_t = self.idx_t
        idx_b = idx_t + ht_shp
        bg = self.board[idx_t:idx_b,:] - self.fs

        if (
            dir == "<" and #check we're not bumping into wall
            sum(self.fs[:,0]) == 0 and #check we're not bumping into rock
            np.array_equal(np.zeros_like(bg), bg*np.roll(self.fs, -1, axis=1)) 
            ):
            self.fs = np.roll(self.fs, -1, axis=1)
        elif (
            dir == ">" and #check we're not bumping into wall
            sum(self.fs[:,-1]) == 0 and #check we're not bumping into rock
            np.array_equal(np.zeros_like(bg), bg*np.roll(self.fs, 1, axis=1))
            ):
            self.fs = np.roll(self.fs, 1, axis=1)

        self.board[idx_t:idx_b,:] = bg + self.fs

    def fall(self):
        if self.long:
            self.n_rock_cur += 1

        fallen = False
        ht_shp = self.fs.shape[0]
        while not fallen:
            # horizontal movement
            if self.long:
                gust = self.wind[self.idx_wind]
                self.idx_wind = (self.idx_wind + 1) % len(self.wind)
            else:
                gust = next(self.wind)
            self.blow(gust, ht_shp)

            # vertical movement
            idx_t = self.idx_t
            idx_b = idx_t + ht_shp
            bg = self.board[idx_t+1:idx_b+1,:].copy() 
            if ht_shp > 1:
                bg[:-1,:] = bg[:-1,:] - self.fs[1:,:]
            if np.array_equal(np.zeros_like(bg), bg*self.fs):
                self.board[idx_t:idx_b,:] = self.board[idx_t:idx_b,:] - self.fs
                self.board[idx_t+1:idx_b+1,:] = bg + self.fs
                self.idx_t += 1
            else:
                fallen = True

def solve_part1():
    
    game = Game(PUZZLE_INPUT, SHAPES)
    for _ in range(2022):
        game.add_shape()
        game.fall()
    print("Solution to part 1 is", game.game_height())
    
    # with np.printoptions(threshold=sys.maxsize):
    #     print(game.board)

def solve_part2():

    n_rock_total = 1_000_000_000_000
    tower_built = 0
    game = Game(PUZZLE_INPUT, SHAPES, long=True, height=10000)

    while game.n_rock_cur < n_rock_total:
        game.add_shape()

        # if the current board state appears previously, we have found a loop and we can expedite simulation
        bses = [bs for bs, _, _ in game.wd[game.idx_wind]]
        cur_bs = bses[-1]
        prev_bses = bses[:-1]        
        if cur_bs in prev_bses: 
            id = prev_bses.index(cur_bs)   
            # height built during one iteration of loop
            hts = [ht for _, ht, _ in game.wd[game.idx_wind]]
            ht_og = hts[id]
            ht_cur = hts[-1]
            ht_loop = ht_cur - ht_og
            # number of fallen rocks during one iteration of loop
            n_rocks = [n_rock for _, _, n_rock in game.wd[game.idx_wind]]
            n_rock_og = n_rocks[id]
            n_rock_cur = n_rocks[-1]
            n_rock_loop = n_rock_cur - n_rock_og
            # number of iterations of loop
            n_loop = (n_rock_total - n_rock_cur) // n_rock_loop
            # expedite the simulation and erase the wind dictionary
            game.n_rock_cur += n_loop * n_rock_loop
            game.wd = {i:[] for i in range(len(PUZZLE_INPUT))}
            # how much gets built during the skip ahead?
            tower_built = n_loop * ht_loop

            # do some printing
            print(f"Loop found at gust index {game.idx_wind}")
            print(f"Skip ahead consists of {n_loop} iterations of {n_rock_loop} rocks falling")
            print(f"{tower_built} units built during skip ahead")
            # with np.printoptions(threshold=sys.maxsize):
            #     print(game.board)
            #exit()
        
        game.fall()

    print("Solution to part 2 is", game.game_height()+tower_built)

if __name__ == "__main__":  
    
    print(f"Data is from {INPUT_PATH}")

    with open(INPUT_PATH) as f:
        PUZZLE_INPUT = f.read().strip()
    
    solve_part1()
    print("Now solving part 2...")
    solve_part2()

    
    
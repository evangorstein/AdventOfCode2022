import sys
import numpy as np
from itertools import cycle

INPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "../data/ex_day17.txt"

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

    def __init__(self, height = 4000):
        self.board = np.zeros((height, 7), dtype=int)
        self.board[-1,:] = 1 # bottom row is ground 
        
    def add_shape(self, shp):
        
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
        fallen = False
        ht_shp = self.fs.shape[0]
        while not fallen:
            # horizontal movement
            self.blow(next(wind), ht_shp)
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

if __name__ == "__main__":  
    
    print(f"Data is from {INPUT_PATH}")

    with open(INPUT_PATH) as f:
        puzzle_input = f.read().strip()

    game = Game()
    wind = cycle(puzzle_input)
    shapes = cycle(SHAPES)
    for _ in range(2022):
        game.add_shape(next(shapes))
        game.fall()
    game_height = 4000 - (np.where(game.board.any(axis=1))[0][0]+1)
    print(game_height)

    


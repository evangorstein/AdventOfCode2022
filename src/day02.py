#AOC2022/day02.py
import pathlib
import sys


def score(round):
    """Returns score for a round, i.e. which is given as string of length 3
    The first character in the string is the opponents' play, either "A"=Rock, 
    "B"=Paper, or "C"=Scissors, and the third charater is my play, either 
    "X"=Rock, "Y"=Paper, or "Z"=Scissors
    """

    you, me = (round[0], round[2])

    #Player 1 plays Rock
    if you == "A":
        if me == "X":
            score1, score2 = (4, 3)
        elif me == "Y":
            score1, score2 = (8, 4)
        else:
            score1, score2 = (3, 8)

    #Player 1 plays Paper
    if you == "B":
        if me == "X":
            score1, score2 = (1, 1)
        elif me == "Y":
            score1, score2 = (5, 5)
        else:
            score1, score2 = (9, 9)
    
    #Player 1 plays Scissors
    if you == "C":
        if me == "X":
            score1, score2 = (7, 2)
        elif me == "Y":
            score1, score2 = (2, 6)
        else: 
            score1, score2 = (6, 7)

    return (score1, score2)
    



if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()

        rounds = puzzle_input.split("\n")
        scrs = list(map(score, rounds))
        total_score1 = sum([scr[0] for scr in scrs]) 
        total_score2 = sum([scr[1] for scr in scrs])

        print(f"Total score for part 1 is {total_score1}\n")
        print(f"Total score for part 2 is {total_score2}\n")


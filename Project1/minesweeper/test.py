


import random


height = 8
width = 8
mines = set()

# Initialize an empty field with no mines
board = []
for i in range(height):
    row = [] 
    for j in range(width):
        row.append(False)
    board.append(row)

print("no mine initial board: ", board)

# Add mines randomly; self.mine is a 2d array with location of mine in self.board. Self.board uses true value to represent mine
while len(mines) != 2:
    i = random.randrange(height)
    j = random.randrange(width)
    if not board[i][j]:
        mines.add((i, j))
        board[i][j] = True

print("board with mine: ", board)
print("Mine location: ", mines )


for i in range(height):
    print("--" * width + "-")
    for j in range(width):
        if board[i][j]:
            print("|X", end="")
        else:
            print("| ", end="")
    print("|")
print("--" * width + "-")

def is_mine(self, cell):
    i, j = cell
    return self.board[i][j]

def nearby_mines(self, cell):
    """
    Returns the number of mines that are
    within one row and column of a given cell,
    not including the cell itself.
    """

    # Keep count of nearby mines
    count = 0

    # Loop over all cells within one row and column -- why this is +2 instead of +1 ?
    for i in range(cell[0] - 1, cell[0] + 2):
        for j in range(cell[1] - 1, cell[1] + 2):

            # Ignore the cell itself
            if (i, j) == cell:
                continue

            # Update count if cell in bounds and is mine
            if 0 <= i < self.height and 0 <= j < self.width:
                if self.board[i][j]:
                    count += 1

    return count

def won(self):
    """
    Checks if all mines have been flagged.
    """
    return self.mines_found == self.mines


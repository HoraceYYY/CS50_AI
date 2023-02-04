"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    """
    [[EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]]
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    row = len(board)
    column = len(board[0])
    count_empty = 0
    
    for i in range(row):
        for j in range(column):
            if (board[i][j] == EMPTY):
                count_empty += 1 ## If the # of empty is odd, X's move, otherwise, O's move
        
    ##print("Number of Empty: ", count_empty)
    if count_empty % 2 == 0:
        ## print ("It is O 's turn")
        return O 
    else:
        ## print ("It is X 's turn")
        return X  

    raise NotImplementedError

def emptyboard(board):
    """
    check if a board is empty and pick a random location to start to avoid meaningless initial computing as O player
    """
    row = len(board)
    column = len(board[0])
    count_empty = 0
    
    for i in range(row):
        for j in range(column):
            if (board[i][j] == EMPTY):
                count_empty += 1 ## If the # of empty is odd, X's move, otherwise, O's move
    
    if count_empty == 9:
        return True
    else:
        return False

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    this is working now
    """
    actions=[]
    row = len(board)
    column = len(board[0])
    ##print("Row is: ",row, "Column is: ", column)

    for i in range(row):
        for j in range(column):
            # print("i is: ",i, "j is: ",j)
            if (board[i][j] == EMPTY):
                actions.append([i,j])
    
    ##print("Action is: ", actions)
    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise NameError("Action Not Valid!")
    
    next_player = player(board)
    newboard = copy.deepcopy(board)
    
    if next_player == O:
        newboard[action[0]][action[1]] = O
    else:
        newboard[action[0]][action[1]] = X

    return newboard

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ## define all posible solution in a solution set
    horizontal_solution = [[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]]]
    vertical_solution = [[[0,0],[1,0],[2,0]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]]]
    diagnal_solution = [[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]]
    solution_set = horizontal_solution + vertical_solution + diagnal_solution
    ##print(solution_set)

    ## find all the postion of X and O, and store them in 2 arrays
    X_position=[]
    O_position=[]
    row = len(board)
    column = len(board[0])

    for i in range(row):
        for j in range(column):
            if (board[i][j] == X):
                X_position.append([i,j])
            elif (board[i][j] == O):
                O_position.append([i,j])

    ##print("x position: ",X_position)
    ##print("o position: ",O_position)

    ## For each solution in the solution set (represeted by solution_set[i]), I am checking if each element 
    # of the solution (represeted by solution_set[i][j]) can be indexed by the x list and o list. If so, that soltion is added to the xwin or owin list.
    # after each solution has been checked against the xlist or olist, I will measure the length of the xwin/owin, if the size of the list is 3, that means we have found a winer,
    # if the size of the list is not 3, the list will be re-initiated to check the next solution
    
    # initialize empty arrays to capture the wining array position
    xwin = []
    owin = []

    # check for x wining
    for i in range(len(solution_set)):
        for j in range(len(solution_set[i])):
            try:
                X_position.index(solution_set[i][j])
            except ValueError:
                break
            else:
                xwin.append(solution_set[i][j])
        ##print("loopx: ", xwin)
   
        if len(xwin) == 3:
            ## print("x wins", xwin)
            return X  # X wins
        else:
            xwin = []
    
    # check for o wining    
    for i in range(len(solution_set)):
        for j in range(len(solution_set[i])):
            try:
                O_position.index(solution_set[i][j])
            except ValueError:
                break
            else:
                owin.append(solution_set[i][j])
        ##print("loopo: ", owin)
   
        if len(owin) == 3:
            ## print("o wins", owin)
            return O  # O wins
        else:
            owin = []


    # if the program has not found and returned a solution, that means no one has won the game
    # print("X didn't win and O didn't win")
    return None  # X didn't win and O didn't win
        
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_result = winner(board)

    if game_result == None:
        if any(EMPTY in list for list in board):  # I don't fully understand this line
            # print("no winner, game is not done")
            return False
        else:
            # print("no winner but board full")
            return True
    else:
        # print("winner is: ", game_result)
        return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    score = float("-inf")
    for action in actions(board):
        score = max(score, min_value(result(board,action)))
    return score

def min_value(board):
    if terminal(board):
        return utility(board)
    score = float('inf') 
    for action in actions(board):
        score = min(score, max_value(result(board,action)))
    return score


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if emptyboard(board): # this only apply to starting as O player to pick a random starting position
        initial_position_index = random.randint(0,8)
        return actions(board)[initial_position_index]
    if player(board) == X:
        score = float('-inf')
        nextstep = None
        for action in actions(board):
            next_board = result(board,action)
            action_score = min_value(next_board)
            if action_score > score:
                score = action_score
                nextstep = action
        return nextstep
    elif player(board) == O:
        score = float("inf")
        nextstep = None
        for action in actions(board):
            next_board = result(board,action)
            action_score = max_value(next_board)
            if action_score < score:
                score = action_score
                nextstep = action
        return nextstep
    raise NotImplementedError

"""
Code to test the output of the function in this file

def main():
    board = initial_state()
##    player(board)
##    print(actions(board))

    terminal(board)
  
    

if __name__ == "__main__":
    main()
"""


from turtle import *
import random


# ============================================================
# TIC TAC TOE
#
# Board values:
# 0 = Nought / Human
# 1 = Cross / Computer
# 2 = Empty
#
# Board positions:
#
#       7 | 8 | 9
#      ---+---+---
#       4 | 5 | 6
#      ---+---+---
#       1 | 2 | 3
#
# ============================================================


# -------------------------
# CONSTANTS
# -------------------------

EMPTY = 2
NOUGHT = 0
CROSS = 1


# Turtle coordinates for each board position
pos = [
    [0, 0],
    [-100, -60], [-5, -60], [85, -60],
    [-100, -5],  [-5, -5],  [85, -5],
    [-100, 45],  [-5, 45],  [85, 45]
]


# Every possible winning combination
winning_lines = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7]
]


# ============================================================
# TURTLE SETUP
# ============================================================

def setup_turtle():

    speed("fastest")
    pencolor("black")
    width(3)
    hideturtle()
    penup()


# ============================================================
# DRAW GRID
# ============================================================

def draw_grid():

    pencolor("black")

    # Vertical lines
    for x in [-50, 50]:

        penup()
        goto(x, 75)

        pendown()
        goto(x, -75)

    # Horizontal lines
    for y in [-25, 25]:

        penup()
        goto(-125, y)

        pendown()
        goto(125, y)

    penup()


# ============================================================
# DRAW CROSS
# ============================================================

def draw_x(key):

    x = pos[key][0]
    y = pos[key][1]

    pencolor("orange")

    # First diagonal
    penup()
    goto(x, y)

    pendown()
    goto(x + 10, y + 10)

    # Second diagonal
    penup()
    goto(x, y + 10)

    pendown()
    goto(x + 10, y)

    penup()


# ============================================================
# DRAW NOUGHT
# ============================================================

def draw_o(key):

    x = pos[key][0]
    y = pos[key][1]

    pencolor("blue")

    penup()
    goto(x, y)

    pendown()

    goto(x + 10, y)
    goto(x + 10, y + 10)
    goto(x, y + 10)
    goto(x, y)

    penup()


# ============================================================
# CHECK WINNER
# ============================================================

def check_winner(board):

    for line in winning_lines:

        a = line[0]
        b = line[1]
        c = line[2]

        if board[a] == board[b] == board[c]:

            if board[a] != EMPTY:
                return board[a]

    return EMPTY


# ============================================================
# CHECK IF BOARD IS FULL
# ============================================================

def board_full(board):

    for i in range(1, 10):

        if board[i] == EMPTY:
            return False

    return True


# ============================================================
# FIND AVAILABLE MOVES
# ============================================================

def available_moves(board):

    moves = []

    for i in range(1, 10):

        if board[i] == EMPTY:
            moves.append(i)

    return moves


# ============================================================
# FIND AN IMMEDIATE WINNING MOVE
# ============================================================

def find_winning_move(board, player):

    moves = available_moves(board)

    for move in moves:

        # Temporarily make the move
        board[move] = player

        winner = check_winner(board)

        # Undo the move
        board[move] = EMPTY

        # If this move wins, return it
        if winner == player:
            return move

    # 0 means no winning move was found
    return 0


# ============================================================
# MINIMAX WITH ALPHA-BETA PRUNING
# ============================================================

def minimax(board, maximising, depth, alpha, beta):

    winner = check_winner(board)

    # Computer has won
    if winner == CROSS:
        return 10 - depth

    # Human has won
    if winner == NOUGHT:
        return depth - 10

    # No spaces left = draw
    if board_full(board):
        return 0


    # --------------------------------------------------------
    # MAXIMISING PLAYER
    # COMPUTER
    # --------------------------------------------------------

    if maximising:

        best_score = -100

        moves = available_moves(board)

        for move in moves:

            # Try computer move
            board[move] = CROSS

            # Recursively search future moves
            score = minimax(
                board,
                False,
                depth + 1,
                alpha,
                beta
            )

            # Undo computer move
            board[move] = EMPTY

            # Store best score
            if score > best_score:
                best_score = score

            # Update alpha
            if best_score > alpha:
                alpha = best_score

            # Alpha-beta pruning
            if beta <= alpha:
                break

        return best_score


    # --------------------------------------------------------
    # MINIMISING PLAYER
    # HUMAN
    # --------------------------------------------------------

    else:

        best_score = 100

        moves = available_moves(board)

        for move in moves:

            # Try human move
            board[move] = NOUGHT

            # Recursively search future moves
            score = minimax(
                board,
                True,
                depth + 1,
                alpha,
                beta
            )

            # Undo human move
            board[move] = EMPTY

            # Store lowest score
            if score < best_score:
                best_score = score

            # Update beta
            if best_score < beta:
                beta = best_score

            # Alpha-beta pruning
            if beta <= alpha:
                break

        return best_score


# ============================================================
# EASY BOT
#
# Chooses a completely random available square.
# ============================================================

def easy_bot(board):

    moves = available_moves(board)

    return random.choice(moves)


# ============================================================
# MEDIUM BOT
#
# 1. Win if possible
# 2. Block player if necessary
# 3. Otherwise choose randomly
# ============================================================

def medium_bot(board):

    # Can the computer win immediately?

    move = find_winning_move(
        board,
        CROSS
    )

    if move != 0:
        return move


    # Can the human win next turn?

    move = find_winning_move(
        board,
        NOUGHT
    )

    if move != 0:
        return move


    # Otherwise make random move

    moves = available_moves(board)

    return random.choice(moves)


# ============================================================
# HARD BOT
#
# Uses heuristic rules.
#
# Priority:
# 1. Win
# 2. Block
# 3. Centre
# 4. Corner
# 5. Other available square
# ============================================================

def hard_bot(board):

    # -------------------------
    # Try to win
    # -------------------------

    move = find_winning_move(
        board,
        CROSS
    )

    if move != 0:
        return move


    # -------------------------
    # Block human win
    # -------------------------

    move = find_winning_move(
        board,
        NOUGHT
    )

    if move != 0:
        return move


    # -------------------------
    # Take centre
    # -------------------------

    if board[5] == EMPTY:
        return 5


    # -------------------------
    # Take available corner
    # -------------------------

    corners = []

    for i in [1, 3, 7, 9]:

        if board[i] == EMPTY:
            corners.append(i)

    if len(corners) > 0:

        return random.choice(corners)


    # -------------------------
    # Take any other square
    # -------------------------

    moves = available_moves(board)

    return random.choice(moves)


# ============================================================
# IMPOSSIBLE BOT
#
# Uses:
#
# Minimax
# +
# Depth scoring
# +
# Alpha-beta pruning
#
# ============================================================

def impossible_bot(board):

    best_score = -100
    best_move = 0

    # Initial alpha and beta values
    alpha = -100
    beta = 100

    moves = available_moves(board)

    # Try every possible computer move
    for move in moves:

        # Make temporary computer move
        board[move] = CROSS

        # Search future game positions
        score = minimax(
            board,
            False,
            0,
            alpha,
            beta
        )

        # Undo move
        board[move] = EMPTY

        # Is this better than previous moves?
        if score > best_score:

            best_score = score
            best_move = move

        # Update alpha
        if best_score > alpha:
            alpha = best_score

    return best_move


# ============================================================
# SELECT CORRECT COMPUTER AI
# ============================================================

def computer_move(board, difficulty):

    if difficulty == 1:

        return easy_bot(board)

    elif difficulty == 2:

        return medium_bot(board)

    elif difficulty == 3:

        return hard_bot(board)

    else:

        return impossible_bot(board)


# ============================================================
# NUMBER INPUT VALIDATION
# ============================================================

def get_number(message, minimum, maximum):

    while True:

        try:

            number = int(input(message))

            if number >= minimum and number <= maximum:

                return number

            else:

                print(
                    "Enter a number from",
                    minimum,
                    "to",
                    maximum
                )

        except:

            print("Please enter a valid number.")


# ============================================================
# GET PLAYER'S MOVE
# ============================================================

def get_player_move(board):

    while True:

        key = get_number(
            "Enter position: ",
            1,
            9
        )

        if board[key] == EMPTY:

            return key

        else:

            print(
                "That position has already been played."
            )


# ============================================================
# PRINT POSITION GUIDE
# ============================================================

def print_positions():

    print()
    print("Board positions:")
    print()
    print("7 | 8 | 9")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("1 | 2 | 3")
    print()


# ============================================================
# GAME MODE MENU
# ============================================================

def get_game_mode():

    print()
    print("====================")
    print("    TIC TAC TOE")
    print("====================")
    print()

    print("1 - Two Players")
    print("2 - Play Computer")
    print()

    mode = get_number(
        "Choose mode: ",
        1,
        2
    )

    return mode


# ============================================================
# DIFFICULTY MENU
# ============================================================

def get_difficulty():

    print()
    print("====================")
    print("    DIFFICULTY")
    print("====================")
    print()

    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    print("4 - Impossible")
    print()

    difficulty = get_number(
        "Choose difficulty: ",
        1,
        4
    )

    return difficulty


# ============================================================
# DISPLAY FINAL RESULT
# ============================================================

def display_result(winner, mode):

    # Small calculator-friendly pause

    for i in range(1, 7):

        penup()

        goto(-100, -100)
        goto(100, 100)


    clear()

    pencolor("black")

    penup()
    goto(-100, 0)

    pendown()


    # Nought won

    if winner == NOUGHT:

        if mode == 2:

            write("You win!")

        else:

            write("Noughts win!")


    # Cross won

    elif winner == CROSS:

        if mode == 2:

            write("Computer wins!")

        else:

            write("Crosses win!")


    # Nobody won

    else:

        write("Draw!")


    penup()


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    # --------------------------------------------------------
    # CREATE EMPTY BOARD
    # --------------------------------------------------------

    board = [
        2, 2, 2, 2, 2,
        2, 2, 2, 2, 2
    ]


    # Nought goes first

    turn = NOUGHT


    # No winner at beginning

    winner = EMPTY


    # --------------------------------------------------------
    # SET UP TURTLE
    # --------------------------------------------------------

    setup_turtle()


    # --------------------------------------------------------
    # GET GAME MODE
    # --------------------------------------------------------

    mode = get_game_mode()


    # Difficulty is only used for computer mode

    difficulty = 0


    if mode == 2:

        difficulty = get_difficulty()


    # --------------------------------------------------------
    # DRAW GAME BOARD
    # --------------------------------------------------------

    draw_grid()


    # ========================================================
    # MAIN GAME LOOP
    # ========================================================

    while True:

        print_positions()


        # ====================================================
        # HUMAN TURN
        # ====================================================

        if mode == 1 or turn == NOUGHT:


            # -----------------------------------------------
            # Display whose turn it is
            # -----------------------------------------------

            if mode == 1:

                if turn == NOUGHT:

                    print("Nought's turn")

                else:

                    print("Cross's turn")

            else:

                print("Your turn")


            # -----------------------------------------------
            # Get player's square
            # -----------------------------------------------

            key = get_player_move(board)


            # -----------------------------------------------
            # NOUGHT
            # -----------------------------------------------

            if turn == NOUGHT:

                board[key] = NOUGHT

                draw_o(key)

                turn = CROSS


            # -----------------------------------------------
            # CROSS
            # -----------------------------------------------

            else:

                board[key] = CROSS

                draw_x(key)

                turn = NOUGHT


        # ====================================================
        # COMPUTER TURN
        # ====================================================

        else:

            print()
            print("Computer thinking...")


            # AI chooses move

            key = computer_move(
                board,
                difficulty
            )


            # Store computer move

            board[key] = CROSS


            # Draw X

            draw_x(key)


            print(
                "Computer chose position",
                key
            )


            # Give turn back to human

            turn = NOUGHT


        # ====================================================
        # CHECK FOR WINNER
        # ====================================================

        winner = check_winner(board)

        if winner != EMPTY:

            break


        # ====================================================
        # CHECK FOR DRAW
        # ====================================================

        if board_full(board):

            break


    # ========================================================
    # GAME OVER
    # ========================================================

    display_result(
        winner,
        mode
    )


    # Keep program open

    input()


# ============================================================
# BOILERPLATE
# ============================================================

if __name__ == "__main__":

    main()

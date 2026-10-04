from turtle import *
import random

# Constants
EMPTY = 2
NOUGHT = 0
CROSS = 1

# Turtle coordinates for each board position
pos = [
    [0, 0],
    [-100, -60], [-5, -60], [85, -60],
    [-100, -5], [-5, -5], [85, -5],
    [-100, 45], [-5, 45], [85, 45]
]

# All possible winning combinations
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

# Turtle setup
def setup_turtle():
    speed("fastest")
    pencolor("black")
    width(3)
    hideturtle()
    penup()

# Draw the grid
def draw_grid():
    pencolor("black")
    for x in [-50, 50]:
        penup()
        goto(x, 75)
        pendown()
        goto(x, -75)
    for y in [-25, 25]:
        penup()
        goto(-125, y)
        pendown()
        goto(125, y)
    penup()

# Draw a cross
def draw_x(key):
    x = pos[key][0]
    y = pos[key][1]
    pencolor("orange")
    penup()
    goto(x, y)
    pendown()
    goto(x + 10, y + 10)
    penup()
    goto(x, y + 10)
    pendown()
    goto(x + 10, y)
    penup()

# Draw a nought
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

# Check if someone has won
def check_winner(board):
    for line in winning_lines:
        a = line[0]
        b = line[1]
        c = line[2]
        if board[a] == board[b] == board[c]:
            if board[a] != EMPTY:
                return board[a]
    return EMPTY

# Check if the board is full
def board_full(board):
    for i in range(1, 10):
        if board[i] == EMPTY:
            return False
    return True

# Find all available moves
def available_moves(board):
    moves = []
    for i in range(1, 10):
        if board[i] == EMPTY:
            moves.append(i)
    return moves

# Find an immediate winning move
def find_winning_move(board, player):
    moves = available_moves(board)
    for move in moves:
        board[move] = player
        winner = check_winner(board)
        board[move] = EMPTY
        if winner == player:
            return move
    return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, maximising, depth, alpha, beta):
    winner = check_winner(board)

    if winner == CROSS:
        return 10 - depth
    if winner == NOUGHT:
        return depth - 10
    if board_full(board):
        return 0

    # Computer tries to maximise the score
    if maximising:
        best_score = -100
        moves = available_moves(board)

        for move in moves:
            board[move] = CROSS
            score = minimax(board, False, depth + 1, alpha, beta)
            board[move] = EMPTY

            if score > best_score:
                best_score = score

            if best_score > alpha:
                alpha = best_score

            # Prune unnecessary branches
            if beta <= alpha:
                break

        return best_score

    # Human tries to minimise the score
    else:
        best_score = 100
        moves = available_moves(board)

        for move in moves:
            board[move] = NOUGHT
            score = minimax(board, True, depth + 1, alpha, beta)
            board[move] = EMPTY

            if score < best_score:
                best_score = score

            if best_score < beta:
                beta = best_score

            # Prune unnecessary branches
            if beta <= alpha:
                break

        return best_score

# Easy bot - random move
def easy_bot(board):
    moves = available_moves(board)
    return random.choice(moves)

# Medium bot - win, block, otherwise random
def medium_bot(board):
    move = find_winning_move(board, CROSS)
    if move != 0:
        return move

    move = find_winning_move(board, NOUGHT)
    if move != 0:
        return move

    moves = available_moves(board)
    return random.choice(moves)

# Hard bot - heuristic strategy
def hard_bot(board):
    # Win if possible
    move = find_winning_move(board, CROSS)
    if move != 0:
        return move

    # Block the player
    move = find_winning_move(board, NOUGHT)
    if move != 0:
        return move

    # Take centre
    if board[5] == EMPTY:
        return 5

    # Take a corner
    corners = []
    for i in [1, 3, 7, 9]:
        if board[i] == EMPTY:
            corners.append(i)

    if len(corners) > 0:
        return random.choice(corners)

    # Otherwise take any available square
    moves = available_moves(board)
    return random.choice(moves)

# Impossible bot - minimax with alpha-beta pruning
def impossible_bot(board):
    best_score = -100
    best_move = 0
    alpha = -100
    beta = 100
    moves = available_moves(board)

    for move in moves:
        board[move] = CROSS
        score = minimax(board, False, 0, alpha, beta)
        board[move] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move

        if best_score > alpha:
            alpha = best_score

    return best_move

# Choose the correct bot
def computer_move(board, difficulty):
    if difficulty == 1:
        return easy_bot(board)
    elif difficulty == 2:
        return medium_bot(board)
    elif difficulty == 3:
        return hard_bot(board)
    else:
        return impossible_bot(board)

# Get a valid number from the user
def get_number(message, minimum, maximum):
    while True:
        try:
            number = int(input(message))
            if number >= minimum and number <= maximum:
                return number
            else:
                print("Enter a number from", minimum, "to", maximum)
        except:
            print("Please enter a valid number.")

# Get a valid board position
def get_player_move(board):
    while True:
        key = get_number("Enter position: ", 1, 9)
        if board[key] == EMPTY:
            return key
        else:
            print("That position has already been played.")

# Display board position numbers
def print_positions():
    print()
    print("Board positions:")
    print("7 | 8 | 9")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("1 | 2 | 3")
    print()

# Game mode menu
def get_game_mode():
    print("====================")
    print("    TIC TAC TOE")
    print("====================")
    print("1 - Two Players")
    print("2 - Play Computer")
    return get_number("Choose mode: ", 1, 2)

# Difficulty menu
def get_difficulty():
    print("====================")
    print("    DIFFICULTY")
    print("====================")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    print("4 - Impossible")
    return get_number("Choose difficulty: ", 1, 4)

# Display final result
def display_result(winner, mode):
    # Small pause before clearing screen
    for i in range(1, 7):
        penup()
        goto(-100, -100)
        goto(100, 100)

    clear()
    pencolor("black")
    penup()
    goto(-100, 0)
    pendown()

    if winner == NOUGHT:
        if mode == 2:
            write("You win!")
        else:
            write("Noughts win!")
    elif winner == CROSS:
        if mode == 2:
            write("Computer wins!")
        else:
            write("Crosses win!")
    else:
        write("Draw!")

    penup()

# Main function
def main():
    board = [EMPTY] * 10
    turn = NOUGHT
    winner = EMPTY

    setup_turtle()

    # Select game mode
    mode = get_game_mode()
    difficulty = 0

    if mode == 2:
        difficulty = get_difficulty()

    draw_grid()

    # Main game loop
    while True:
        print_positions()

        # Human/player turn
        if mode == 1 or turn == NOUGHT:
            if mode == 1:
                if turn == NOUGHT:
                    print("Nought's turn")
                else:
                    print("Cross's turn")
            else:
                print("Your turn")

            key = get_player_move(board)

            if turn == NOUGHT:
                board[key] = NOUGHT
                draw_o(key)
                turn = CROSS
            else:
                board[key] = CROSS
                draw_x(key)
                turn = NOUGHT

        # Computer turn
        else:
            print("Computer thinking...")
            key = computer_move(board, difficulty)
            board[key] = CROSS
            draw_x(key)
            print("Computer chose position", key)
            turn = NOUGHT

        # Check for a winner
        winner = check_winner(board)
        if winner != EMPTY:
            break

        # Check for a draw
        if board_full(board):
            break

    display_result(winner, mode)
    input()

# Program entry point
if __name__ == "__main__":
    main()

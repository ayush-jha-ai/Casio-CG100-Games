from turtle import *
from random import randint

# 0 = O, 1 = X, 2 = empty
O = 0
X = 1
EMPTY = 2

pos = [
    [0, 0],
    [-100, -60], [-5, -60], [85, -60],
    [-100, -5], [-5, -5], [85, -5],
    [-100, 45], [-5, 45], [85, 45]
]

wins = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7]
]

def draw_grid():
    pencolor("black")
    width(3)

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

def winner(board):
    for line in wins:
        a = line[0]
        b = line[1]
        c = line[2]

        if board[a] != EMPTY:
            if board[a] == board[b]:
                if board[a] == board[c]:
                    return board[a]

    return EMPTY

def board_full(board):
    for i in range(1, 10):
        if board[i] == EMPTY:
            return False

    return True

def winning_move(board, player):
    for i in range(1, 10):
        if board[i] == EMPTY:
            board[i] = player

            if winner(board) == player:
                board[i] = EMPTY
                return i

            board[i] = EMPTY

    return 0

def random_move(board):
    empty_count = 0

    for i in range(1, 10):
        if board[i] == EMPTY:
            empty_count += 1

    choice = randint(1, empty_count)
    count = 0

    for i in range(1, 10):
        if board[i] == EMPTY:
            count += 1

            if count == choice:
                return i

def minimax(board, maximise, depth, alpha, beta):
    win = winner(board)

    if win == X:
        return 10 - depth

    if win == O:
        return depth - 10

    if board_full(board):
        return 0

    if maximise:
        best = -100

        for i in range(1, 10):
            if board[i] == EMPTY:
                board[i] = X

                score = minimax(
                    board,
                    False,
                    depth + 1,
                    alpha,
                    beta
                )

                board[i] = EMPTY

                if score > best:
                    best = score

                if best > alpha:
                    alpha = best

                if beta <= alpha:
                    break

        return best

    else:
        best = 100

        for i in range(1, 10):
            if board[i] == EMPTY:
                board[i] = O

                score = minimax(
                    board,
                    True,
                    depth + 1,
                    alpha,
                    beta
                )

                board[i] = EMPTY

                if score < best:
                    best = score

                if best < beta:
                    beta = best

                if beta <= alpha:
                    break

        return best

def easy_bot(board):
    return random_move(board)

def medium_bot(board):
    move = winning_move(board, X)

    if move != 0:
        return move

    move = winning_move(board, O)

    if move != 0:
        return move

    if board[5] == EMPTY:
        return 5

    return random_move(board)

def impossible_bot(board):
    best_score = -100
    best_move = 0
    alpha = -100
    beta = 100

    # Centre is a strong first move and avoids
    # searching the entire empty game tree.
    if board[5] == EMPTY:
        return 5

    for i in range(1, 10):
        if board[i] == EMPTY:
            board[i] = X

            score = minimax(
                board,
                False,
                0,
                alpha,
                beta
            )

            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

            if best_score > alpha:
                alpha = best_score

    return best_move

def computer_move(board, difficulty):
    if difficulty == 1:
        return easy_bot(board)

    if difficulty == 2:
        return medium_bot(board)

    return impossible_bot(board)

def get_number(message, low, high):
    while True:
        number = int(input(message))

        if number >= low and number <= high:
            return number

        print("Enter", low, "to", high)

def get_player_move(board):
    while True:
        key = get_number(
            "Position: ",
            1,
            9
        )

        if board[key] == EMPTY:
            return key

        print("Already played")

def show_positions():
    print()
    print("7 | 8 | 9")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("1 | 2 | 3")
    print()

def show_result(win, mode):
    for i in range(5):
        penup()
        goto(-100, -100)
        goto(100, 100)

    clear()
    pencolor("black")
    penup()
    goto(-100, 0)
    pendown()

    if win == O:
        if mode == 2:
            write("You win!")
        else:
            write("Noughts win!")

    elif win == X:
        if mode == 2:
            write("Computer wins!")
        else:
            write("Crosses win!")

    else:
        write("Draw!")

    penup()

def main():
    board = [EMPTY] * 10
    turn = O

    speed("fastest")
    pencolor("black")
    width(3)
    hideturtle()
    penup()

    print("TIC TAC TOE")
    print()
    print("1 - Two Players")
    print("2 - Computer")

    mode = get_number(
        "Mode: ",
        1,
        2
    )

    difficulty = 0

    if mode == 2:
        print()
        print("1 - Easy")
        print("2 - Medium")
        print("3 - Impossible")

        difficulty = get_number(
            "Difficulty: ",
            1,
            3
        )

    draw_grid()

    while True:
        show_positions()

        if mode == 1 or turn == O:

            if mode == 1:
                if turn == O:
                    print("Nought's turn")
                else:
                    print("Cross's turn")
            else:
                print("Your turn")

            key = get_player_move(board)

            if turn == O:
                board[key] = O
                draw_o(key)
                turn = X

            else:
                board[key] = X
                draw_x(key)
                turn = O

        else:
            print("Computer thinking...")

            key = computer_move(
                board,
                difficulty
            )

            board[key] = X
            draw_x(key)

            print("Computer played", key)

            turn = O

        win = winner(board)

        if win != EMPTY:
            show_result(win, mode)
            break

        if board_full(board):
            show_result(EMPTY, mode)
            break

    input()

if __name__ == "__main__":
    main()


import math
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt

# Function to evaluate the game board
def evaluate(board):
    for row in board:
        if row.count('X') == 3:
            return 10
        elif row.count('O') == 3:
            return -10

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return 10
            elif board[0][col] == 'O':
                return -10

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return 10
        elif board[0][0] == 'O':
            return -10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return 10
        elif board[0][2] == 'O':
            return -10

    return 0

# Function to generate symmetrical boards
def generate_symmetric_boards(board):
    boards = []
    boards.append(board)  # Add the original board

    # Generate symmetric boards: rotated and mirrored
    for _ in range(3):
        board = rotate_board(board)
        if board not in boards:
            boards.append(board)
        mirrored_board = mirror_board(board)
        if mirrored_board not in boards:
            boards.append(mirrored_board)
    return boards

# Function to rotate the board 90 degrees
def rotate_board(board):
    return [list(row) for row in zip(*reversed(board))]

# Function to mirror the board
def mirror_board(board):
    return [row[::-1] for row in board]

# Alpha-beta pruning algorithm with symmetry reduction and memoization
def minimax_symmetry(board, depth, is_maximizing, alpha, beta, memo):
    board_str = tuple(map(tuple, board))
    if board_str in memo:
        return memo[board_str]

    score = evaluate(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not any('-' in row for row in board):
        return 0

    boards = generate_symmetric_boards(board)

    if is_maximizing:
        best = -math.inf
        for sym_board in boards:
            for i in range(3):
                for j in range(3):
                    if sym_board[i][j] == '-':
                        sym_board[i][j] = 'X'
                        best = max(best, minimax_symmetry(sym_board, depth + 1, not is_maximizing, alpha, beta, memo))
                        sym_board[i][j] = '-'
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        memo[board_str] = best
        return best
    else:
        best = math.inf
        for sym_board in boards:
            for i in range(3):
                for j in range(3):
                    if sym_board[i][j] == '-':
                        sym_board[i][j] = 'O'
                        best = min(best, minimax_symmetry(sym_board, depth + 1, not is_maximizing, alpha, beta, memo))
                        sym_board[i][j] = '-'
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        memo[board_str] = best
        return best

# AI move function with memoization and time complexity measurement
def ai_move():
    global time_complexity_data
    best_val = -math.inf
    best_move = (-1, -1)
    memo = {}

    # Measure execution time for the ai_move function
    start_time = time.time()

    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'X'
                move_val = minimax_symmetry(board, 0, False, -math.inf, math.inf, memo)
                board[i][j] = '-'

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    row, col = best_move
    buttons[row][col].config(text='X', state=tk.DISABLED)
    board[row][col] = 'X'

    # Measure execution time for the ai_move function
    end_time = time.time()
    execution_time = end_time - start_time
    time_complexity_data.append(execution_time)
    print(f"AI Move Time Complexity: {execution_time} seconds")

    if evaluate(board) == 10:
        messagebox.showinfo("Tic Tac Toe", "AI wins!")
        update_scores('ai')
        calculate_time_complexity()
        reset_board()
    elif not any('-' in row for row in board):
        messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        update_scores('tie')
        calculate_time_complexity()
        reset_board()

# Button click event
def on_click(row, col):
    if board[row][col] == '-':
        buttons[row][col].config(text='O', state=tk.DISABLED)
        board[row][col] = 'O'

        if evaluate(board) == -10:
            messagebox.showinfo("Tic Tac Toe", "You win!")
            update_scores('player')
            calculate_time_complexity()
            reset_board()
        elif any('-' in row for row in board):
            ai_move()
        else:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            update_scores('tie')
            calculate_time_complexity()
            reset_board()

# Reset the board
def reset_board():
    for i in range(3):
        for j in range(3):
            board[i][j] = '-'
            buttons[i][j].config(text='', state=tk.NORMAL)

# Update scores based on the result
def update_scores(result):
    global player_score, ai_score, tie_score
    if result == 'player':
        player_score += 1
    elif result == 'ai':
        ai_score += 1
    elif result == 'tie':
        tie_score += 1

    player_score_label.config(text=f"Player: {player_score}")
    ai_score_label.config(text=f"AI: {ai_score}")
    tie_score_label.config(text=f"Tie: {tie_score}")

# Calculate time complexity
def calculate_time_complexity():
    global start_time
    if not start_time:
        start_time = time.time()
    else:
        elapsed_time = time.time() - start_time
        print(f"Time complexity: {elapsed_time} seconds")
        start_time = None

# Calculate and show time complexity plot
def show_time_complexity():
    # Plot the results
    moves = list(range(1, len(time_complexity_data) + 1))
    plt.plot(moves, time_complexity_data, marker='o')
    plt.xlabel('AI Moves')
    plt.ylabel('Execution Time (s)')
    plt.title('Time Complexity Analysis for Each AI Move')
    plt.show()

    # Calculate and print the average time complexity
    average_time_complexity = sum(time_complexity_data) / len(time_complexity_data)
    print(f"Average Time Complexity: {average_time_complexity} seconds")

# Create main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Initialize the board
board = [['-' for _ in range(3)] for _ in range(3)]

# Create buttons
buttons = [[0 for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 20), width=5, height=2,
                                  command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Create labels for scores
player_score = 0
ai_score = 0
tie_score = 0

player_score_label = tk.Label(root, text=f"Player: {player_score}")
ai_score_label = tk.Label(root, text=f"AI: {ai_score}")
tie_score_label = tk.Label(root, text=f"Tie: {tie_score}")

player_score_label.grid(row=3, column=0)
ai_score_label.grid(row=3, column=1)
tie_score_label.grid(row=3, column=2)

start_time = None  # Initialize start_time variable
time_complexity_data = []  # Store execution times for each AI move

# Button to show time complexity
time_complexity_button = tk.Button(root, text="Show Time Complexity", command=show_time_complexity)
time_complexity_button.grid(row=4, columnspan=3)

root.mainloop()



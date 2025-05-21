
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import math

class TicTacToe:
    def __init__(self, master):
        self.buttons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = None  # Initialize to None, will be set after asking the user
        self.execution_times = []  # Added

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('Arial', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.calculate_button = tk.Button(master, text="Calculate Time Complexity", command=self.calculate_and_show_plot)
        self.calculate_button.grid(row=3, column=0, columnspan=3)

        # After initializing the GUI, ask the user to choose the starting player
        self.choose_starting_player()

    def choose_starting_player(self):
        answer = messagebox.askquestion("Tic Tac Toe", "Do you want to play first?")
        if answer == 'yes':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
            self.ai_move_with_corners()

    def evaluate(self, board):
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

        corner_control = 0
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if board[corner[0]][corner[1]] == 'X':
                corner_control += 1
            elif board[corner[0]][corner[1]] == 'O':
                corner_control -= 1

        return corner_control

    def minimax_with_corners(self, board, depth, is_maximizing):
        score = self.evaluate(board)
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any('-' in row for row in board):
            return 0

        if is_maximizing:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'X'
                        best = max(best, self.minimax_with_corners(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        best = min(best, self.minimax_with_corners(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best

    def ai_move_with_corners(self):
        # Measure execution time for the ai_move_with_corners function - Modified
        start_time = time.time()

        best_val = -math.inf
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.board[i][j] = 'X'
                    move_val = self.minimax_with_corners(self.board, 0, False)
                    self.board[i][j] = '-'

                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        row, col = best_move
        self.buttons[row][col].config(text='X', state=tk.DISABLED)
        self.board[row][col] = 'X'

        result = self.evaluate(self.board)
        if result == 10:
            messagebox.showinfo("Tic Tac Toe", "AI wins!")
            self.reset_board()
        elif not any('-' in row for row in self.board):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_board()
        else:
            self.current_player = 'O'

        # Measure execution time for the ai_move_with_corners function - Modified
        end_time = time.time()
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)  # Added
        print(f"AI Move Execution Time: {execution_time} seconds")  # Added

    def on_click(self, row, col):
        if self.board[row][col] == '-':
            self.buttons[row][col].config(text='O', state=tk.DISABLED)
            self.board[row][col] = 'O'

            result = self.evaluate(self.board)
            if result == -10:
                messagebox.showinfo("Tic Tac Toe", "You win!")
                self.reset_board()
            elif any('-' in row for row in self.board):
                self.ai_move_with_corners()
            else:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_board()

    def reset_board(self):
        play_again = messagebox.askyesno("Tic Tac Toe", "Do you want to play again?")
        if play_again:
            for i in range(3):
                for j in range(3):
                    self.board[i][j] = '-'
                    self.buttons[i][j].config(text='', state=tk.NORMAL)

            self.current_player = None
            self.choose_starting_player()

    def calculate_time_complexity(self, board_size, num_simulations):  # Modified
        input_sizes = list(range(3, board_size + 1))
        execution_times = []

        for size in input_sizes:
            self.board = [['-' for _ in range(size)] for _ in range(size)]

            for _ in range(num_simulations):  # Added
                # Measure execution time for the ai_move_with_corners function - Modified
                start_time = time.time()
                self.ai_move_with_corners()
                end_time = time.time()
                execution_time = end_time - start_time
                execution_times.append(execution_time)
                print(f"Board Size: {size}x{size}, Execution Time: {execution_time} seconds")

        # Plot the results - Modified
        plt.plot(range(1, num_simulations + 1), execution_times, marker='o')  # Modified
        plt.xlabel('AI Moves')  # Modified
        plt.ylabel('Execution Time (s)')  # Modified
        plt.title('Time Complexity Analysis (Corner Control Heuristic)')  # Modified
        plt.show()

        # Calculate and print the average time complexity - Added
        average_time_complexity = sum(execution_times) / len(execution_times)
        print(f"Average Time Complexity: {average_time_complexity} seconds")  # Added

    def calculate_and_show_plot(self):
        # Plot the results
        moves = list(range(1, len(self.execution_times) + 1))
        plt.plot(moves, self.execution_times, marker='o')
        plt.xlabel('AI Moves')
        plt.ylabel('Execution Time (s)')
        plt.title('Time Complexity Analysis for Each AI Move')
        plt.show()

        # Calculate and print the average time complexity
        average_time_complexity = sum(self.execution_times) / len(self.execution_times)
        print(f"Average Time Complexity: {average_time_complexity} seconds")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()



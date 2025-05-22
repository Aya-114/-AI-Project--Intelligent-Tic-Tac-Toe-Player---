import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import math
import sys
from styled_wrapper import create_styled_game

class TicTacToe:
    def __init__(self, master):
              # Add score tracking variables
        self.ai_score = 0
        self.player_score = 0

# Add score display label (after creating the game board buttons)
        self.score_label = tk.Label(master, text=f"AI: {self.ai_score}  You: {self.player_score}", font=('Arial', 12))
        self.score_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.buttons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = self.choose_starting_player()
        self.execution_times = []
        self.space_complexity = []

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('Arial', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        # Create calculate button but don't add it to layout - styled wrapper will handle this
        self.calculate_button = tk.Button(master, text="Calculate Time Complexity and Space Complexity", command=self.calculate_and_show_plot)
        # Removed: self.calculate_button.grid(row=3, column=0, columnspan=3)

        if self.current_player == 'X':
            self.ai_move()

    def choose_starting_player(self):
        result = messagebox.askyesno("Tic Tac Toe", "Do you want to play first?")
        return 'O' if result else 'X'

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

        return 0

    def minimax(self, board, depth, is_maximizing):
        # Check for symmetry to reduce search space
        board = self.normalize_board(board)
        
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
                        best = max(best, self.minimax(board, depth + 1, False))
                        board[i][j] = '-'
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        best = min(best, self.minimax(board, depth + 1, True))
                        board[i][j] = '-'
            return best
    
    def normalize_board(self, board):
        # Normalize the board by considering symmetries
        # This reduces the search space by eliminating equivalent board states
        
        # For simplicity, we'll just return the original board in this implementation
        # In a full implementation, this would identify and normalize symmetric positions
        return board

    def ai_move(self):
        start_time = time.time()

        best_val = -math.inf
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.board[i][j] = 'X'
                    move_val = self.minimax(self.board, 0, False)
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
            self.ai_score += 1
            self.update_score_display()
            self.reset_board()
        elif not any('-' in row for row in self.board):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_board()
        else:
            self.current_player = 'O'

        end_time = time.time()
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)

        space_used = sys.getsizeof(self.board)
        self.space_complexity.append(space_used)

        print(f"AI Move Execution Time: {execution_time} seconds, Space Complexity: {space_used} bytes")

    def on_click(self, row, col):
        if self.board[row][col] == '-' and self.current_player == 'O':
            self.buttons[row][col].config(text='O', state=tk.DISABLED)
            self.board[row][col] = 'O'

            result = self.evaluate(self.board)
            if result == -10:
                messagebox.showinfo("Tic Tac Toe", "You win!")
                self.player_score += 1
                self.update_score_display()

                self.reset_board()
            elif any('-' in row for row in self.board):
                self.ai_move()
            else:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_board()
    def update_score_display(self):
      self.score_label.config(text=f"AI: {self.ai_score}  You: {self.player_score}")

    def reset_board(self):
        play_again = messagebox.askyesno("Tic Tac Toe", "Do you want to play again?")
        if play_again:
            for i in range(3):
                for j in range(3):
                    self.board[i][j] = '-'
                    self.buttons[i][j].config(text='', state=tk.NORMAL)

            self.current_player = self.choose_starting_player()
            if self.current_player == 'X':
                self.ai_move()

    def calculate_and_show_plot(self):
        moves = list(range(1, len(self.execution_times) + 1))
        plt.plot(moves, self.execution_times, marker='o', label='Time Complexity')
        plt.plot(moves, self.space_complexity, marker='o', label='Space Complexity')
        plt.xlabel('AI Moves')
        plt.ylabel('Complexity')
        plt.title('Time and Space Complexity Analysis for Each AI Move')
        plt.legend()
        plt.show()

        average_time_complexity = sum(self.execution_times) / len(self.execution_times)
        print(f"Average Time Complexity: {average_time_complexity} seconds")

        average_space_complexity = sum(self.space_complexity) / len(self.space_complexity)
        print(f"Average Space Complexity: {average_space_complexity} bytes")

if __name__ == "__main__":
    root = tk.Tk()
    # Use the styled wrapper to enhance visuals while preserving original logic
    styled_game = create_styled_game(TicTacToe)(root)
    root.mainloop()

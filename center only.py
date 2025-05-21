import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import sys

class TicTacToe:
    def __init__(self, master):
        self.buttons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = self.choose_starting_player()
        self.execution_times = []  # تخزين أوقات التنفيذ لكل حركة AI
        self.space_complexity = []  # تخزين استهلاك اAIلذاكرة لكل حركة 

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('Arial', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.calculate_button = tk.Button(master, text="Calculate Time Complexity and Space Complexity", command=self.calculate_and_show_plot)
        self.calculate_button.grid(row=3, column=0, columnspan=3)

        if self.current_player == 'X':
            self.ai_move_with_center()

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

        center_control = 0
        if board[1][1] == 'X':
            center_control += 1
        if board[1][1] == 'O':
            center_control -= 1

        return center_control

    def ai_move_with_center(self):
        start_time = time.time()

        # إذا المركز فاضي خليه
        if self.board[1][1] == '-':
            row, col = 1, 1
        else:
            # اختار أول خانة فاضية بدون Minimax
            move_found = False
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        row, col = i, j
                        move_found = True
                        break
                if move_found:
                    break

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
                self.reset_board()
            elif any('-' in row for row in self.board):
                self.ai_move_with_center()
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

            self.current_player = self.choose_starting_player()
            if self.current_player == 'X':
                self.ai_move_with_center()

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
    game = TicTacToe(root)
    root.mainloop()

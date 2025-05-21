import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import math
import winsound


class TicTacToe:
    def __init__(self, master):
        self.buttons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [["-" for _ in range(3)] for _ in range(3)]
        self.current_player = self.choose_starting_player()
        self.score = {"X": 0, "O": 0, "Tie": 0}
        self.nodes_visited = 0  # Track the number of nodes visited

        # Load scores from file
        self.load_score_from_file()

        # Label to display scores
        self.score_label = tk.Label(
            master,
            text=f"X Wins: {self.score['X']} | O Wins: {self.score['O']} | Ties: {self.score['Tie']}",
        )
        self.score_label.grid(row=4, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    master,
                    text="",
                    font=("Arial", 20),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.on_click(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j)

        self.calculate_button = tk.Button(
            master,
            text="Calculate Time Complexity and Nodes Visited",
            command=self.calculate_and_show_plot,
        )
        self.calculate_button.grid(row=3, column=0, columnspan=3)

        if self.current_player == "X":
            self.ai_move()

    def choose_starting_player(self):
        result = messagebox.askyesno("Tic Tac Toe", "Do you want to play first?")
        return "O" if result else "X"

    def evaluate(self, board):
        for row in board:
            if row.count("X") == 3:
                return 10
            elif row.count("O") == 3:
                return -10

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] == "X":
                    return 10
                elif board[0][col] == "O":
                    return -10

        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == "X":
                return 10
            elif board[0][0] == "O":
                return -10

        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == "X":
                return 10
            elif board[0][2] == "O":
                return -10

        return 0

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        self.nodes_visited += 1  # Increment the nodes_visited counter
        score = self.evaluate(board)

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any("-" in row for row in board):
            return 0

        if is_maximizing:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "-":
                        board[i][j] = "X"
                        best = max(
                            best,
                            self.minimax(
                                board, depth + 1, not is_maximizing, alpha, beta
                            ),
                        )
                        board[i][j] = "-"
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "-":
                        board[i][j] = "O"
                        best = min(
                            best,
                            self.minimax(
                                board, depth + 1, not is_maximizing, alpha, beta
                            ),
                        )
                        board[i][j] = "-"
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def ai_move(self):
        self.nodes_visited = 0  # Reset the nodes_visited counter
        best_val = -math.inf
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    self.board[i][j] = "X"
                    move_val = self.minimax(self.board, 0, False, -math.inf, math.inf)
                    self.board[i][j] = "-"

                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        row, col = best_move
        self.buttons[row][col].config(text="X", state=tk.DISABLED)
        self.board[row][col] = "X"

        result = self.evaluate(self.board)
        if result == 10:
            messagebox.showinfo("Tic Tac Toe", "AI wins!")
            self.score["X"] += 1
            self.save_score_to_file()
            winsound.PlaySound("RAAAA.wav", winsound.SND_FILENAME)
            print(f"Nodes Visited: {self.nodes_visited}")  # Print the nodes visited
            self.reset_board()
        elif not any("-" in row for row in self.board):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.score["Tie"] += 1
            self.save_score_to_file()
            print(f"Nodes Visited: {self.nodes_visited}")  # Print the nodes visited
            self.reset_board()
        else:
            self.current_player = "O"

    def on_click(self, row, col):
        if self.board[row][col] == "-" and self.current_player == "O":
            self.buttons[row][col].config(text="O", state=tk.DISABLED)
            self.board[row][col] = "O"

            result = self.evaluate(self.board)
            if result == -10:
                messagebox.showinfo("Tic Tac Toe", "You win!")
                self.score["O"] += 1
                self.save_score_to_file()
                print(f"Nodes Visited: {self.nodes_visited}")  # Print the nodes visited
                self.reset_board()
            elif any("-" in row for row in self.board):
                self.current_player = "X"
                self.ai_move()
            else:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.score["Tie"] += 1
                self.save_score_to_file()
                print(f"Nodes Visited: {self.nodes_visited}")  # Print the nodes visited
                self.reset_board()

    def reset_board(self):
        # Update the score label
        self.score_label.config(
            text=f"X Wins: {self.score['X']} | O Wins: {self.score['O']} | Ties: {self.score['Tie']}"
        )

        play_again = messagebox.askyesno("Tic Tac Toe", "Do you want to play again?")
        if play_again:
            for i in range(3):
                for j in range(3):
                    self.board[i][j] = "-"
                    self.buttons[i][j].config(text="", state=tk.NORMAL)

            self.current_player = self.choose_starting_player()
            if self.current_player == "X":
                self.ai_move()

    def save_score_to_file(self):
        with open("alphaScore.txt", "w") as file:
            file.write(f"X Wins: {self.score['X']}\n")
            file.write(f"O Wins: {self.score['O']}\n")
            file.write(f"Ties: {self.score['Tie']}\n")

    def load_score_from_file(self):
        try:
            with open("alphaScore.txt", "r") as file:
                lines = file.readlines()
                self.score["X"] = int(lines[0].split(": ")[1].strip())
                self.score["O"] = int(lines[1].split(": ")[1].strip())
                self.score["Tie"] = int(lines[2].split(": ")[1].strip())
        except FileNotFoundError:
            # If the file is not found, initialize scores to 0
            self.score = {"X": 0, "O": 0, "Tie": 0}

    def calculate_time_complexity(self, board_size):
        input_sizes = list(range(3, board_size + 1))
        execution_times = []

        for size in input_sizes:
            self.board = [["-" for _ in range(size)] for _ in range(size)]

            # Measure execution time for the ai_move function
            start_time = time.time()
            self.ai_move()
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            print(
                f"Board Size: {size}x{size}, Execution Time: {execution_time} seconds"
            )

        # Plot the results
        plt.plot(input_sizes, execution_times)
        plt.xlabel("Board Size")
        plt.ylabel("Execution Time (s)")
        plt.title("Time Complexity Analysis")
        plt.show()

    def calculate_and_show_plot(self):
        board_size = 8  # You can adjust this to the desired board size
        self.calculate_time_complexity(board_size)


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

import tkinter as tk
import tkinter.messagebox
import random
import time
import matplotlib.pyplot as plt
import pygame
import sys

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = self.choose_starting_player()
        self.buttons = []
        self.score = {'X': 0, 'O': 0, 'Tie': 0}
        self.load_score_from_file()
        self.create_board_gui()
        self.create_analysis_button()
        self.create_score_label()
        self.max_nodes = 0  # Variable to track the maximum number of nodes in memory
        self.root.after(0, self.make_first_move)  # Call make_first_move after the GUI is initialized
        self.root.mainloop()

    def make_first_move(self):
        if self.current_player == 'O':
            self.ai_move()

    def create_board_gui(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text='', font=('Arial', 20), width=4, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def create_analysis_button(self):
        analysis_button = tk.Button(self.root, text="Calculate Time and Space Complexity", command=self.calculate_and_show_plot)
        analysis_button.grid(row=3, column=0, columnspan=3)

    def create_score_label(self):
        self.score_label = tk.Label(self.root, text="Score: X - 0, O - 0, Tie - 0", font=('Arial', 12))
        self.score_label.grid(row=4, column=0, columnspan=3)

    def on_button_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.game_over(f"Player {self.current_player} wins!")
            elif ' ' not in self.board:
                self.game_over("It's a tie!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_move()

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O')
        if self.check_winner('O'):
            self.game_over("AI wins!")
        elif ' ' not in self.board:
            self.game_over("It's a tie!")
        else:
            self.current_player = 'X'

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    self.max_nodes = max(sys.getsizeof(board), self.max_nodes)  # Check the size of the board
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def choose_starting_player(self):
        answer = tk.messagebox.askquestion("Start Game", "Do you want to play first")
        if answer == 'yes':
            return 'X'
        else:
            return 'O'

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                return True
        return False

    def game_over(self, message):
        if "AI wins!" in message:
            self.play_sound('RAAAA.wav')
            self.score['O'] += 1
        elif "X" in message:
            self.score['X'] += 1
        else:
            self.score['Tie'] += 1

        self.update_score_label()

        print(f"Space Complexity: {self.max_nodes} bytes")  # Print the max nodes

        answer = tk.messagebox.askquestion("Game Over", f"{message}\nDo you want to play again?")
        if answer == 'yes':
            self.reset_board()
        else:
            self.save_score_to_file()
           

    def reset_board(self):
        for i in range(9):
            self.board[i] = ' '
            self.buttons[i].config(text='')
        self.current_player = self.choose_starting_player()
        if self.current_player == 'O':
            self.ai_move()

    def calculate_time_complexity(self, board_size):
        input_sizes = list(range(3, board_size + 1))
        execution_times = []

        for size in input_sizes:
            self.board = [' ' for _ in range(size * size)]

            # Measure execution time for the ai_move function
            start_time = time.time()
            self.ai_move()
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            print(f"Board Size: {size}x{size}, Execution Time: {execution_time} seconds")

        # Plot the results
        plt.plot(input_sizes, execution_times)
        plt.xlabel('Board Size')
        plt.ylabel('Execution Time (s)')
        plt.title('Time Complexity Analysis')
        plt.show()

    def calculate_and_show_plot(self):
        board_size = 8  # You can adjust this to the desired board size
        self.calculate_time_complexity(board_size)

    def save_score_to_file(self):
        with open('miniScore.txt', 'w') as file:
            file.write(f"X Wins: {self.score['X']}\n")
            file.write(f"O Wins: {self.score['O']}\n")
            file.write(f"Ties: {self.score['Tie']}\n")

    def load_score_from_file(self):
        try:
            with open('miniScore.txt', 'r') as file:
                lines = file.readlines()
                self.score['X'] = int(lines[0].split(': ')[1])
                self.score['O'] = int(lines[1].split(': ')[1])
                self.score['Tie'] = int(lines[2].split(': ')[1])
        except FileNotFoundError:
            pass

    def update_score_label(self):
        self.score_label.config(text=f"Score: X - {self.score['X']}, O - {self.score['O']}, Tie - {self.score['Tie']}")

    def play_sound(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

if __name__ == "__main__":
    game = TicTacToe()

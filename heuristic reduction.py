
import tkinter as tk
import tkinter.messagebox
import copy
import random
import time
import matplotlib.pyplot as plt

class TicTacToe:
    def __init__(self):
        # Initialize the GUI and game variables
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.buttons = []
        self.create_board_gui()
        self.calculate_button = tk.Button(self.root, text="Calculate Time Complexity", command=self.calculate_and_show_plot)
        self.calculate_button.grid(row=3, column=0, columnspan=3)
        self.reset_board()  # Start a new game and ask the player if they want to play first
        self.root.mainloop()

    def create_board_gui(self):
        # Create the GUI for the Tic Tac Toe board
        for i in range(3):
            for j in range(3):
                # Create buttons for each cell in the board
                button = tk.Button(self.root, text='', font=('Arial', 20), width=4, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def on_button_click(self, row, col):
        # Handle player's move when a button is clicked
        index = 3 * row + col
        if self.board[index] == ' ':
            # If the cell is empty, mark it with the current player's symbol
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                # Check if the current player has won after their move
                self.game_over(f"Player {self.current_player} wins!")
            elif ' ' not in self.board:
                # If the board is full and there's no winner, it's a tie
                self.game_over("It's a tie!")
            else:
                # Switch to the AI's turn if the game continues
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    # AI's turn to make a move
                    self.ai_move()

    def ai_move(self):
        # AI calculates and makes the best move
        best_move = self.get_best_move()
        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O')
        if self.check_winner('O'):
            self.game_over("AI wins!")
        elif ' ' not in self.board:
            self.game_over("It's a tie!")
        else:
            self.current_player = 'X'

    def get_best_move(self):
        # Get the best move for the AI by evaluating potential moves
        best_score = float('-inf')
        best_moves = []
        for i in range(9):
            if self.board[i] == ' ':
                # Try each empty cell and evaluate the move
                new_board = copy.deepcopy(self.board)
                new_board[i] = 'O'
                score = self.get_heuristic_value(new_board)
                if score > best_score:
                    # Update best moves based on the heuristic score
                    best_score = score
                    best_moves = [i]
                elif score == best_score:
                    best_moves.append(i)
        return random.choice(best_moves)

    def get_heuristic_value(self, board):
        # Evaluate the heuristic value for the given board
        symmetrical_boards = self.generate_symmetric_boards(board)
        max_wins = 0
        for sym_board in symmetrical_boards:
            # Count potential wins for the AI player on symmetrical boards
            wins = self.count_potential_wins(sym_board, 'O')
            max_wins = max(max_wins, wins)
        return max_wins

    def count_potential_wins(self, board, player):
        # Count the potential winning combinations for a player on the board
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        count = 0
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                count += 1
        return count

    def generate_symmetric_boards(self, board):
        # Generate symmetrical boards: original, mirrored, and rotated
        symmetrical_boards = []
        symmetrical_boards.append(board)  # Original board
        mirrored_board = [board[2 - i + 3 * j] for i in range(3) for j in range(3)]  # Mirrored board
        symmetrical_boards.append(mirrored_board)
        rotated_board = [board[6 + i - 3 * j] for i in range(3) for j in range(3)]  # Rotated board
        symmetrical_boards.append(rotated_board)
        return symmetrical_boards

    def check_winner(self, player):
        # Check if the given player has won
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
        # Display game-over message and ask if the player wants to play again
        result = tk.messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
        if result:
            # Reset the board and start a new game
            self.reset_board()

    def reset_board(self):
        # Reset the board and ask if the player wants to play first
        result = tk.messagebox.askyesno("Tic Tac Toe", "Do you want to play first?")
        self.current_player = 'X' if result else 'O'
        for i in range(9):
            self.board[i] = ' '
            self.buttons[i].config(text='')
        if self.current_player == 'O':
            # AI's turn to make a move if player chose 'O'
            self.ai_move()

    def calculate_time_complexity(self, board_size):
        input_sizes = list(range(3, board_size + 1))
        execution_times = []

        for size in input_sizes:
            self.board = [' ' for _ in range(size ** 2)]

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
        # Reset the board and ask if the player wants to play first after plotting
        self.reset_board()

if __name__ == "__main__":
    game = TicTacToe()






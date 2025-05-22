import tkinter as tk
from tkinter import messagebox, font
import time
import matplotlib.pyplot as plt
import math
import sys

class ModernTicTacToe:
    def __init__(self, master, variant_type="center"):
        """
        Initialize the Modern Tic Tac Toe game
        
        Parameters:
        - master: Tkinter root window
        - variant_type: Type of game variant ("center", "corner", "minimax", "minimax_alpha_beta", "symmetry", "heuristic")
        """
        # Set window properties
        master.title("Tic Tac Toe Variants")
        master.geometry("600x700")
        master.configure(bg="#2c3e50")
        
        # Center the window
        self.center_window(master)
        
        # Define colors
        self.colors = {
            "background": "#2c3e50",  # Dark blue
            "cell_bg": "#3498db",      # Blue
            "cell_hover": "#2980b9",   # Darker blue
            "x_color": "#e74c3c",      # Red
            "o_color": "#2ecc71",      # Green
            "x_border": "#c0392b",     # Darker red
            "o_border": "#27ae60",     # Darker green
            "grid_lines": "#ecf0f1",   # Light gray/white
            "text": "#ffffff"          # White
        }
        
        # Game state variables
        self.buttons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = self.choose_starting_player()
        self.execution_times = []
        self.space_complexity = []
        self.x_score = 0
        self.o_score = 0
        self.winning_line = None
        self.variant_type = variant_type
        
        # Create main frame
        self.main_frame = tk.Frame(master, bg=self.colors["background"], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create game board frame
        self.board_frame = tk.Frame(self.main_frame, bg=self.colors["background"], 
                                   bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.board_frame.pack(pady=20)
        
        # Create game board
        self.create_game_board()
        
        # Create status bar
        self.create_status_bar()
        
        # Create footer with buttons
        self.create_footer()
        
        # Start game if AI goes first
        if self.current_player == 'X':
            self.status_var.set("AI (X) is thinking...")
            master.after(500, self.ai_move)

    def center_window(self, window):
        """Center the window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_header(self):
        """Create the header with game title and score"""
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Game title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        
        # Set title based on variant
        variant_titles = {
            "center": "Center Control",
            "center_minimax": "Center Control with Minimax",
            "center_alpha_beta": "Center Control with Alpha-Beta",
            "corner": "Corner Control",
            "corner_minimax": "Corner Control with Minimax",
            "corner_alpha_beta": "Corner Control with Alpha-Beta",
            "minimax": "Basic Minimax",
            "minimax_alpha_beta": "Minimax with Alpha-Beta",
            "symmetry": "Symmetry Reduction",
            "heuristic": "Heuristic Reduction"
        }
        
        title = variant_titles.get(self.variant_type, "Tic Tac Toe Variants")
        
        self.title_label = tk.Label(self.header_frame, text=title, 
                                   font=title_font, bg=self.colors["background"], 
                                   fg=self.colors["text"])
        self.title_label.pack(pady=10)
        
        # Score frame
        self.score_frame = tk.Frame(self.header_frame, bg=self.colors["background"])
        self.score_frame.pack(pady=5)
        
        # X score
        self.x_score_var = tk.StringVar(value="AI (X): 0")
        self.x_score_label = tk.Label(self.score_frame, textvariable=self.x_score_var,
                                     font=("Helvetica", 14), bg=self.colors["background"],
                                     fg=self.colors["x_color"], padx=20)
        self.x_score_label.pack(side=tk.LEFT)
        
        # O score
        self.o_score_var = tk.StringVar(value="You (O): 0")
        self.o_score_label = tk.Label(self.score_frame, textvariable=self.o_score_var,
                                     font=("Helvetica", 14), bg=self.colors["background"],
                                     fg=self.colors["o_color"], padx=20)
        self.o_score_label.pack(side=tk.RIGHT)

    def create_game_board(self):
        """Create the game board with animated buttons"""
        for i in range(3):
            for j in range(3):
                # Create a frame for each cell to add border effect
                cell_frame = tk.Frame(self.board_frame, bg=self.colors["grid_lines"],
                                     padx=3, pady=3)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                
                # Create the button with larger size
                self.buttons[i][j] = tk.Button(cell_frame, text='', font=('Helvetica', 36, 'bold'),
                                              width=3, height=1, bd=0,
                                              bg=self.colors["cell_bg"], activebackground=self.colors["cell_hover"],
                                              command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].pack(fill=tk.BOTH, expand=True)
                
                # Add hover effect
                self.buttons[i][j].bind("<Enter>", lambda event, btn=self.buttons[i][j]: 
                                      self.on_hover_enter(btn))
                self.buttons[i][j].bind("<Leave>", lambda event, btn=self.buttons[i][j]: 
                                      self.on_hover_leave(btn))

    def create_status_bar(self):
        """Create status bar to show game state"""
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Game ready to start")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var,
                                    font=("Helvetica", 12), bg=self.colors["background"],
                                    fg=self.colors["text"], pady=5)
        self.status_label.pack()

    def create_footer(self):
        """Create footer with buttons"""
        self.footer_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.footer_frame.pack(fill=tk.X, pady=10)
        
        # Calculate complexity button with improved styling
        self.calculate_button = tk.Button(self.footer_frame, 
                                        text="Calculate Complexity", 
                                        font=("Helvetica", 12),
                                        bg="#9b59b6", fg="white",
                                        activebackground="#8e44ad",
                                        bd=0, padx=15, pady=8,
                                        command=self.calculate_and_show_plot)
        self.calculate_button.pack(pady=10)
        
        # Reset button
        self.reset_button = tk.Button(self.footer_frame, 
                                     text="Reset Game", 
                                     font=("Helvetica", 12),
                                     bg="#e67e22", fg="white",
                                     activebackground="#d35400",
                                     bd=0, padx=15, pady=8,
                                     command=self.manual_reset)
        self.reset_button.pack(pady=10)

    def on_hover_enter(self, button):
        """Handle mouse enter event for hover effect"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.colors["cell_hover"])

    def on_hover_leave(self, button):
        """Handle mouse leave event for hover effect"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.colors["cell_bg"])

    def choose_starting_player(self):
        """Choose who starts the game"""
        result = messagebox.askyesno("Tic Tac Toe Variants", "Do you want to play first?")
        return 'O' if result else 'X'

    def evaluate(self, board):
        """Evaluate the board state"""
        # Check rows
        for i, row in enumerate(board):
            if row.count('X') == 3:
                self.winning_line = [(i, 0), (i, 1), (i, 2)]
                return 10
            elif row.count('O') == 3:
                self.winning_line = [(i, 0), (i, 1), (i, 2)]
                return -10

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] == 'X':
                    self.winning_line = [(0, col), (1, col), (2, col)]
                    return 10
                elif board[0][col] == 'O':
                    self.winning_line = [(0, col), (1, col), (2, col)]
                    return -10

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'X':
                self.winning_line = [(0, 0), (1, 1), (2, 2)]
                return 10
            elif board[0][0] == 'O':
                self.winning_line = [(0, 0), (1, 1), (2, 2)]
                return -10

        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == 'X':
                self.winning_line = [(0, 2), (1, 1), (2, 0)]
                return 10
            elif board[0][2] == 'O':
                self.winning_line = [(0, 2), (1, 1), (2, 0)]
                return -10

        # Add heuristic based on variant type
        if self.variant_type.startswith("center"):
            # Center control heuristic
            center_control = 0
            if board[1][1] == 'X':
                center_control += 1
            if board[1][1] == 'O':
                center_control -= 1
            return center_control
        elif self.variant_type.startswith("corner"):
            # Corner control heuristic
            corner_control = 0
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for i, j in corners:
                if board[i][j] == 'X':
                    corner_control += 0.5
                if board[i][j] == 'O':
                    corner_control -= 0.5
            return corner_control
        
        return 0

    def minimax(self, board, depth, is_maximizing):
        """Basic minimax algorithm"""
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
                        best = max(best, self.minimax(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        best = min(best, self.minimax(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
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
                        val = self.minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                        best = max(best, val)
                        alpha = max(alpha, best)
                        board[i][j] = '-'
                        if beta <= alpha:
                            break
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        val = self.minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                        best = min(best, val)
                        beta = min(beta, best)
                        board[i][j] = '-'
                        if beta <= alpha:
                            break
            return best

    def is_symmetric_position(self, board, i, j):
        """Check if a position is symmetric to one already evaluated"""
        # Implement symmetry reduction logic here
        # This is a simplified version
        if i == j:  # Diagonal symmetry
            return True
        return False

    def minimax_with_symmetry(self, board, depth, is_maximizing):
        """Minimax with symmetry reduction"""
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
                    if board[i][j] == '-' and not self.is_symmetric_position(board, i, j):
                        board[i][j] = 'X'
                        best = max(best, self.minimax_with_symmetry(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-' and not self.is_symmetric_position(board, i, j):
                        board[i][j] = 'O'
                        best = min(best, self.minimax_with_symmetry(board, depth + 1, not is_maximizing))
                        board[i][j] = '-'
            return best

    def heuristic_evaluation(self, board):
        """Heuristic evaluation function for faster computation"""
        # Count lines that can still be completed
        x_potential = 0
        o_potential = 0
        
        # Check rows
        for row in board:
            if 'O' not in row:
                x_potential += row.count('X')
            if 'X' not in row:
                o_potential += row.count('O')
                
        # Check columns
        for col in range(3):
            column = [board[row][col] for row in range(3)]
            if 'O' not in column:
                x_potential += column.count('X')
            if 'X' not in column:
                o_potential += column.count('O')
                
        # Check diagonals
        diag1 = [board[i][i] for i in range(3)]
        if 'O' not in diag1:
            x_potential += diag1.count('X')
        if 'X' not in diag1:
            o_potential += diag1.count('O')
            
        diag2 = [board[i][2-i] for i in range(3)]
        if 'O' not in diag2:
            x_potential += diag2.count('X')
        if 'X' not in diag2:
            o_potential += diag2.count('O')
            
        return x_potential - o_potential

    def minimax_with_heuristic(self, board, depth, max_depth, is_maximizing):
        """Minimax with depth limit and heuristic evaluation"""
        score = self.evaluate(board)
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any('-' in row for row in board) or depth >= max_depth:
            return self.heuristic_evaluation(board)

        if is_maximizing:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'X'
                        best = max(best, self.minimax_with_heuristic(board, depth + 1, max_depth, not is_maximizing))
                        board[i][j] = '-'
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        best = min(best, self.minimax_with_heuristic(board, depth + 1, max_depth, not is_maximizing))
                        board[i][j] = '-'
            return best

    def ai_move(self):
        """AI move based on the selected variant"""
        # Measure execution time
        start_time = time.time()

        # Different AI logic based on variant type
        if self.variant_type.startswith("center"):
            # Try to take center if available
            if self.board[1][1] == '-':
                row, col = 1, 1
            else:
                best_val = -math.inf
                best_move = (-1, -1)

                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '-':
                            self.board[i][j] = 'X'
                            
                            # Choose algorithm based on variant
                            if self.variant_type == "center":
                                move_val = self.evaluate(self.board)
                            elif self.variant_type == "center_minimax":
                                move_val = self.minimax(self.board, 0, False)
                            elif self.variant_type == "center_alpha_beta":
                                move_val = self.minimax_alpha_beta(self.board, 0, -math.inf, math.inf, False)
                            else:
                                move_val = self.evaluate(self.board)
                                
                            self.board[i][j] = '-'

                            if move_val > best_val:
                                best_move = (i, j)
                                best_val = move_val

                row, col = best_move
                
        elif self.variant_type.startswith("corner"):
            # Try to take a corner if available
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            corner_available = False
            
            for i, j in corners:
                if self.board[i][j] == '-':
                    corner_available = True
                    break
                    
            if corner_available:
                best_val = -math.inf
                best_move = (-1, -1)
                
                for i, j in corners:
                    if self.board[i][j] == '-':
                        self.board[i][j] = 'X'
                        
                        # Choose algorithm based on variant
                        if self.variant_type == "corner":
                            move_val = self.evaluate(self.board)
                        elif self.variant_type == "corner_minimax":
                            move_val = self.minimax(self.board, 0, False)
                        elif self.variant_type == "corner_alpha_beta":
                            move_val = self.minimax_alpha_beta(self.board, 0, -math.inf, math.inf, False)
                        else:
                            move_val = self.evaluate(self.board)
                            
                        self.board[i][j] = '-'
                        
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
                            
                row, col = best_move
            else:
                # If no corner is available, use regular minimax
                best_val = -math.inf
                best_move = (-1, -1)
                
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '-':
                            self.board[i][j] = 'X'
                            
                            # Choose algorithm based on variant
                            if self.variant_type == "corner":
                                move_val = self.evaluate(self.board)
                            elif self.variant_type == "corner_minimax":
                                move_val = self.minimax(self.board, 0, False)
                            elif self.variant_type == "corner_alpha_beta":
                                move_val = self.minimax_alpha_beta(self.board, 0, -math.inf, math.inf, False)
                            else:
                                move_val = self.evaluate(self.board)
                                
                            self.board[i][j] = '-'
                            
                            if move_val > best_val:
                                best_move = (i, j)
                                best_val = move_val
                                
                row, col = best_move
                
        elif self.variant_type == "minimax":
            # Basic minimax
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
            
        elif self.variant_type == "minimax_alpha_beta":
            # Minimax with alpha-beta pruning
            best_val = -math.inf
            best_move = (-1, -1)
            
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = 'X'
                        move_val = self.minimax_alpha_beta(self.board, 0, -math.inf, math.inf, False)
                        self.board[i][j] = '-'
                        
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
                            
            row, col = best_move
            
        elif self.variant_type == "symmetry":
            # Minimax with symmetry reduction
            best_val = -math.inf
            best_move = (-1, -1)
            
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-' and not self.is_symmetric_position(self.board, i, j):
                        self.board[i][j] = 'X'
                        move_val = self.minimax_with_symmetry(self.board, 0, False)
                        self.board[i][j] = '-'
                        
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
                            
            row, col = best_move
            
        elif self.variant_type == "heuristic":
            # Minimax with heuristic evaluation
            best_val = -math.inf
            best_move = (-1, -1)
            
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = 'X'
                        move_val = self.minimax_with_heuristic(self.board, 0, 3, False)  # Depth limit of 3
                        self.board[i][j] = '-'
                        
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
                            
            row, col = best_move
            
        else:
            # Default to basic minimax
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

        # Update board state
        self.board[row][col] = 'X'
        
        # Animate the move
        self.animate_button(row, col, 'X')
        self.buttons[row][col].config(state=tk.DISABLED)

        # Check game result
        result = self.evaluate(self.board)
        if result == 10:
            self.highlight_winning_line()
            self.x_score += 1
            self.x_score_var.set(f"AI (X): {self.x_score}")
            self.status_var.set("AI wins!")
            self.buttons[0][0].after(1500, lambda: messagebox.showinfo("Tic Tac Toe Variants", "AI wins!"))
            self.buttons[0][0].after(1600, self.reset_board)
        elif not any('-' in row for row in self.board):
            self.status_var.set("It's a tie!")
            self.buttons[0][0].after(1000, lambda: messagebox.showinfo("Tic Tac Toe Variants", "It's a tie!"))
            self.buttons[0][0].after(1100, self.reset_board)
        else:
            self.current_player = 'O'
            self.status_var.set("Your turn (O)")

        # Calculate and store metrics
        end_time = time.time()
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)

        space_used = sys.getsizeof(self.board)
        self.space_complexity.append(space_used)

        print(f"AI Move Execution Time: {execution_time} seconds, Space Complexity: {space_used} bytes")

    def animate_button(self, row, col, player):
        """Animate the button when a move is made"""
        button = self.buttons[row][col]
        
        # Set initial state
        button.config(text='')
        
        # Configure colors based on player
        if player == 'X':
            fg_color = self.colors["x_color"]
            bg_color = self.colors["x_border"]
        else:
            fg_color = self.colors["o_color"]
            bg_color = self.colors["o_border"]
        
        # Animation frames
        def frame1():
            button.config(bg=bg_color)
            button.after(50, frame2)
            
        def frame2():
            button.config(text=player, fg=fg_color)
            button.after(50, frame3)
            
        def frame3():
            button.config(relief=tk.SUNKEN)
            
        # Start animation
        button.after(0, frame1)

    def highlight_winning_line(self):
        """Highlight the winning line with animation"""
        if not self.winning_line:
            return
            
        # Determine winner color
        winner = self.board[self.winning_line[0][0]][self.winning_line[0][1]]
        highlight_color = self.colors["x_color"] if winner == 'X' else self.colors["o_color"]
        
        # Animation variables
        flash_count = 0
        max_flashes = 5
        
        def flash_on():
            nonlocal flash_count
            if flash_count >= max_flashes:
                return
                
            # Highlight winning cells
            for row, col in self.winning_line:
                self.buttons[row][col].config(bg=highlight_color)
                
            flash_count += 1
            self.buttons[0][0].after(300, flash_off)
            
        def flash_off():
            # Return to normal color
            for row, col in self.winning_line:
                player = self.board[row][col]
                bg_color = self.colors["x_border"] if player == 'X' else self.colors["o_border"]
                self.buttons[row][col].config(bg=bg_color)
                
            self.buttons[0][0].after(300, flash_on)
            
        # Start animation
        flash_on()

    def on_click(self, row, col):
        """Handle player click on a cell"""
        if self.board[row][col] == '-' and self.current_player == 'O':
            # Update board state
            self.board[row][col] = 'O'
            
            # Animate the move
            self.animate_button(row, col, 'O')
            self.buttons[row][col].config(state=tk.DISABLED)

            # Check game result
            result = self.evaluate(self.board)
            if result == -10:
                self.highlight_winning_line()
                self.o_score += 1
                self.o_score_var.set(f"You (O): {self.o_score}")
                self.status_var.set("You win!")
                self.buttons[0][0].after(1500, lambda: messagebox.showinfo("Tic Tac Toe Variants", "You win!"))
                self.buttons[0][0].after(1600, self.reset_board)
            elif any('-' in row for row in self.board):
                self.current_player = 'X'
                self.status_var.set("AI (X) is thinking...")
                self.buttons[0][0].after(800, self.ai_move)
            else:
                self.status_var.set("It's a tie!")
                self.buttons[0][0].after(1000, lambda: messagebox.showinfo("Tic Tac Toe Variants", "It's a tie!"))
                self.buttons[0][0].after(1100, self.reset_board)

    def reset_board(self):
        """Reset the game board with animation"""
        play_again = messagebox.askyesno("Tic Tac Toe Variants", "Do you want to play again?")
        if play_again:
            # Fade out animation
            def fade_out(alpha):
                if alpha > 0:
                    for i in range(3):
                        for j in range(3):
                            # Gradually fade to background color
                            blend_factor = alpha / 10
                            r1, g1, b1 = self.buttons[i][j].winfo_rgb()
                            r2, g2, b2 = self.board_frame.winfo_rgb()
                            r = int(r1 * blend_factor + r2 * (1 - blend_factor))
                            g = int(g1 * blend_factor + g2 * (1 - blend_factor))
                            b = int(b1 * blend_factor + b2 * (1 - blend_factor))
                            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
                            self.buttons[i][j].config(bg=color)
                    self.buttons[0][0].after(50, lambda: fade_out(alpha - 1))
                else:
                    # Reset the board
                    for i in range(3):
                        for j in range(3):
                            self.board[i][j] = '-'
                            self.buttons[i][j].config(
                                text='', 
                                state=tk.NORMAL,
                                bg=self.colors["cell_bg"],
                                relief=tk.RAISED
                            )
                    
                    # Reset game state
                    self.winning_line = None
                    self.current_player = self.choose_starting_player()
                    
                    # Start new game
                    if self.current_player == 'X':
                        self.status_var.set("AI (X) is thinking...")
                        self.buttons[0][0].after(800, self.ai_move)
                    else:
                        self.status_var.set("Your turn (O)")
            
            # Start fade out animation
            fade_out(10)

    def manual_reset(self):
        """Manual reset triggered by reset button"""
        self.reset_board()

    def calculate_and_show_plot(self):
        """Calculate and show complexity plot with improved styling"""
        if not self.execution_times:
            messagebox.showinfo("Tic Tac Toe Variants", "No data available yet. Play some games first!")
            return
            
        # Create a more visually appealing plot
        plt.figure(figsize=(10, 6))
        plt.style.use('ggplot')
        
        moves = list(range(1, len(self.execution_times) + 1))
        
        # Plot time complexity
        plt.subplot(2, 1, 1)
        plt.plot(moves, self.execution_times, marker='o', color='#3498db', 
                linewidth=2, markersize=8, label='Time Complexity')
        plt.fill_between(moves, self.execution_times, alpha=0.3, color='#3498db')
        plt.xlabel('AI Moves', fontsize=12)
        plt.ylabel('Time (seconds)', fontsize=12)
        plt.title('Time Complexity Analysis', fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Plot space complexity
        plt.subplot(2, 1, 2)
        plt.plot(moves, self.space_complexity, marker='s', color='#e74c3c',
                linewidth=2, markersize=8, label='Space Complexity')
        plt.fill_between(moves, self.space_complexity, alpha=0.3, color='#e74c3c')
        plt.xlabel('AI Moves', fontsize=12)
        plt.ylabel('Memory (bytes)', fontsize=12)
        plt.title('Space Complexity Analysis', fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Calculate and display averages
        average_time_complexity = sum(self.execution_times) / len(self.execution_times)
        average_space_complexity = sum(self.space_complexity) / len(self.space_complexity)
        
        messagebox.showinfo("Complexity Analysis", 
                          f"Average Time Complexity: {average_time_complexity:.6f} seconds\n"
                          f"Average Space Complexity: {average_space_complexity:.2f} bytes")

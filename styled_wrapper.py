import tkinter as tk
from tkinter import messagebox, font
import time
import matplotlib.pyplot as plt
import math
import sys

class StyledTicTacToe:
    """
    A wrapper class that enhances the visual style of TicTacToe games
    while preserving the original game logic.
    """
    def __init__(self, original_game_class):
        self.original_game_class = original_game_class
        
    def create_game(self, master):
        # Configure window properties for modern look
        master.title("Tic Tac Toe")
        master.configure(bg="#2c3e50")
        
        # Create a main frame to hold everything
        self.main_frame = tk.Frame(master, bg="#2c3e50", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header with title
        self.create_header(self.main_frame)
        
        # Create game board frame with modern styling
        self.board_frame = tk.Frame(self.main_frame, bg="#2c3e50", 
                                   bd=5, relief=tk.RIDGE, padx=10, pady=10)
        self.board_frame.pack(pady=20)
        
        # Create the original game instance but don't use its UI
        # We'll create our own styled UI but use the original game logic
        self.game = self.original_game_class(self.board_frame)
        
        # Override the original buttons with styled ones
        self.create_styled_buttons(self.board_frame)
        
        # Create styled calculate button
        self.create_styled_calculate_button(self.main_frame)
        
        # Start game if AI goes first (using original game logic)
        if self.game.current_player == 'X':
            self.game.ai_move_with_center()
    
    def create_header(self, parent):
        """Create a styled header with game title"""
        header_frame = tk.Frame(parent, bg="#2c3e50")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Game title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(header_frame, text="Tic Tac Toe", 
                              font=title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=10)
        
        # Add a separator
        separator_frame = tk.Frame(parent, height=2, bg="#ecf0f1")
        separator_frame.pack(fill=tk.X, pady=(0, 20))
    
    def create_styled_buttons(self, parent):
        """Create styled game buttons while preserving original logic"""
        # Define colors
        self.colors = {
            "cell_bg": "#3498db",      # Blue
            "cell_hover": "#2980b9",   # Darker blue
            "x_color": "#e74c3c",      # Red
            "o_color": "#2ecc71",      # Green
        }
        
        # Create styled buttons
        for i in range(3):
            for j in range(3):
                # Create a frame for each cell to add border effect
                cell_frame = tk.Frame(parent, bg="#ecf0f1", padx=3, pady=3)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                
                # Create the button with larger size and better styling
                styled_button = tk.Button(cell_frame, text='', font=('Helvetica', 36, 'bold'),
                                        width=3, height=1, bd=0,
                                        bg=self.colors["cell_bg"], activebackground=self.colors["cell_hover"],
                                        command=lambda row=i, col=j: self.on_click_wrapper(row, col))
                styled_button.pack(fill=tk.BOTH, expand=True)
                
                # Add hover effect
                styled_button.bind("<Enter>", lambda event, btn=styled_button: 
                                 self.on_hover_enter(btn))
                styled_button.bind("<Leave>", lambda event, btn=styled_button: 
                                 self.on_hover_leave(btn))
                
                # Replace the original button with our styled one
                self.game.buttons[i][j] = styled_button
    
    def create_styled_calculate_button(self, parent):
        """Create a styled calculate button"""
        footer_frame = tk.Frame(parent, bg="#2c3e50")
        footer_frame.pack(fill=tk.X, pady=10)
        
        # Replace the original calculate button with a styled one
        styled_calculate_button = tk.Button(footer_frame, 
                                          text="Calculate Complexity", 
                                          font=("Helvetica", 12),
                                          bg="#9b59b6", fg="white",
                                          activebackground="#8e44ad",
                                          bd=0, padx=15, pady=8,
                                          command=self.game.calculate_and_show_plot)
        styled_calculate_button.pack(pady=10)
        
        # Add hover effect
        styled_calculate_button.bind("<Enter>", lambda e: styled_calculate_button.config(bg="#8e44ad"))
        styled_calculate_button.bind("<Leave>", lambda e: styled_calculate_button.config(bg="#9b59b6"))
        
        # Replace the original button
        self.game.calculate_button = styled_calculate_button
    
    def on_hover_enter(self, button):
        """Handle mouse enter event for hover effect"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.colors["cell_hover"])
    
    def on_hover_leave(self, button):
        """Handle mouse leave event for hover effect"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.colors["cell_bg"])
    
    def on_click_wrapper(self, row, col):
        """Wrapper for the original on_click method with visual enhancements"""
        # Call the original on_click method to preserve game logic
        self.game.on_click(row, col)
        
        # Add visual enhancements for the player's move
        if self.game.board[row][col] == 'O':
            self.game.buttons[row][col].config(fg=self.colors["o_color"])
        
        # The AI's move is handled by the original game logic
        # We just need to ensure X moves have the right color
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == 'X' and self.game.buttons[i][j]['fg'] != self.colors["x_color"]:
                    self.game.buttons[i][j].config(fg=self.colors["x_color"])

# This function will be used to create a styled version of any TicTacToe variant
def create_styled_game(original_game_class):
    def wrapper(root):
        styled_game = StyledTicTacToe(original_game_class)
        styled_game.create_game(root)
        return styled_game
    return wrapper

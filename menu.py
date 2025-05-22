import tkinter as tk
from tkinter import messagebox, font
import subprocess
import sys
import os

# Map each submenu option to the script filename you provided
menu_structure = {
    "Center Control": {
        "Center Control Only": "center only.py",
        "Center Control with Minimax": "center minimax.py",
        "Center Control with Minimax & Alpha-Beta": "center minimax with Alphabeta.py"
    },
    "Corner Control": {
        "Corner Control Only": "corner only.py",
        "Corner Control with Minimax": "corner with minimax.py",
        "Corner Control with Minimax & Alpha-Beta": "corner minimax with Alphabeta.py"
    },
    "Minimax": {
        "Basic Minimax": "minimaxtkinter.py",
        "Minimax Alpha-Beta": "minimaxtkinter with alpha.py",
        "Symmetry Reduction": "Symmetry reduction.py",
        "Heuristic Reduction": "heuristic reduction.py"
    }
}

class ModernMenuApp:
    def __init__(self, root):
        # Set window properties
        self.root = root
        self.root.title("Tic Tac Toe Variants")
        self.root.geometry("600x650")
        self.root.minsize(550, 600)
        
        # Center the window on screen
        self.center_window()
        
        # Define colors to match game board
        self.colors = {
            "background": "#2c3e50",  # Dark blue
            "button_bg": "#3498db",    # Blue
            "button_hover": "#2980b9", # Darker blue
            "primary_button": "#9b59b6", # Purple
            "primary_hover": "#8e44ad",  # Darker purple
            "secondary_button": "#e67e22", # Orange
            "secondary_hover": "#d35400", # Darker orange
            "x_color": "#e74c3c",      # Red
            "o_color": "#2ecc71",      # Green
            "grid_lines": "#ecf0f1",   # Light gray/white
            "text": "#ffffff"          # White
        }
        
        # Configure the root window
        self.root.configure(bg=self.colors["background"])
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg=self.colors["background"], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.create_header()
        
        # Create content frame
        self.create_content()
        
        # Create footer
        self.create_footer()
        
        # Initialize the options
        self.update_options(self.category_var.get())
        
        # Create tooltips
        self.create_tooltips()
        
        # Set initial status
        self.status_var.set("Ready to launch a game variant")

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_header(self):
        """Create the header with title"""
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Game title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.title_label = tk.Label(self.header_frame, text="Tic Tac Toe Variants", 
                                   font=title_font, bg=self.colors["background"], 
                                   fg=self.colors["text"])
        self.title_label.pack(pady=15)
        
        # Add a separator
        separator_frame = tk.Frame(self.main_frame, height=2, bg=self.colors["grid_lines"])
        separator_frame.pack(fill=tk.X, pady=(0, 20))

    def create_content(self):
        """Create the main content section with animated elements"""
        # Create a frame with border
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors["background"],
                                     bd=5, relief=tk.RIDGE, padx=15, pady=15)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Category selection
        category_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        category_frame.pack(fill=tk.X, pady=10)
        
        self.category_label = tk.Label(category_frame, text="Select Category:", 
                                     font=("Helvetica", 14, "bold"),
                                     bg=self.colors["background"], fg=self.colors["text"])
        self.category_label.pack(side=tk.LEFT, padx=10)
        
        self.category_var = tk.StringVar(value="Center Control")
        
        # Create custom dropdown for categories
        self.category_menu_frame = tk.Frame(category_frame, bg=self.colors["button_bg"],
                                          bd=0, relief=tk.RAISED, padx=2, pady=2)
        self.category_menu_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)
        
        self.category_menu_button = tk.Menubutton(self.category_menu_frame, 
                                                textvariable=self.category_var,
                                                font=("Helvetica", 12),
                                                bg=self.colors["button_bg"],
                                                fg=self.colors["text"],
                                                activebackground=self.colors["button_hover"],
                                                activeforeground=self.colors["text"],
                                                bd=0, padx=10, pady=5,
                                                relief=tk.FLAT,
                                                highlightthickness=0)
        self.category_menu_button.pack(fill=tk.X)
        
        self.category_menu = tk.Menu(self.category_menu_button, tearoff=0,
                                    bg=self.colors["background"],
                                    fg=self.colors["text"],
                                    activebackground=self.colors["button_hover"],
                                    activeforeground=self.colors["text"],
                                    bd=0)
        self.category_menu_button["menu"] = self.category_menu
        
        for category in menu_structure.keys():
            self.category_menu.add_command(
                label=category,
                command=lambda cat=category: self.update_category(cat)
            )
        
        # Add hover effect to category menu
        self.category_menu_button.bind("<Enter>", lambda e: self.on_hover_enter(self.category_menu_button, self.colors["button_hover"]))
        self.category_menu_button.bind("<Leave>", lambda e: self.on_hover_leave(self.category_menu_button, self.colors["button_bg"]))
        
        # Add a separator
        separator_frame1 = tk.Frame(self.content_frame, height=1, bg=self.colors["grid_lines"])
        separator_frame1.pack(fill=tk.X, pady=10)
        
        # Option selection
        option_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        option_frame.pack(fill=tk.X, pady=10)
        
        self.option_label = tk.Label(option_frame, text="Select Variant:", 
                                   font=("Helvetica", 14, "bold"),
                                   bg=self.colors["background"], fg=self.colors["text"])
        self.option_label.pack(side=tk.LEFT, padx=10)
        
        self.option_var = tk.StringVar()
        
        # Create custom dropdown for options
        self.option_menu_frame = tk.Frame(option_frame, bg=self.colors["button_bg"],
                                        bd=0, relief=tk.RAISED, padx=2, pady=2)
        self.option_menu_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)
        
        self.option_menu_button = tk.Menubutton(self.option_menu_frame, 
                                              textvariable=self.option_var,
                                              font=("Helvetica", 12),
                                              bg=self.colors["button_bg"],
                                              fg=self.colors["text"],
                                              activebackground=self.colors["button_hover"],
                                              activeforeground=self.colors["text"],
                                              bd=0, padx=10, pady=5,
                                              relief=tk.FLAT,
                                              highlightthickness=0)
        self.option_menu_button.pack(fill=tk.X)
        
        self.option_menu = tk.Menu(self.option_menu_button, tearoff=0,
                                  bg=self.colors["background"],
                                  fg=self.colors["text"],
                                  activebackground=self.colors["button_hover"],
                                  activeforeground=self.colors["text"],
                                  bd=0)
        self.option_menu_button["menu"] = self.option_menu
        
        # Add hover effect to option menu
        self.option_menu_button.bind("<Enter>", lambda e: self.on_hover_enter(self.option_menu_button, self.colors["button_hover"]))
        self.option_menu_button.bind("<Leave>", lambda e: self.on_hover_leave(self.option_menu_button, self.colors["button_bg"]))
        
        # Add a separator
        separator_frame2 = tk.Frame(self.content_frame, height=1, bg=self.colors["grid_lines"])
        separator_frame2.pack(fill=tk.X, pady=10)
        
        # Add a description frame
        self.description_frame = tk.Frame(self.content_frame, bg=self.colors["background"],
                                        bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.description_frame.pack(fill=tk.X, pady=15)
        
        self.description_label = tk.Label(self.description_frame,
                                        text="Description:",
                                        font=("Helvetica", 12, "bold"),
                                        bg=self.colors["background"],
                                        fg=self.colors["text"])
        self.description_label.pack(anchor="w", pady=(0, 5))
        
        self.description_text = tk.Text(self.description_frame, 
                                      height=5, 
                                      width=50, 
                                      wrap=tk.WORD,
                                      bg=self.colors["background"],
                                      fg=self.colors["text"],
                                      font=("Helvetica", 11),
                                      relief=tk.FLAT,
                                      padx=5, pady=5,
                                      borderwidth=0,
                                      highlightthickness=0)
        self.description_text.pack(fill=tk.X, pady=5)
        self.description_text.insert(tk.END, "Select a variant to see its description.")
        self.description_text.config(state=tk.DISABLED)
        
        # Add a separator
        separator_frame3 = tk.Frame(self.content_frame, height=1, bg=self.colors["grid_lines"])
        separator_frame3.pack(fill=tk.X, pady=10)
        
        # Run button with animation
        self.button_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        self.button_frame.pack(pady=15)
        
        self.run_button = tk.Button(self.button_frame, 
                                  text="Run Selected Variant", 
                                  font=("Helvetica", 14, "bold"),
                                  bg=self.colors["primary_button"],
                                  fg=self.colors["text"],
                                  activebackground=self.colors["primary_hover"],
                                  activeforeground=self.colors["text"],
                                  bd=0, padx=20, pady=10,
                                  relief=tk.RAISED,
                                  command=self.run_script)
        self.run_button.pack()
        
        # Add hover effect to run button
        self.run_button.bind("<Enter>", lambda e: self.on_hover_enter(self.run_button, self.colors["primary_hover"]))
        self.run_button.bind("<Leave>", lambda e: self.on_hover_leave(self.run_button, self.colors["primary_button"]))
        
        # Add click animation to run button
        self.run_button.bind("<Button-1>", self.on_button_click)
        self.run_button.bind("<ButtonRelease-1>", lambda e: self.on_hover_enter(self.run_button, self.colors["primary_hover"]))

    def create_footer(self):
        """Create the footer section"""
        # Add a separator
        separator_frame = tk.Frame(self.main_frame, height=2, bg=self.colors["grid_lines"])
        separator_frame.pack(fill=tk.X, pady=(20, 10))
        
        self.footer_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.footer_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.footer_frame, 
                                 textvariable=self.status_var,
                                 font=("Helvetica", 10),
                                 bg=self.colors["background"],
                                 fg=self.colors["text"])
        self.status_bar.pack(side=tk.LEFT, padx=10)
        
        # Button frame for footer buttons
        button_frame = tk.Frame(self.footer_frame, bg=self.colors["background"])
        button_frame.pack(side=tk.RIGHT)
        
        # Help button
        self.help_button = tk.Button(button_frame, 
                                   text="Help", 
                                   font=("Helvetica", 10),
                                   bg=self.colors["secondary_button"],
                                   fg=self.colors["text"],
                                   activebackground=self.colors["secondary_hover"],
                                   activeforeground=self.colors["text"],
                                   bd=0, padx=15, pady=5,
                                   command=self.show_help)
        self.help_button.pack(side=tk.RIGHT, padx=10)
        
        # Add hover effect to help button
        self.help_button.bind("<Enter>", lambda e: self.on_hover_enter(self.help_button, self.colors["secondary_hover"]))
        self.help_button.bind("<Leave>", lambda e: self.on_hover_leave(self.help_button, self.colors["secondary_button"]))
        
        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar(value=True)  # Default to dark mode to match game board
        self.dark_mode_check = tk.Checkbutton(button_frame, 
                                            text="Light Mode", 
                                            variable=self.dark_mode_var,
                                            font=("Helvetica", 10),
                                            bg=self.colors["background"],
                                            fg=self.colors["text"],
                                            selectcolor=self.colors["background"],
                                            activebackground=self.colors["background"],
                                            activeforeground=self.colors["text"],
                                            command=self.toggle_dark_mode)
        self.dark_mode_check.pack(side=tk.RIGHT, padx=10)

    def on_hover_enter(self, widget, color):
        """Handle mouse enter event for hover effect"""
        widget.config(bg=color)

    def on_hover_leave(self, widget, color):
        """Handle mouse leave event for hover effect"""
        widget.config(bg=color)

    def on_button_click(self, event):
        """Handle button click animation"""
        self.run_button.config(relief=tk.SUNKEN, bg=self.colors["primary_button"])
        # Schedule return to normal state
        self.run_button.after(100, lambda: self.run_button.config(relief=tk.RAISED))

    def update_category(self, category):
        """Update category and refresh options"""
        self.category_var.set(category)
        self.update_options(category)
        
        # Animate the category change
        def flash():
            self.category_menu_button.config(bg=self.colors["button_hover"])
            self.category_menu_button.after(100, lambda: self.category_menu_button.config(bg=self.colors["button_bg"]))
            
        flash()

    def update_options(self, category):
        """Update the options menu based on selected category"""
        options = list(menu_structure[category].keys())
        self.option_var.set(options[0])
        
        # Clear the option menu
        self.option_menu.delete(0, tk.END)
        
        # Add new options
        for option in options:
            self.option_menu.add_command(
                label=option,
                command=lambda opt=option: self.update_option(opt)
            )
        
        # Update description based on selection
        self.update_description(category, options[0])
        
        # Update status bar
        self.status_var.set(f"Category: {category} | Selected: {options[0]}")
        
        # Animate the option change
        def flash():
            self.option_menu_button.config(bg=self.colors["button_hover"])
            self.option_menu_button.after(100, lambda: self.option_menu_button.config(bg=self.colors["button_bg"]))
            
        flash()

    def update_option(self, option):
        """Update selected option and description"""
        self.option_var.set(option)
        self.update_description(self.category_var.get(), option)
        self.status_var.set(f"Category: {self.category_var.get()} | Selected: {option}")
        
        # Animate the option change
        def flash():
            self.option_menu_button.config(bg=self.colors["button_hover"])
            self.option_menu_button.after(100, lambda: self.option_menu_button.config(bg=self.colors["button_bg"]))
            
        flash()

    def update_description(self, category, option):
        """Update the description text based on selection with animation"""
        descriptions = {
            "Center Control": {
                "Center Control Only": "Basic strategy focusing on controlling the center position of the board.",
                "Center Control with Minimax": "Center control strategy enhanced with Minimax algorithm for better decision making.",
                "Center Control with Minimax & Alpha-Beta": "Advanced center control using Minimax with Alpha-Beta pruning for efficiency."
            },
            "Corner Control": {
                "Corner Control Only": "Strategy focusing on controlling the corner positions of the board.",
                "Corner Control with Minimax": "Corner control strategy enhanced with Minimax algorithm for better decision making.",
                "Corner Control with Minimax & Alpha-Beta": "Advanced corner control using Minimax with Alpha-Beta pruning for efficiency."
            },
            "Minimax": {
                "Basic Minimax": "Implementation of the Minimax algorithm for optimal move selection.",
                "Minimax Alpha-Beta": "Enhanced Minimax with Alpha-Beta pruning for faster computation.",
                "Symmetry Reduction": "Minimax with symmetry reduction to decrease the search space.",
                "Heuristic Reduction": "Minimax with heuristic evaluation to improve performance."
            }
        }
        
        description = descriptions.get(category, {}).get(option, "No description available.")
        
        # Animate the description change
        def fade_out():
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.config(state=tk.DISABLED)
            self.description_text.after(50, lambda: fade_in(description))
            
        def fade_in(text):
            self.description_text.config(state=tk.NORMAL)
            self.description_text.insert(tk.END, text)
            self.description_text.config(state=tk.DISABLED)
            
        fade_out()

    def run_script(self):
        """Run the selected script with animation"""
        category = self.category_var.get()
        option = self.option_var.get()
        script_name = menu_structure[category][option]
        
        # Animate button press
        self.run_button.config(relief=tk.SUNKEN)
        self.run_button.after(200, lambda: self.run_button.config(relief=tk.RAISED))
        
        if not os.path.isfile(script_name):
            messagebox.showerror("Error", f"Script '{script_name}' not found.")
            self.status_var.set(f"Error: Script '{script_name}' not found")
            return
        
        # Update status with animation
        def update_status(text, count=0):
            if count < 3:
                dots = "." * (count + 1)
                self.status_var.set(f"{text}{dots}")
                self.root.after(300, lambda: update_status(text, (count + 1) % 3))
            else:
                self.status_var.set(f"Launched: {script_name}")
                
        update_status(f"Launching {script_name}")
        
        # Run the script in a separate process
        try:
            # Use python executable compatible with current environment
            subprocess.Popen([sys.executable, script_name])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script: {e}")
            self.status_var.set(f"Error: Failed to run script")

    def show_help(self):
        """Show help information with improved styling"""
        help_text = """
        Tic Tac Toe Variants Help
        
        This application allows you to run different Tic Tac Toe game variants:
        
        1. Select a category from the dropdown menu
        2. Choose a specific variant from the second dropdown
        3. Read the description to understand the variant
        4. Click "Run Selected Variant" to start the game
        
        If you encounter any issues, ensure all script files are in the same directory as this application.
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x350")
        help_window.configure(bg=self.colors["background"])
        help_window.resizable(False, False)
        
        # Center the help window
        help_window.update_idletasks()
        width = help_window.winfo_width()
        height = help_window.winfo_height()
        x = (help_window.winfo_screenwidth() // 2) - (width // 2)
        y = (help_window.winfo_screenheight() // 2) - (height // 2)
        help_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a frame with border
        help_frame = tk.Frame(help_window, bg=self.colors["background"],
                             bd=5, relief=tk.RIDGE, padx=15, pady=15)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        help_label = tk.Label(help_frame, 
                             text="Tic Tac Toe Variants - Help", 
                             font=("Helvetica", 16, "bold"),
                             bg=self.colors["background"],
                             fg=self.colors["text"])
        help_label.pack(pady=10)
        
        # Add a separator
        separator_frame = tk.Frame(help_frame, height=2, bg=self.colors["grid_lines"])
        separator_frame.pack(fill=tk.X, pady=10)
        
        help_text_widget = tk.Text(help_frame, 
                                  wrap=tk.WORD, 
                                  bg=self.colors["background"],
                                  fg=self.colors["text"],
                                  font=("Helvetica", 11),
                                  relief=tk.FLAT,
                                  padx=10, pady=10,
                                  borderwidth=0,
                                  highlightthickness=0)
        help_text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        # Add a separator
        separator_frame2 = tk.Frame(help_frame, height=2, bg=self.colors["grid_lines"])
        separator_frame2.pack(fill=tk.X, pady=10)
        
        close_button = tk.Button(help_frame, 
                               text="Close", 
                               command=help_window.destroy,
                               font=("Helvetica", 12),
                               bg=self.colors["secondary_button"],
                               fg=self.colors["text"],
                               activebackground=self.colors["secondary_hover"],
                               activeforeground=self.colors["text"],
                               bd=0, padx=20, pady=8)
        close_button.pack(pady=10)
        
        # Add hover effect to close button
        close_button.bind("<Enter>", lambda e: close_button.config(bg=self.colors["secondary_hover"]))
        close_button.bind("<Leave>", lambda e: close_button.config(bg=self.colors["secondary_button"]))

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        if self.dark_mode_var.get():  # Light mode
            # Light mode colors
            light_colors = {
                "background": "#f5f5f5",  # Light gray
                "button_bg": "#3498db",    # Blue
                "button_hover": "#2980b9", # Darker blue
                "primary_button": "#9b59b6", # Purple
                "primary_hover": "#8e44ad",  # Darker purple
                "secondary_button": "#e67e22", # Orange
                "secondary_hover": "#d35400", # Darker orange
                "x_color": "#e74c3c",      # Red
                "o_color": "#2ecc71",      # Green
                "grid_lines": "#2c3e50",   # Dark blue
                "text": "#2c3e50"          # Dark blue
            }
            
            # Update colors
            self.colors = light_colors
            
            # Update all widgets
            self.root.configure(bg=self.colors["background"])
            self.main_frame.configure(bg=self.colors["background"])
            
            # Update header
            self.header_frame.configure(bg=self.colors["background"])
            self.title_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            
            # Update content frame
            self.content_frame.configure(bg=self.colors["background"])
            
            # Update category section
            self.category_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.category_menu_frame.configure(bg=self.colors["button_bg"])
            self.category_menu_button.configure(bg=self.colors["button_bg"], fg=self.colors["text"],
                                              activebackground=self.colors["button_hover"])
            
            # Update option section
            self.option_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.option_menu_frame.configure(bg=self.colors["button_bg"])
            self.option_menu_button.configure(bg=self.colors["button_bg"], fg=self.colors["text"],
                                            activebackground=self.colors["button_hover"])
            
            # Update description section
            self.description_frame.configure(bg=self.colors["background"])
            self.description_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.description_text.configure(bg=self.colors["background"], fg=self.colors["text"])
            
            # Update button
            self.button_frame.configure(bg=self.colors["background"])
            self.run_button.configure(bg=self.colors["primary_button"], fg=self.colors["text"],
                                    activebackground=self.colors["primary_hover"])
            
            self.footer_frame.configure(bg=self.colors["background"])
            self.status_bar.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.help_button.configure(bg=self.colors["secondary_button"], fg=self.colors["text"],
                                     activebackground=self.colors["secondary_hover"])
            self.dark_mode_check.configure(bg=self.colors["background"], fg=self.colors["text"],
                                         selectcolor=self.colors["background"],
                                         activebackground=self.colors["background"])
            
        else:  # Dark mode
            # Dark mode colors
            dark_colors = {
                "background": "#2c3e50",  # Dark blue
                "button_bg": "#3498db",    # Blue
                "button_hover": "#2980b9", # Darker blue
                "primary_button": "#9b59b6", # Purple
                "primary_hover": "#8e44ad",  # Darker purple
                "secondary_button": "#e67e22", # Orange
                "secondary_hover": "#d35400", # Darker orange
                "x_color": "#e74c3c",      # Red
                "o_color": "#2ecc71",      # Green
                "grid_lines": "#ecf0f1",   # Light gray/white
                "text": "#ffffff"          # White
            }
            
            self.colors = dark_colors
            
            self.root.configure(bg=self.colors["background"])
            self.main_frame.configure(bg=self.colors["background"])
            
            self.header_frame.configure(bg=self.colors["background"])
            self.title_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            
            self.content_frame.configure(bg=self.colors["background"])
            
            self.category_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.category_menu_frame.configure(bg=self.colors["button_bg"])
            self.category_menu_button.configure(bg=self.colors["button_bg"], fg=self.colors["text"],
                                              activebackground=self.colors["button_hover"])
            
            self.option_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.option_menu_frame.configure(bg=self.colors["button_bg"])
            self.option_menu_button.configure(bg=self.colors["button_bg"], fg=self.colors["text"],
                                            activebackground=self.colors["button_hover"])
            
            self.description_frame.configure(bg=self.colors["background"])
            self.description_label.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.description_text.configure(bg=self.colors["background"], fg=self.colors["text"])
            
            self.button_frame.configure(bg=self.colors["background"])
            self.run_button.configure(bg=self.colors["primary_button"], fg=self.colors["text"],
                                    activebackground=self.colors["primary_hover"])
            
            self.footer_frame.configure(bg=self.colors["background"])
            self.status_bar.configure(bg=self.colors["background"], fg=self.colors["text"])
            self.help_button.configure(bg=self.colors["secondary_button"], fg=self.colors["text"],
                                     activebackground=self.colors["secondary_hover"])
            self.dark_mode_check.configure(bg=self.colors["background"], fg=self.colors["text"],
                                         selectcolor=self.colors["background"],
                                         activebackground=self.colors["background"])

    def create_tooltips(self):
        """Create tooltips for widgets"""
        self.create_tooltip(self.category_menu_button, "Select a game category")
        self.create_tooltip(self.option_menu_button, "Select a specific game variant")
        self.create_tooltip(self.run_button, "Launch the selected game variant")
        self.create_tooltip(self.help_button, "Show help information")
        self.create_tooltip(self.dark_mode_check, "Toggle between light and dark mode")

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            frame = tk.Frame(self.tooltip, bg=self.colors["background"], bd=1, relief=tk.SOLID)
            frame.pack(fill=tk.BOTH, expand=True)
            
            label = tk.Label(frame, text=text, 
                           bg=self.colors["background"], fg=self.colors["text"],
                           font=("Helvetica", 9), padx=5, pady=3)
            label.pack()
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMenuApp(root)
    root.mainloop()

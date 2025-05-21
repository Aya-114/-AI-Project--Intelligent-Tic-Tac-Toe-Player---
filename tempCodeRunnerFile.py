import tkinter as tk
from tkinter import messagebox
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

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Variants Menu")

        self.label = tk.Label(root, text="Select a Category", font=("Arial", 16))
        self.label.pack(pady=10)

        self.category_var = tk.StringVar(value="Center Control")
        self.category_menu = tk.OptionMenu(root, self.category_var, *menu_structure.keys(), command=self.update_options)
        self.category_menu.pack(pady=5)

        self.option_var = tk.StringVar()
        self.option_menu = tk.OptionMenu(root, self.option_var, "")
        self.option_menu.pack(pady=5)

        self.run_button = tk.Button(root, text="Run Selected Script", command=self.run_script)
        self.run_button.pack(pady=15)

        self.update_options(self.category_var.get())

    def update_options(self, category):
        options = list(menu_structure[category].keys())
        self.option_var.set(options[0])
        menu = self.option_menu["menu"]
        menu.delete(0, "end")
        for option in options:
            menu.add_command(label=option, command=lambda opt=option: self.option_var.set(opt))

    def run_script(self):
        category = self.category_var.get()
        option = self.option_var.get()
        script_name = menu_structure[category][option]

        if not os.path.isfile(script_name):
            messagebox.showerror("Error", f"Script '{script_name}' not found.")
            return

        # Run the script in a separate process
        try:
            # Use python executable compatible with current environment
            subprocess.Popen([sys.executable, script_name])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

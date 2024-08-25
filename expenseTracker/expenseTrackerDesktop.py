import tkinter as tk
from tkinter import messagebox

# Create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Expense Tracker")
    
    # Window resizing
    window.geometry("300x200") # This is where the window size is set
    window.resizable(True,True) # This will allow the window to be resized

    # Create a button to add expenses using grid layout
    add_button = tk.Button(window, text="Add Expense", width=20, height=2, command=show_add_expense_window)

    # Use grid to place the button and center it (3x3 grid for flexibility)
    add_button.grid(row=2, column=2, padx=10, pady=10)

    # Configure the grid system
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(3, weight=1)

    window.mainloop()

# Define the function to show a new window for adding expenses
def show_add_expense_window():
    add_window = tk.Toplevel() # This will create a new window
    add_window.title("Add Expense")
    add_window.geometry("300x200")

# Start the application
create_main_window()
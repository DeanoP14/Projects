import tkinter as tk
from tkinter import messagebox

# Create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Expense Tracker")
    window.geometry("300x200") # This is where the window size is set

    # Create a button to add expenses
    add_button = tk.Button(window, text="Add Expense", command=show_add_expense_window)
    add_button.pack(pady=20) # This places the button within the window

    window.mainloop()

# Define the function to show a new window for adding expenses
def show_add_expense_window():
    add_window = tk.Toplevel() # This will create a new window
    add_window.title("Add Expense")
    add_window.geometry("300x200")

    # Add widgets like labels and entry fields in the future
    messagebox.showinfo("Info", "This is where you'll add expenses.")

# Start the application
create_main_window()
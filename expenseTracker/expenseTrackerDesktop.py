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
    add_button.grid(row=0, column=0, padx=10, pady=10)

    # Configure the grid system
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)

    window.mainloop()

# Define the function to show a new window for adding expenses
def show_add_expense_window():
    add_window = tk.Toplevel() # This will create a new window
    add_window.title("Add Expense")
    add_window.geometry("400x200")

    # Labels and entry fields
    tk.Label(add_window, text="Amount:").grid(row=0,column=0,padx=10,pady=10,sticky="e")
    amount_entry = tk.Entry(add_window)
    amount_entry.grid(row=0,column=1,padx=10,pady=10)

    tk.Label(add_window, text="Category:").grid(row=1,column=0,padx=10,pady=10,sticky="e")
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1,column=1,padx=10,pady=10)

    tk.Label(add_window, text="Message:").grid(row=2,column=0,padx=10,pady=10,sticky="e")
    message_entry = tk.Entry(add_window)
    message_entry.grid(row=2,column=1,padx=10,pady=10)

    # Submit Button
    submit_button = tk.Button(add_window, text="Submit", command=lambda: submit_expense(amount_entry, category_entry, message_entry, add_window))
    submit_button.grid(row=3,column=0,columnspan=2,pady=10)

def submit_expense(amount_entry, category_entry, message_entry, window):
    amount = amount_entry.get()
    category = category_entry.get()
    message = message_entry.get()

    # For proof of concept going to print screen to show all functions working
    print(f"Amount: {amount}, Category: {category}, Message: {message}")

    # Show message box
    messagebox.showinfo("Expense Submitted", f"Amount: {amount}\nCategory: {category}\nMessage: {message}")

    # Close the add expense window
    window.destroy()

# Start the application
create_main_window()
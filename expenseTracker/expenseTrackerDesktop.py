import sqlite3 
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Create a function to initialise and create the database
def init():
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount DECIMAL NOT NULL,
            category TEXT NOT NULL,
            message TEXT,
            date TEXT NOT NULL
        )
        '''
        c.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error initialising database: {e}")
    finally:
        conn.close()

# Create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Expense Tracker")
    
    # Window resizing
    window.geometry("600x400") # This is where the window size is set
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
    add_window.geometry("500x300")

    # Labels and entry fields
    tk.Label(add_window, text="Amount:").grid(row=0,column=0,padx=10,pady=10)
    amount_entry = tk.Entry(add_window)
    amount_entry.grid(row=0,column=1,padx=10,pady=10)

    # Category Label
    tk.Label(add_window, text="Category:").grid(row=1,column=0,padx=10,pady=10)
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1,column=1,padx=10,pady=10)

    # Message label
    tk.Label(add_window, text="Message:").grid(row=2,column=0,padx=10,pady=10)
    message_entry = tk.Entry(add_window)
    message_entry.grid(row=2,column=1,padx=10,pady=10)

    # Save Button to trigger the log function
    save_button = tk.Button(add_window, text="Save Expense", command=lambda: save_expense(amount_entry.get(), category_entry.get(), message_entry.get()))
    save_button.grid(row=3,columnspan=2,pady=20)

def save_expense(amount, category, message):
    try:
        # Convert amount to a float for validation
        amount = float(amount)

        # Get the current date and log the expense
        date = datetime.now().strftime("%Y-%m-%d")
        data = (amount, category, message, date)

        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = 'INSERT INTO expenses (amount, category, message, date) VALUES (?, ?, ?, ?)'
        c.execute(sql, data)
        conn.commit()
        messagebox.showinfo("Success", "Expense added successfully.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid number for amount.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error logging expense: {e}")
    finally:
        conn.close

# Start the application
create_main_window()
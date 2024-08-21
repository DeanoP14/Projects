import sqlite3
from datetime import datetime

# Initialise a new database if it does not exist, to store the expenses.
def init():
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount DECIMAL,
            category TEXT,
            message TEXT,
            date TEXT
            )
        '''
        c.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# Funtion that logs the expenses to the database. 
def log(amount, category, message=""):
    try:
        date = datetime.now().strftime("%Ywat i wo-%m-%d")
        data = (amount, category, message, date)
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = 'INSERT INTO expenses (amount, category, message, date) VALUES (?,?,?,?)'
        c.execute(sql,data)
        conn.commit()
        print("Expenses added successfully.")
    except sqlite3.Error as e:
        print(f"Error logging expense: {e}")
    finally:
        conn.close()

# Function to remove a selected expense
def remove(expense_id):
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = 'DELETE FROM expenses WHERE id = ?'
        c.execute(sql, (expense_id,))
        if c.rowcount == 0:
            print("No expense found with that ID.")
        else:
            conn.commit()
            print("Expense removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing expense: {e}")
    finally:
        conn.close()

# Funtion to show a list of the expenses and total expense. Can select specific categories.
def view(category=None):
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        if category:
            sql = '''
            SELECT * FROM expenses WHERE category = ?
            '''
            sql2 = '''
            SELECT sum(amount) FROM expenses WHERE category = ?
            '''
            c.execute(sql, (category,))
            results = c.fetchall()
            c.execute(sql2, (category,))
        else:
            sql = '''
            SELECT * FROM expenses
            '''
            sql2 = '''
            SELECT sum(amount) FROM expenses
            '''
            c.execute(sql)
            results = c.fetchall()
            c.execute(sql2)
    
        total_amount = c.fetchone()[0]
        if total_amount is None:
            total_amount = 0
        
        return total_amount, results
    except sqlite3.Error as e:
        print(f"Error viewing expenses: {e}")
        return 0, []
    finally:
        conn.close()

    

# Function to display the menu and handle user input
def menu():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. View All Expenses")
        print("4. View Total Expenses")
        print("5. View Expenses by Category")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                message = input("Enter message (optional): ")
                log(amount, category, message)
                print("Expense added successfully.")
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
        elif choice == '2':
            try:
                expense_id = int(input("Enter the ID of the expense to remove: "))
                remove(expense_id)
                print("Expense removed successfully.")
            except ValueError:
                print("Invalid input for expense ID. Please enter a number.")
        elif choice == '3':
            total, expenses = view()
            print(f"\nTotal Expenses: {total}")
            for expense in expenses:
                print(expense)
        elif choice == '4':
            total, _ = view()
            print(f"\nTotal Expenses: {total}")
        elif choice == '5':
            category = input("Enter category: ")
            total, expenses = view(category)
            print(f"\nTotal {category} Expenses: {total}")
            for expense in expenses:
                print(expense)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    init()
    menu()

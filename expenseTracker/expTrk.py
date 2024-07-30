import sqlite3
from datetime import datetime
import hashlib
import os

# Hashing password function
def hash_password(password, salt):
    return hashlib.sha256(password.encode() + salt.encode()).hexdigest()

# Initialise a new database if it does not exist, to store the expenses.
def init():
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        users = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL)
        '''
        c.execute(users)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# Define the signup process
def signup():
    username = input("Please enter the username you would like to use: ")
    email = input("Please enter your email address: ")
    pwd = input("Please enter your password: ")
    conf_pwd = input("Please confirm your password: ")

    # Salting and hashing of password during signup
    if conf_pwd == pwd:
        salt = os.urandom(16).hex()
        hashed_password = hash_password(conf_pwd, salt)
        conn = sqlite3.connect('budget.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password, salt) VALUES (?,?,?,?)',(username, email, hashed_password, salt))
            conn.commit()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user_id = cursor.fetchone()[0]
            create_user_expense_table(user_id)
            print("You have registered successfully")
        except sqlite3.IntegrityError:
            print("Error you have already registered! Try logging in instead.")
        finally:
            conn.close()
    else:
        print("Your passwords do not match!!")

# Defin function to create new table for each user to store their expenses
def create_user_expense_table(user_id):
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        expense_table = f'''
        CREATE TABLE IF NOT EXISTS user_{user_id}_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            category TEXT,
            message TEXT,
            date TEXT
        )
        '''
        c.execute(expense_table)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating user expense table: {e}")
    finally:
        conn.close()


# Define the login process for this application
def login():
    username = input("Enter your username: ")
    pwd = input("Please enter your password: ")
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, password, salt FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        user_id, stored_password, stored_salt = result
        if stored_password == hash_password(pwd, stored_salt):
            print(f"Welcome back to - MyBudgetApp - {username}.")
            ## Create a pause function before proceding to next step
            menu(user_id)
        else:
            print("Login Failed!! Please try again")
    else:
        print("User not found!")

# Funtion that logs the expenses to the database. 
def log(user_id, amount, category, message=""):
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (amount, category, message, date)
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = f'INSERT INTO user_{user_id}_expenses (amount, category, message, date) VALUES (?,?,?,?)'
        c.execute(sql,data)
        conn.commit()
        print("Expenses added successfully.")
    except sqlite3.Error as e:
        print(f"Error logging expense: {e}")
    finally:
        conn.close()

# Function to remove a selected expense
def remove(user_id, expense_id):
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        sql = f'DELETE FROM user_{user_id}_expenses WHERE id = ?'
        c.execute(sql, (expense_id, user_id))
        if c.rowcount == 0:
            print("No expense found with that ID for this user.")
        else:
            conn.commit()
            print("Expense removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing expense: {e}")
    finally:
        conn.close()

# Funtion to show a list of the expenses and total expense. Can select specific categories.
def view(user_id, category=None):
    try:
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        if category:
            sql = f'''
            SELECT * FROM user_{user_id}_expenses WHERE category = ?
            '''
            sql2 = f'''
            SELECT sum(amount) FROM user_{user_id}_expenses WHERE category = ?
            '''
            c.execute(sql, (category,))
            results = c.fetchall()
            c.execute(sql2, (category,))
        else:
            sql = f'''
            SELECT * FROM user_{user_id}_expenses 
            '''
            sql2 = f'''
            SELECT sum(amount) FROM user_{user_id}_expenses
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
def menu(user_id):
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
                amount = int(input("Enter amount: "))
                category = input("Enter category: ")
                message = input("Enter message (optional): ")
                log(user_id, amount, category, message)
                print("Expense added successfully.")
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
        elif choice == '2':
            try:
                expense_id = int(input("Enter the ID of the expense to remove: "))
                remove(user_id, expense_id)
                print("Expense removed successfully.")
            except ValueError:
                print("Invalid input for expense ID. Please enter a number.")
        elif choice == '3':
            total, expenses = view(user_id)
            print(f"\nTotal Expenses: {total}")
            for expense in expenses:
                print(expense)
        elif choice == '4':
            total, _ = view(user_id)
            print(f"\nTotal Expenses: {total}")
        elif choice == '5':
            category = input("Enter category: ")
            total, expenses = view(user_id, category)
            print(f"\nTotal {category} Expenses: {total}")
            for expense in expenses:
                print(expense)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

# Define application main menu at startup
def main_menu():
    while True:
        print("********** - MyBudgetApp - **********")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        ch = input("Please enter your choice: ")

        if ch == "1":
            signup()
        elif ch == "2":
            login()
        elif ch == "3":
            print("Exiting...")
            break
        else:
            print("Wrong choice. Please select the number 1, 2 or 3!!")


if __name__ == "__main__":
    init()
    main_menu()
    
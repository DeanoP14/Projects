import sqlite3
from datetime import datetime

# Initialise a new database if it does not exist, to store the expenses.
def init():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    sql = '''
    CREATE TABLE IF NOT EXISTS expenses (
        amount INTEGER,
        category TEXT,
        message TEXT,
        date TEXT
        )
    '''
    c.execute(sql)
    conn.commit()
    conn.close()

# Funtion that logs the expenses to the database. 
def log(amount, category, message=""):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (amount, category, message, date)
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    sql = 'INSERT INTO expenses (amount, category, message, date) VALUES (?,?,?,?)'
    c.execute(sql,data)
    conn.commit()
    conn.close()

# Funtion to show a list of the expenses and total expense. Can select specific categories.
def view(category=None):
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
        c.execute(sql2, (category,))
    else:
        sql = '''
        SELECT * FROM expenses
        '''
        sql2 = '''
        SELECT sum(amount) FROM expenses
        '''
        c.execute(sql)
        c.execute(sql2)
    
    results = c.fetchall()
    total_amount = c.fetchone()
    conn.close()

    return total_amount, results

# Testing the functions
if __name__ == "__main__":
    init()
    log(100, 'Food', 'Groceries')
    log(50, 'Entertainment', 'Movie')
    total, expenses = view()
    print(f"Total Expenses: {total}")
    for expense in expenses:
        print(expense)

    # View a specific category
    total, food_expenses = view('Food')
    print(f"\nTotal Food Expenses: {total}")
    for expense in food_expenses:
        print(expense)
import sqlite3

# Connect to the budget database, or create if it does not exist.

conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

# SQL to create the expenses table
create_table_query = '''
CREATE TABLE IF NOT EXISTS expenses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date TEXT NOT NULL,
	category TEXT NOT NULL,
	amount DECIMAL NOT NULL,
	description TEXT
);
'''

# Execute the table creation query
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'expenses' created successfully!")

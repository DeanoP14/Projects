import ui
import sqlite3

# Initialise the database
def init_db():
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
		print(f"Error initializing database: {e}")
	finally:
		conn.close

# Create the main window view for the application
class MainView(ui.View):
	def __init__(self):
		super().__init__()
		self.background_color = 'white'
		
		# Create a label for the title
		self.title_label = ui.Label(text="Expense Tracker", alignment=ui.ALIGN_CENTER)
		self.title_label.font = ('<system-bold>', 30)
		self.title_label.text_color = '#333333'
		self.add_subview(self.title_label)
		
		# Create a textfield for the amount
		self.amount_field = ui.TextField(placeholder='Enter Amount')
		self.amount_field.keyboard_type = ui.KEYBOARD_DECIMAL_PAD # To accept numbers only
		self.amount_field.border_width = 1
		self.amount_field.border_color = '#cccccc'
		self.amount_field.corner_radius = 5
		self.amount_field.width = 200
		self.amount_field.height = 50
		self.add_subview(self.amount_field)
		
		# Create a textfield for the category
		self.category_field = ui.TextField(placeholder='Enter Category')
		self.category_field.border_width = 1
		self.category_field.border_color = '#cccccc'
		self.category_field.corner_radius = 5
		self.category_field.width = 200
		self.category_field.height = 50
		self.add_subview(self.category_field)
		
		# Create a textfield for optional message
		self.message_field = ui.TextField(placeholder='Enter Message')
		self.message_field.border_width = 1
		self.message_field.border_color = '#cccccc'
		self.message_field.corner_radius = 5
		self.message_field.width = 200
		self.message_field.height = 50
		self.add_subview(self.message_field)

		# Create a button to log an expense
		self.add_button = ui.Button(title="Add Expense")
		self.add_button.width = 200
		self.add_button.height = 50
		self.add_button.font = ('<system-bold>', 18)
		self.add_button.background_color = '#007AFF'
		self.add_button.tint_color = 'white'
		self.add_button.border_width = 2
		self.add_button.border_color = '#005BB5'
		self.add_button.corner_radius = 10
		self.add_button.action = self.add_expense
		self.add_subview(self.add_button)
		
		# Create a view history button
		self.view_button = ui.Button(title="View Expense History")
		self.view_button.width = 200
		self.view_button.height = 50
		self.view_button.font = ('<system-bold>',18)
		self.view_button.background_color = '#34C759'
		self.view_button.tint_color = 'white'
		self.view_button.border_width = 2
		self.view_button.border_color = '#28A745'
		self.view_button.corner_radius = 10
		self.view_button.action = self.view_history
		self.add_subview(self.view_button)
		
	def layout(self):
		self.title_label.size_to_fit()
		self.title_label.center = (self.width * 0.5, 50)
		self.amount_field.center = (self.width * 0.5, 150)
		self.category_field.center = (self.width * 0.5, 220)
		self.message_field.center = (self.width * 0.5, 290)
		self.add_button.center = (self.width * 0.5, 370)
		self.view_button.center = (self.width * 0.5, 450)

	def add_expense(self, sender):
		# Capture the input from the amount field
		amount = self.amount_field.text
		category = self.category_field.text
		message = self.message_field.text or "(No Message)"
		# Validate inputs
		if not amount or not category:
			print("Please enter an amount and select a category.")
			return
		
		try:
			amount = float(amount)
		except ValueError:
			print("Please enter a valid number for the amount.")
			return 
		
		# If validation is passed, store the expense in the database
		self.save_expense(amount, category, message)
		
	def save_expense(self, amount, category, message):
		try:
			conn = sqlite3.connect('budget.db')
			c = conn.cursor()
			sql = '''
			INSERT INTO expenses (amount, category, message, date) VALUES (?, ?, ?, DATE('now'))
			'''
			c.execute(sql, (amount, category, message))
			conn.commit()
			print('Expense logged successfully!')
		except sqlite3.Error as e:
			print(f"Error saving expense: {e}")
		finally:
			conn.close()
			
	def view_history(self, sender):
		try:
			conn = sqlite3.connect('budget.db')
			c = conn.cursor()
			sql = 'SELECT * FROM expenses ORDER BY date DESC'
			c.execute(sql)
			expenses = c.fetchall()
			
			# Create new view for view expenses history
			history_view = ui.View()
			history_view.background_color = 'white'
			
			# Create a textview to display the expense history
			history_text = ui.TextView()
			history_text.editable = False 
			history_text.font = ('<system>', 16)
			
			# Format and display expenses
			history_content = ""
			for expense in expenses:
				history_content += f"ID: {expense[0]} | Amount: ${expense[1]} | Category: {expense[2]} | Message: {expense[3]} | Date: {expense[4]}\n\n"
			
			history_text.text = history_content
			history_text.frame = (0, 0, history_view.width, history_view.height)
			history_text.flex = 'WH'
			
			history_view.add_subview(history_text)
			history_view.present('fullscreen')
			
		except sqlite3.Error as e:
			print('Error fetching expense history: {e}')
			
		finally:
			conn.close()
				
	def will_close(self):
		print("MainView is closing")
		
# Initialize the database when the app starts
init_db()

# Create and present the main view
main_view = MainView()
main_view.present('fullscreen')

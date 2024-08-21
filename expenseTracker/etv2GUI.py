import ui
import sqlite3

# Initialise the database
def init_db():
	try:
		conn = sqlite3.connect('budget.db')
		c = conn.cursor()
		sql = '''
		CREATE TABLE IS NOT EXISTS expenses (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			amount DECIMAL NOT NULL,
			category TEXT NOT NULL,
			message TEXT NOT NULL,
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
		self.name = "Expense Tracker"
		
	def will_close(self):
		print("MainView is closing")
		
# Initialize the database when the app starts
init_db()

# Create and present the main view
main_view = MainView()
main_view.present('fullscreen')

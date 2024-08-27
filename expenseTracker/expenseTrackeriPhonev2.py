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
		self.title_label = ui.Label(text="Expense Tracker", aligment=ui.ALIGN_CENTER)
		self.title_label.font = ('<system-bold>', 30)
		self.title_label.text_color = '#333333'
		self.add_subview(self.title_label)

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

	def layout(self):
		self.title_label.size_to_fit()
		self.title_label.center = (self.width * 0.5, 50)
		self.add_button.center = (self.width * 0.5, 150)

	def add_expense(self, sender):
		print("Add expense button pressed")
		
	def will_close(self):
		print("MainView is closing")
		
# Initialize the database when the app starts
init_db()

# Create and present the main view
main_view = MainView()
main_view.present('fullscreen')

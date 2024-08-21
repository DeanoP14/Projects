import ui
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO

def get_expense_data(month):
	conn = sqlite3.connect('budget.db')
	cursor = conn.cursor()
	query = '''
	SELECT category, SUM(amount)
	FROM tablename
	WHERE strftime('%m, date') = ?
	GROUP BY category
	'''
	cursor.execute(query,(month,))
	data = cursor.fetchall()
	conn.close
	return data

def show_menu(sender):
	# Function to show the menu
	menu_view = MenuView()
	nav_view.push_view(menu_view)
	
def show_signup(sender):
	# Function to show the signup function
	signup_view = SignupView()
	nav_view.push_view(signup_view)

def create_pie_chart(data):
	categories, amounts = zip(*data)
	plt.figure(figsize=(4,4))
	plt.pie(amounts, labels=categories,autopct='%1.1f%%', startangle=140)
	plt.axis('equal')# Equal aspect ratio ensures that pie is drawn as a circle.
	# Save the figure to a BytesIO object
	buf = BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)
	plt.close()
	# COnver to ui.Image
	img = ui.Image.from_data(buf.read())
	buf.close()
	return img
		
class MainView(ui.View):
	def __init__(self):
		super().__init__()
		self.background_color = 'white'
		
		# Create a label for the title
		self.title_label = ui.Label(text='Expense Tracking Solutions', alignment=ui.ALIGN_CENTER, font=('<system>', 24), text_color='black')
		self.title_label.frame = (10,10, self.width - 20, 50)
		self.title_label.flex = 'W'
		self.add_subview(self.title_label)
		
		# Create a menu button
		self.menu_button = ui.Button(title='Menu')
		self.menu_button.frame = (10, 70, 100, 50)
		self.menu_button.background_color = 'lightblue'
		self.menu_button.border_width = 2
		self.menu_button.border_color = 'blue'
		self.menu_button.corner_radius = 10
		self.menu_button.tint_color = 'black'
		self.menu_button.flex = ''
		self.menu_button.action = show_menu
		self.add_subview(self.menu_button)
		
		# Create a signup button
		self.signup_button = ui.Button(title='Sign Up')
		self.signup_button.frame = (200, 50, 100, 50)
		self.signup_button.background_color = 'lightblue'
		self.signup_button.border_width = 2
		self.signup_button.border_color = 'blue'
		self.signup_button.corner_radius = 10
		self.signup_button.tint_color = 'black'
		self.signup_button.flex = ''
		self.signup_button.action = show_signup
		self.add_subview(self.signup_button)
		
		# Month selector button for the chart
		self.month_selector = ui.SegmentedControl(segments=['January','February','March','April','May','June','July','August','September','October','November','December'])
		self.month_selector.selected_index = 7
		self.month_selector.frame = (10,130, self.width - 20, 40)
		self.month_selector.flex = 'W'
		self.month_selector.action = self.update_chart
		self.add_subview(self.month_selector)
		
		# Display the chart
		self.chart_image_view = ui.ImageView()
		self.chart_image_view.frame = (10, 180, self.width - 20, self.height - 190)
		self.chart_image_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
		self.chart_image_view.flex = 'WH'
		self.add_subview(self.chart_image_view)
		
		# Initial chart display
		self.update_chart()
		
	def update_chart(self, sender=None):
		month_index = self.month_selector.selected_index + 1
		month_str = f'{month_index:02d}'
		data = get_expense_data(month_str)
		img = create_pie_chart(data)
		self.chart_image_view.image = img
		
class MenuView(ui.View):
	def __init__(self):
		super().__init__()
		self.background_color = 'lightgrey'
		# Create label to indicate that its a menu
		self.label = ui.Label(text='Menu', alignment=ui.ALIGN_CENTER)
		self.label.frame = (self.width * 0.25, self.height * 0.4, self.width * 0.5, 32)
		self.label.flex = 'LRTB'
		self.add_subview(self.label)
		# Create button to close the menu
		self.close_button = ui.Button(title='Close Menu')
		self.close_button.center = (self.width * 0.5, self.height * 0.6)
		self.close_button.flex = 'LRTB'
		self.close_button.action = close_menu
		self.add_subview(self.close_button)
		
	def layout(self):
		# Center the label and button
		self.label.frame = (self.width * 0.25, self.height * 0.4, self.width * 0.5, 32)
		self.close_button.center = (self.width * 0.5, self.height * 0.6)
		
class SignupView(ui.View):
	def __init__(self):
		super().__init__()
		self.background_color = 'orange'
		# Create label to indicate that its a menu
		self.label = ui.Label(text='Signup', alignment=ui.ALIGN_CENTER)
		self.label.frame = (self.width * 0.25, self.height * 0.4, self.width * 0.5, 32)
		self.label.flex = 'LRTB'
		self.add_subview(self.label)
		# Create button to close the menu
		self.close_button = ui.Button(title='Close Menu')
		self.close_button.center = (self.width * 0.5, self.height * 0.6)
		self.close_button.flex = 'LRTB'
		self.close_button.action = close_menu
		self.add_subview(self.close_button)
		
	def layout(self):
		# Center the label and button
		self.label.frame = (self.width * 0.25, self.height * 0.4, self.width * 0.5, 32)
		self.close_button.center = (self.width * 0.5, self.height * 0.6)
		
def close_menu(sender):
    # Function to close the menu
    nav_view.pop_view()
    
# Create the view and navigation view
main_view = MainView()
nav_view = ui.NavigationView(main_view)
nav_view.present('fullscreen')


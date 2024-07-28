import tkinter as tk
from tkinter import ttk,messagebox,simpledialog
import csv
import matplotlib.pyplot as plt

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1300x600")
        self.expenses = []
        self.categories = ["Mortgage/Rent","Food","Transportation","Utilities","Entertainment","Kids","Other"]
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.categories[0])
        self.create_widgets()
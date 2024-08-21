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
        
    def create_widgets(self):
        self.label = tk.label(self, text="Expense Tracker", font=("Helvetica", 20,"bold"))
        self.label.pack(pady=10)
        self.frame_input = tk.Frame(self)
        self.frame_input.pack(pady=10)
        self.expense_label = tk.label(self.frame_input, text="Expense Amount:", font("Helvetica", 12))
        self.expense_label.grid(row=0, column=0, padx=5)
        self.expense_entry = tk.Entry(self.frame_input, font("Helvetica", 12), width=15)
        self.expense_entry.grid()
        
        

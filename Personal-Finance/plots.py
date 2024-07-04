import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class FinancePlots:
    def __init__(self, db):
        self.db = db

    def plot_dashboard(self, frame):
        transactions = self.db.get_transactions()
        
        if not transactions:
            no_data_label = tk.Label(frame, text="No data available.", font=('Helvetica', 16), bg='#ecf0f1')
            no_data_label.pack(pady=20)
            return
        
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        
        self.plot_current_balance(axs[0, 0])
        self.plot_budget_distribution(axs[0, 1])
        self.plot_expense_categories(axs[1, 0])
        self.plot_recent_transactions(axs[1, 1])

        # Adjust layout
        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def plot_current_balance(self, ax):
        balance = self.db.get_balance()
        ax.barh(['Current Balance'], [balance], color='blue')
        ax.set_title('Current Balance')

    def plot_budget_distribution(self, ax):
        transactions = self.db.get_transactions()
        incomes = [t[2] for t in transactions if t[1] == "Income"]
        expenses = [t[2] for t in transactions if t[1] == "Expense"]
        
        if not incomes and not expenses:
            ax.pie([1], labels=['No Data'], autopct='%1.1f%%', startangle=90)
            return
        
        total_income = sum(incomes)
        total_expense = sum(expenses)
        
        ax.pie([total_income, total_expense], labels=['Income', 'Expenses'], autopct='%1.1f%%', startangle=90)
        ax.set_title('Budget Distribution')

    def plot_expense_categories(self, ax):
        transactions = self.db.get_transactions()
        categories = {}
        for t in transactions:
            if t[1] == "Expense":
                categories[t[3]] = categories.get(t[3], 0) + t[2]
        
        if not categories:
            ax.bar(['No Data'], [0], color='red')
            return

        ax.bar(categories.keys(), categories.values(), color='red')
        ax.set_title('Expenses by Category')

    def plot_recent_transactions(self, ax):
        transactions = self.db.get_transactions()
        recent_transactions = transactions[-5:]
        
        labels = [f"{t[4]} ({t[1]})" for t in recent_transactions]
        amounts = [t[2] for t in recent_transactions]
        
        ax.barh(labels, amounts, color='green')
        ax.set_title('Recent Transactions')

import tkinter as tk
from tkinter import ttk
from database import FinanceDatabase
from plots import FinancePlots

class FinanceApp:
    def __init__(self, root):
        self.db = FinanceDatabase()
        self.root = root
        self.root.title("Personal Finance Management System")
        self.root.geometry("1000x600")

        self.create_menu()
        self.create_frames()

        self.show_home()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, bg='#2c3e50')
        self.menu_frame.pack(side='left', fill='y')

        self.home_btn = tk.Button(self.menu_frame, text="Dashboard", command=self.show_home, bg='#34495e', fg='white', pady=20)
        self.home_btn.pack(fill='x')

        self.add_btn = tk.Button(self.menu_frame, text="Add Transaction", command=self.show_add_transaction, bg='#34495e', fg='white', pady=20)
        self.add_btn.pack(fill='x')

        self.view_expenses_btn = tk.Button(self.menu_frame, text="View Expenses", command=self.show_expenses, bg='#34495e', fg='white', pady=20)
        self.view_expenses_btn.pack(fill='x')

    def create_frames(self):
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(side='right', expand=True, fill='both')

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()

        balance = self.db.get_balance()
        total_expenses = sum(t[2] for t in self.db.get_transactions() if t[1] == "Expense")

        # Create top frame for cards
        top_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        top_frame.pack(side='top', fill='x', pady=20, padx=10)

        # Create cards for current balance and total expenses
        balance_card = tk.Label(top_frame, text=f"Current Balance: ${balance:.2f}", font=('Helvetica', 16), bg='#1abc9c', fg='white', padx=20, pady=20)
        balance_card.pack(side='left', padx=10)

        expenses_card = tk.Label(top_frame, text=f"Total Expenses: ${total_expenses:.2f}", font=('Helvetica', 16), bg='#e74c3c', fg='white', padx=20, pady=20)
        expenses_card.pack(side='left', padx=10)

        # Create bottom frame for graphs
        bottom_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        bottom_frame.pack(side='bottom', expand=True, fill='both', pady=20, padx=10)

        # Plot the dashboard graphs
        plotter = FinancePlots(self.db)
        plotter.plot_dashboard(bottom_frame)

    def show_add_transaction(self):
        self.clear_frame()

        type_label = tk.Label(self.main_frame, text="Type (Income/Expense):", font=('Helvetica', 12), bg='#ecf0f1')
        type_label.pack(pady=5)
        type_entry = ttk.Combobox(self.main_frame, values=["Income", "Expense"])
        type_entry.pack(pady=5)

        amount_label = tk.Label(self.main_frame, text="Amount:", font=('Helvetica', 12), bg='#ecf0f1')
        amount_label.pack(pady=5)
        amount_entry = tk.Entry(self.main_frame)
        amount_entry.pack(pady=5)

        category_label = tk.Label(self.main_frame, text="Category:", font=('Helvetica', 12), bg='#ecf0f1')
        category_label.pack(pady=5)
        category_entry = tk.Entry(self.main_frame)
        category_entry.pack(pady=5)

        date_label = tk.Label(self.main_frame, text="Date (YYYY-MM-DD):", font=('Helvetica', 12), bg='#ecf0f1')
        date_label.pack(pady=5)
        date_entry = tk.Entry(self.main_frame)
        date_entry.pack(pady=5)

        description_label = tk.Label(self.main_frame, text="Description (optional):", font=('Helvetica', 12), bg='#ecf0f1')
        description_label.pack(pady=5)
        description_entry = tk.Entry(self.main_frame)
        description_entry.pack(pady=5)

        def save_transaction():
            self.db.add_transaction(type_entry.get(), float(amount_entry.get()), category_entry.get(), date_entry.get(), description_entry.get())
            self.show_home()

        save_btn = tk.Button(self.main_frame, text="Save", command=save_transaction, bg='#2ecc71', fg='white')
        save_btn.pack(pady=20)

    def show_expenses(self):
        self.clear_frame()

        columns = ('id', 'type', 'amount', 'category', 'date', 'description')
        tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')

        # Define headings
        for col in columns:
            tree.heading(col, text=col.capitalize())

        # Center-align all cell values
        style = ttk.Style()
        style.configure("Treeview.Heading", anchor='center')
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview", font=('Helvetica', 10))
        style.configure("Treeview.Cell", anchor='center')

        # Populate rows with data
        for row in self.db.get_transactions():
            tree.insert('', tk.END, values=row)

        # Add scrollbar for the table
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        tree.pack(expand=True, fill='both')


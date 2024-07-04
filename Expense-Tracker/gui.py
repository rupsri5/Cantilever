import tkinter as tk
from tkinter import messagebox, ttk
from database import connect_db, add_expense, fetch_expenses, delete_expense, update_expense, fetch_expenses_by_date
from analysis import plot_pie_chart
from datetime import datetime

def submit_expense():
    amount = float(amount_entry.get())
    category = category_entry.get()
    date = date_entry.get()
    description = description_entry.get()

    conn = connect_db()
    add_expense(conn, amount, category, date, description)
    conn.close()

    refresh_expense_list()
    clear_entries()
    messagebox.showinfo("Expense Tracker", "Expense Added Successfully")

def delete_selected_expense():
    selected_item = expense_tree.selection()
    if selected_item:
        expense_id = expense_tree.item(selected_item)['values'][0]
        conn = connect_db()
        delete_expense(conn, expense_id)
        conn.close()
        refresh_expense_list()
        messagebox.showinfo("Expense Tracker", "Expense Deleted Successfully")

def update_selected_expense():
    selected_item = expense_tree.selection()
    if selected_item:
        expense_id = expense_tree.item(selected_item)['values'][0]
        amount = float(amount_entry.get())
        category = category_entry.get()
        date = date_entry.get()
        description = description_entry.get()

        conn = connect_db()
        update_expense(conn, expense_id, amount, category, date, description)
        conn.close()
        refresh_expense_list()
        clear_entries()
        messagebox.showinfo("Expense Tracker", "Expense Updated Successfully")

def load_selected_expense(event):
    selected_item = expense_tree.selection()
    if selected_item:
        expense_id, amount, category, date, description = expense_tree.item(selected_item)['values']
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, amount)
        category_entry.delete(0, tk.END)
        category_entry.insert(0, category)
        date_entry.delete(0, tk.END)
        date_entry.insert(0, date)
        description_entry.delete(0, tk.END)
        description_entry.insert(0, description)

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def refresh_expense_list():
    for item in expense_tree.get_children():
        expense_tree.delete(item)
    
    conn = connect_db()
    for row in fetch_expenses(conn):
        expense_tree.insert('', tk.END, values=row)
    conn.close()

def show_expenses_by_date():
    date = date_filter_entry.get()
    if not date:
        messagebox.showwarning("Expense Tracker", "Please enter a date to filter by.")
        return
    
    for item in expense_tree.get_children():
        expense_tree.delete(item)
    
    conn = connect_db()
    expenses = fetch_expenses_by_date(conn, date)
    conn.close()
    
    for expense in expenses:
        expense_tree.insert('', tk.END, values=expense)

def analyze_expenses():
    plot_pie_chart()

# Initialize main application window
app = tk.Tk()
app.title("Expense Tracker")

# Input fields for adding/editing expenses
tk.Label(app, text="Amount").grid(row=0, column=0)
tk.Label(app, text="Category").grid(row=1, column=0)
tk.Label(app, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
tk.Label(app, text="Description").grid(row=3, column=0)

amount_entry = tk.Entry(app)
category_entry = tk.Entry(app)
date_entry = tk.Entry(app)
description_entry = tk.Entry(app)

amount_entry.grid(row=0, column=1)
category_entry.grid(row=1, column=1)
date_entry.grid(row=2, column=1)
description_entry.grid(row=3, column=1)

# Buttons for CRUD operations
tk.Button(app, text="Add Expense", command=submit_expense).grid(row=4, column=0)
tk.Button(app, text="Update Expense", command=update_selected_expense).grid(row=4, column=1)
tk.Button(app, text="Delete Expense", command=delete_selected_expense).grid(row=4, column=2)
tk.Button(app, text="Clear", command=clear_entries).grid(row=4, column=3)

# Expense list frame
expense_frame = tk.LabelFrame(app, text="All Expenses")
expense_frame.grid(row=5, column=0, columnspan=4, pady=10)

# Expense list (tree view)
columns = ("ID", "Amount", "Category", "Date", "Description")
expense_tree = ttk.Treeview(expense_frame, columns=columns, show='headings')

for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100)

expense_tree.bind('<<TreeviewSelect>>', load_selected_expense)
expense_tree.pack(fill=tk.BOTH, expand=True)

# Filter by date
tk.Label(app, text="Filter by Date (YYYY-MM-DD)").grid(row=6, column=0)
date_filter_entry = tk.Entry(app)
date_filter_entry.grid(row=6, column=1)
tk.Button(app, text="Show Expenses", command=show_expenses_by_date).grid(row=6, column=2)

# Analyze expenses
tk.Button(app, text="Analyze Expenses", command=analyze_expenses).grid(row=7, column=0, columnspan=4)

# Refresh the expense list when the app starts
refresh_expense_list()

app.mainloop()

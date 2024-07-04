import matplotlib.pyplot as plt
from database import connect_db, fetch_expenses
import pandas as pd

def plot_pie_chart():
    conn = connect_db()
    expenses = fetch_expenses(conn)
    conn.close()

    df = pd.DataFrame(expenses, columns=['ID', 'Amount', 'Category', 'Date', 'Description'])
    category_group = df.groupby('Category')['Amount'].sum()

    # Plotting pie chart
    category_group.plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Expenses by Category')
    plt.ylabel('')  # Hide the 'Amount' label
    plt.show()

if __name__ == '__main__':
    plot_pie_chart()

import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('expenses.db')

def create_table(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL NOT NULL,
                            category TEXT NOT NULL,
                            date TEXT NOT NULL,
                            description TEXT
                        );''')

def add_expense(conn, amount, category, date, description):
    with conn:
        conn.execute('''INSERT INTO expenses (amount, category, date, description) 
                        VALUES (?, ?, ?, ?)''', (amount, category, date, description))

def update_expense(conn, id, amount, category, date, description):
    with conn:
        conn.execute('''UPDATE expenses SET amount=?, category=?, date=?, description=?
                        WHERE id=?''', (amount, category, date, description, id))

def delete_expense(conn, id):
    with conn:
        conn.execute('DELETE FROM expenses WHERE id=?', (id,))

def fetch_expenses(conn):
    with conn:
        return conn.execute('SELECT * FROM expenses').fetchall()

def fetch_expenses_by_date(conn, date):
    with conn:
        return conn.execute('SELECT * FROM expenses WHERE date=?', (date,)).fetchall()

# Initialize database
if __name__ == '__main__':
    conn = connect_db()
    create_table(conn)
    conn.close()

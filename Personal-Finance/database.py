import sqlite3

class FinanceDatabase:
    def __init__(self, db_name='finance.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    type TEXT NOT NULL,
                                    amount REAL NOT NULL,
                                    category TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    description TEXT
                                )''')

    def add_transaction(self, type, amount, category, date, description=None):
        with self.conn:
            self.conn.execute('''INSERT INTO transactions (type, amount, category, date, description) 
                                 VALUES (?, ?, ?, ?, ?)''', (type, amount, category, date, description))

    def get_transactions(self):
        with self.conn:
            return self.conn.execute('SELECT * FROM transactions').fetchall()

    def get_balance(self):
        with self.conn:
            income = self.conn.execute('SELECT SUM(amount) FROM transactions WHERE type="Income"').fetchone()[0] or 0
            expenses = self.conn.execute('SELECT SUM(amount) FROM transactions WHERE type="Expense"').fetchone()[0] or 0
            return income - expenses

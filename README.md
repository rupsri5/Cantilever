# Python Projects: Contact Book, Personal Finance, and Expense Tracker

Welcome to our Python Projects repository, featuring three distinct applications designed to enhance productivity and simplify everyday tasks. Explore each project below to see how they can streamline your workflow:

- **Contact Book:** Manage your contacts effortlessly with features for adding, editing, and organizing contact information.

- **Personal Finance:** Track income, expenses, and visualize financial data to make informed decisions about your finances.

- **Expense Tracker:** Monitor and analyze your spending habits through an intuitive interface, helping you manage your budget effectively.

# Getting Started

To run these locally, follow the steps:
#### 1. Clone the Repository:
```powershell
git clone git@github.com:rupsri5/Cantilever.git
```

#### 2. Create a Python environment (Optional):
Navigate to the Directory and Create Python environment
```powershell
python -m venv venv
```

Activate environment in bash
```bash
source venv/bin/Activate
```
or in powershell
```powershell
.\venv\scripts\Activate
```

#### 3. Install Dependencies:
```powershell
pip install -r requirements.txt
```

#### 4. To run each project individually:

Navigate to project directory and run command:
```powershell
python main.py
```

# 1. Contact Book
The Contact Book Application is a simple Python GUI program built using Tkinter and SQLite for managing contacts. It allows users to add, view, edit, delete, search, and display contacts stored in a relational database.

## Features
1. **Add Contact:** Add new contacts with a name and phone number.
2. **View Contact:** View details of a selected contact.
3. **Edit Contact:** Modify the name or phone number of an existing contact.
4. **Delete Contact:** Remove a contact from the database.
5. **Search Contacts:** Search for contacts by name.
6. **Sorting:** Contacts are displayed in alphabetical order.
7. **Persistent Storage:** Contacts are stored in an SQLite database (contacts.db).

## Technologies Used
- Python 3: Programming language used for the application.
- Tkinter: Python's de-facto standard GUI (Graphical User Interface) package.
- SQLite: Lightweight relational database management system bundled with Python.

# 2. Personal Finance

The Personal Finance Management System is a Python-based application designed to help you manage your personal finances. Track your income, expenses, and visualize financial data effortlessly using SQLite for data storage and Matplotlib for graphical representation.

## Features
1. **Dashboard:** View your current balance, total expenses, and graphical representations of your financial status.
2. **Add Transactions:** Add new income or expense transactions with details such as amount, category, date, and optional description.
3. **View Expenses:** Display a table of all stored expenses with options for filtering and sorting.

## Technologies Used
- Python 3: The core programming language used for the application.
- Tkinter: For creating the graphical user interface.
- SQLite: Used to store financial data in a lightweight, relational database.
- Matplotlib: For creating visual representations of financial data.

# 3. Expense Tracker

The Expense Tracker Application is a comprehensive tool designed to help you manage and analyze your expenses. With an intuitive graphical interface, you can record, categorize, and visualize your spending habits, all stored securely in an SQLite database.

## Features
1. **Expense Management:** Add, edit, and delete expenses with details like amount, category, date, and description.
2. **Expense Display:** View a list of all recorded expenses.
3. **Date Filtering:** Filter expenses by specific dates or date ranges.
4. **Data Analysis:** Generate pie charts to visualize expenses by category.
5. **Database Storage:** Securely store all expense records in an SQLite database.

## Technologies Used
- Python 3: The main programming language used for development.
- Tkinter: Used for the graphical user interface.
- SQLite: For storing and managing expense records.
- Matplotlib: For creating pie charts and visual data representations.
- Pandas: For efficient data management and analysis.
- Datetime: To handle and manipulate date information.

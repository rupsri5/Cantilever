from database import connect_db, create_table
from gui import app

def main():
    conn = connect_db()
    create_table(conn)
    conn.close()

    app.mainloop()

if __name__ == '__main__':
    main()

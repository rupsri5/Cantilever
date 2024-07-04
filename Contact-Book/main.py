import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("400x500")
        self.root.config(bg="#f0f0f0")
        
        #connection with sqlite database
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()

        self.create_table()

        # self.load_contacts()

        self.create_widgets()

    def create_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Frame for the search bar and contact list
        self.search_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.search_frame.pack(pady=10)

        # Search bar
        self.search_label = tk.Label(self.search_frame, text="Search:", font=("Arial", 12), bg="#f0f0f0")
        self.search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(self.search_frame, width=30, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_contacts, font=("Arial", 12), bg="#2196F3", fg="white")
        self.search_button.pack(side=tk.LEFT, padx=5)

        #frame of contact list
        self.contact_list_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.contact_list_frame.pack(pady=20)

        # Label for Contact List
        self.title_label = tk.Label(self.contact_list_frame, text="Contacts", font=("Arial", 14), bg="#f0f0f0")
        self.title_label.pack()

        #listbox to display contact
        self.contact_listbox = tk.Listbox(self.contact_list_frame, width=50, height=10, font=("Arial", 10))
        self.contact_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        #scrollbar for listbox
        self.scrollbar = tk.Scrollbar(self.contact_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contact_listbox.yview)

        # Frame for action buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        #buttons for action
        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(self.button_frame, text="View Contact", command=self.view_contacts, font=("Arial", 12), bg="#2196F3", fg="white")
        self.view_button.pack(pady=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Contact", command=self.edit_contact, font=("Arial", 12), bg="#FFC107", fg="white")
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact, font=("Arial", 12), bg="#F44336", fg="white")
        self.delete_button.pack(pady=5)

        self.load_contacts_into_listbox()

    def add_contact(self):
        dialog = ContactDialog(self.root, "Add Contact")
        self.root.wait_window(dialog.top)

        if dialog.result:
            name, phone = dialog.result
            self.cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            self.conn.commit()
            self.load_contacts_into_listbox()

    def view_contacts(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            self.cursor.execute("SELECT phone FROM contacts WHERE name=?", (selected_contact,))
            phone = self.cursor.fetchone()[0]
            messagebox.showinfo("Contact Details", f"Name: {selected_contact}\nPhone: {phone}")
        except tk.TclError:
            messagebox.showerror("Error", "No contact selected")

    def edit_contact(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            new_name = simpledialog.askstring("Edit Contact", "Enter new name:", initialvalue=selected_contact)
            self.cursor.execute("SELECT phone FROM contacts WHERE name=?", (selected_contact,))
            current_phone = self.cursor.fetchone()[0]
            new_phone = simpledialog.askstring("Edit Contact", "Enter new phone number:", initialvalue=current_phone)
            if new_name and new_phone:
                self.cursor.execute("UPDATE contacts SET name=?, phone=? WHERE name=?", (new_name, new_phone, selected_contact))
                self.conn.commit()
                self.load_contacts_into_listbox
        except tk.TclError:
            messagebox.showerror("Error", "No contact selected")
    
    def delete_contact(self):
        try:
            selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
            self.cursor.execute("DELETE FROM contacts WHERE name=?", (selected_contact,))
            self.conn.commit()
            self.contact_listbox.delete(tk.ANCHOR)
        except tk.TclError:
            messagebox.showerror("Error", "No contact selected")

    def load_contacts_into_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name FROM contacts ORDER BY name", ())
        for row in self.cursor.fetchall():
            self.contact_listbox.insert(tk.END, row[0])

    def search_contacts(self):
        query = self.search_entry.get().lower()
        self.contact_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name FROM contacts WHERE lower(name) LIKE ? ORDER BY name", ('%' + query + '%',))
        for row in self.cursor.fetchall():
            self.contact_listbox.insert(tk.END, row[0])

    def close(self):
        self.conn.close()
        self.root.destroy()

class ContactDialog:
    def __init__(self, parent, title, name='', phone=''):
        top = self.top = tk.Toplevel(parent)
        top.title(title)
        top.geometry("300x200")
        top.config(bg="#f0f0f0")


        self.name = tk.StringVar(value=name)
        self.phone = tk.StringVar(value=phone)

        # Name Label and Entry
        tk.Label(top, text="Name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.name_entry = tk.Entry(top, textvariable=self.name, font=("Arial", 12), width=25)
        self.name_entry.pack()

        # Phone Label and Entry
        tk.Label(top, text="Phone:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.phone_entry = tk.Entry(top, textvariable=self.phone, font=("Arial", 12), width=25)
        self.phone_entry.pack()

        # OK and Cancel Buttons
        tk.Button(top, text="OK", command=self.ok, font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(top, text="Cancel", command=self.cancel, font=("Arial", 12), bg="#F44336", fg="white").pack(side=tk.RIGHT, padx=20, pady=20)

        self.result = None

    def ok(self):
        name = self.name.get().strip()
        phone = self.phone.get().strip()
        if name and phone:
            self.result = (name, phone)
            self.top.destroy()
        else:
            messagebox.showwarning("Input Error", "Both fields are required.")

    def cancel(self):
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import os
from Modules.AddCustomer import AddCustomer

database_location = os.getcwd() + "\\Database\\people.db"

if not (os.path.isfile(database_location)):
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE customer (
                f_name TEXT,
                l_name TEXT,
                phone INTEGER,
                street TEXT,
                city TEXT,
                state TEXT,
                zipcode INT,
                email TEXT,
                invoice_location TEXT
                )""")
    conn.commit()
    conn.close()


def main():
    root = Tk()
    screen_width = str(root.winfo_screenwidth())
    screen_height = str(root.winfo_screenheight())
    root.geometry(screen_width + "x" + screen_height)
    root.resizable(height=True, width=True)

    tabs = ttk.Notebook(root)
    tabs.grid(row=0, column=0)

    add_customer_menu = AddCustomer(root)
    tabs.add(add_customer_menu.get_frame(), text="Add Customer")

    root.mainloop()


if __name__ == "__main__":
    main()

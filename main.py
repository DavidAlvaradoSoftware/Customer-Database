from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import os
from Modules.AddCustomer import AddCustomer
from Modules.ExistingCustomer import ExistingCustomer

database_location = os.getcwd() + "\\Database\\people.db"


def main():
    create_directories()
    root = Tk()
    screen_width = str(root.winfo_screenwidth())
    screen_height = str(root.winfo_screenheight())
    root.geometry(screen_width + "x" + screen_height)
    root.resizable(height=True, width=True)

    tabs = ttk.Notebook(root)
    tabs.grid(row=0, column=0)

    add_customer_menu = AddCustomer(root, database_location)
    tabs.add(add_customer_menu.get_frame(), text="Add Customer")

    add_existing_customer_menu = ExistingCustomer(root, database_location)
    tabs.add(add_existing_customer_menu.get_frame(), text="Existing Customer")

    root.mainloop()


def create_directories():
    try:
        os.makedirs(os.getcwd() + "\\Customers")
        os.makedirs(os.getcwd() + "\\Old Customers")
        os.makedirs(os.getcwd() + "\\Database")

        if not (os.path.isfile(database_location)):
            connection = sqlite3.connect(database_location)
            cursor = connection.cursor()

            cursor.execute("""CREATE TABLE customer (
                        f_name TEXT,
                        l_name TEXT,
                        phone TEXT,
                        street TEXT,
                        city TEXT,
                        state TEXT,
                        zipcode TEXT,
                        email TEXT,
                        invoice_location TEXT
                        )""")
            connection.commit()
            connection.close()


    except Exception as e:
        # Do nothing
        print(e)
        pass
    else:
        if not (os.path.isfile(database_location)):
            connection = sqlite3.connect(database_location)
            cursor = connection.cursor()

            cursor.execute("""CREATE TABLE customer (
                        f_name TEXT,
                        l_name TEXT,
                        phone TEXT,
                        street TEXT,
                        city TEXT,
                        state TEXT,
                        zipcode TEXT,
                        email TEXT,
                        invoice_location TEXT
                        )""")
            connection.commit()
            connection.close()


if __name__ == "__main__":
    main()

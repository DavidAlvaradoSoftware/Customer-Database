# Working on adding customer to database method
from tkinter import *
from Modules.ValidCredentialChecker import CheckCredentials
from tkinter import ttk, messagebox
import os
import sqlite3


class AddCustomer:
    def __init__(self, root, database_location):

        self.root = root
        self.database_location = database_location
        self.add_customer_tab_frame = Frame(root, width=300, height=300)

        # Add customer title
        self.customer_tab_label = Label(self.add_customer_tab_frame, text="Add Customer", font=("Arial", 25))
        self.customer_tab_label.grid(row=1, column=0)

        # Customer information labels and Textboxes
        self.customer_credentials_labels = [None] * 8
        self.customer_credential_label_initialization()

        self.customer_credentials_textboxes = [None] * 8
        self.customer_credentials_textboxes_initialization()

        # Buttons
        self.add_customer_button = Button(self.add_customer_tab_frame, text="Add Customer",
                                          bg='#5FC663', height=1, width=50,
                                          command=self.add_customer_to_database)
        self.add_customer_button.grid(row=11, column=1, columnspan=2, pady=(0, 10))

        self.clear_fields_button = Button(self.add_customer_tab_frame, text="Clear Textboxes",
                                          command=self.clear_textboxes)
        self.clear_fields_button.grid(row=10, column=2, pady=10)

    def customer_credential_label_initialization(self):
        label_list = ["First Name", "Last Name",
                      "Phone Number (0123456789)", "Email",
                      "Street", "City", "State(XY)", "Zip Code(12345)"]

        for label in range(len(label_list)):
            self.customer_credentials_labels[label] = Label(self.add_customer_tab_frame, text=label_list[label],
                                                            font=("Arial", 14))
            self.customer_credentials_labels[label].grid(row=2 + label, column=0, padx=(10, 0), sticky=W)

    def customer_credentials_textboxes_initialization(self):
        for textbox in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[textbox] = Entry(self.add_customer_tab_frame, width=50)
            self.customer_credentials_textboxes[textbox].grid(row=2 + textbox, column=2)

    def add_customer_to_database(self):
        # If the result is True, Then it passed. If it's false, it failed.
        self.disable_text_boxes()
        result = CheckCredentials(self.customer_credentials_textboxes)
        if result is False:
            messagebox.showerror("Unable to add customer", "Unable to add customer.")
            self.enable_text_boxes()
        else:
            self.add_customer_button.configure(state="disabled")
            self.clear_fields_button.configure(state="disabled")

            if not self.does_customer_already_exists():
                customer_folder_location = os.getcwd() + "\\Customers\\" + \
                                           self.customer_credentials_textboxes[1].get() + " " + \
                                           self.customer_credentials_textboxes[2].get()
                try:
                    if not (os.path.isfile(customer_folder_location)):
                        os.makedirs(customer_folder_location)
                except OSError:
                    messagebox.showerror("Creating Customer Folder",
                                         "Error creating customer folder. Check if customer "
                                         "folder already exists")
                    self.clear_textboxes()
                    self.enable_text_boxes()
                    self.add_customer_button.configure(state="normal")
                    self.clear_fields_button.configure(state="normal")
                else:
                    try:
                        connection = sqlite3.connect(self.database_location)
                        cursor = connection.cursor()
                        cursor.execute(
                            "INSERT INTO customer VALUES(:f_name, :l_name, :phone, :street, :city, :state, :zipcode, "
                            ":email, :invoice_location)",
                            {
                                'f_name': self.customer_credentials_textboxes[0].get(),
                                'l_name': self.customer_credentials_textboxes[1].get(),
                                'phone': int(self.customer_credentials_textboxes[2].get()),
                                'street': self.customer_credentials_textboxes[4].get(),
                                'city': self.customer_credentials_textboxes[5].get(),
                                'state': self.customer_credentials_textboxes[6].get(),
                                'zipcode': int(self.customer_credentials_textboxes[7].get()),
                                'email': self.customer_credentials_textboxes[3].get(),
                                'invoice_location': customer_folder_location

                            })
                        connection.commit()
                        cursor.execute("SELECT oid, * FROM customer")
                        print(cursor.fetchall())

                        connection.close()

                        self.enable_text_boxes()
                        self.clear_textboxes()
                        self.add_customer_button.configure(state="normal")
                        self.clear_fields_button.configure(state="normal")
                        messagebox.showinfo(title="Success", message="Customer successfully added")
                    except Exception as error:
                        print('Error when adding customer to database')
                        print(error)
            else:
                messagebox.showerror("Customer already in database",
                                     "A customer with the same phone number is in the database")
                self.enable_text_boxes()
                self.add_customer_button.configure("normal")
                self.clear_fields_button.configure("normal")

    def does_customer_already_exists(self):
        connection = sqlite3.connect(self.database_location)
        cursor = connection.cursor()
        cursor.execute("SELECT * From customer WHERE phone = ?", (self.customer_credentials_textboxes[2].get(),))
        existing_customer = cursor.fetchall()
        connection.close()
        if len(existing_customer) == 0:
            return False
        else:
            return True

    def disable_text_boxes(self):
        for textbox in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[textbox].configure(state="disabled")

    def enable_text_boxes(self):
        for textbox in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[textbox].configure(state="normal")

    def clear_textboxes(self):
        for textbox in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[textbox].delete(0, END)

    def get_frame(self):
        return self.add_customer_tab_frame

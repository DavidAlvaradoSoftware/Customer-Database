from tkinter import *
from tkinter import ttk, messagebox
import os
import sqlite3
import re


class AddCustomer:
    def __init__(self, root):

        self.root = root
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

        self.clear_fields = Button(self.add_customer_tab_frame, text="Clear Textboxes", command=self.clear_texboxes())
        self.clear_fields.grid(row=10, column=2, pady=10)

    def customer_credential_label_initialization(self):
        label_list = ["First Name", "Last Name", "Phone Number", "Email", "Street", "City", "State", "Zip Code"]
        for label in range(len(label_list)):
            self.customer_credentials_labels[label] = Label(self.add_customer_tab_frame, text=label_list[label],
                                                            font=("Arial", 14))
            self.customer_credentials_labels[label].grid(row=2 + label, column=0, padx=(10, 0), sticky=W)

    def customer_credentials_textboxes_initialization(self):
        for textbox in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[textbox] = Entry(self.add_customer_tab_frame, width=50)
            self.customer_credentials_textboxes[textbox].grid(row=2 + textbox, column=2)

    def add_customer_to_database(self):
        pass

    def clear_texboxes(self):
        pass

    def get_frame(self):
        return self.add_customer_tab_frame

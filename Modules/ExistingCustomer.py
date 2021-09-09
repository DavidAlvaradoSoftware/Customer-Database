import sqlite3
from tkinter import *
from tkinter import messagebox
from Modules.EditCustomer import EditCustomer



class ExistingCustomer:
    def __init__(self, root, database_location):
        self.root = root
        self.database_location = database_location

        self.existing_customer_frame = Frame(self.root, borderwidth=10, relief="solid",
                                             width=self.root.winfo_screenwidth(),
                                             height=self.root.winfo_screenheight())
        self.customer_search_frame = Frame(self.existing_customer_frame, borderwidth=10, relief="solid",
                                           width=int(self.root.winfo_screenwidth() / 2),
                                           height=int(self.root.winfo_screenheight() / 2))
        self.customer_search_frame.grid(row=0, column=0, padx=20)

        #######################     Phone # search frame setup    ##########################
        self.search_for_customer_title = Label(self.customer_search_frame, text="Search For Customer",
                                               font=("Arial", 25))
        self.search_for_customer_title.grid(row=0, column=0, padx=(10, 0), sticky=W)
        self.search_for_phone_label = Label(self.customer_search_frame, text="Phone Number (0123456789)",
                                            font=("Arial", 14))
        self.search_for_phone_label.grid(row=1, column=0, padx=(10, 0), sticky=W)

        self.phone_search_textbox = Entry(self.customer_search_frame, width=50)
        self.phone_search_textbox.grid(row=1, column=1, padx=(0, 10), sticky=W)

        self.search_button = Button(self.customer_search_frame, text="Search",
                                    command=self.search_database_phone_number)
        self.search_button.grid(row=2, column=1)

        ########################    Result Frame    ##############################
        self.customer_result_frame = Frame(self.existing_customer_frame, borderwidth=10, relief="solid",
                                           width=int(self.root.winfo_screenwidth() / 2),
                                           height=int(self.root.winfo_screenheight() / 2))
        self.customer_result_frame.grid(row=0, column=1, padx=20)

        self.results_title = Label(self.customer_result_frame, text="Results", font=("Arial", 25))
        self.results_title.grid(row=0, column=0)
        self.create_customer_credential_labels()

        self.edit_customer_button = Button(self.customer_result_frame, text="Edit", bg='#FFFF33', height=1, width=50,
                                           command=self.edit_customer)
        self.edit_customer_button.grid(row=9, column=1, padx=10, pady=10)

        self.current_customer = None

    def create_customer_credential_labels(self):
        label_list = ["First Name", "Last Name",
                      "Phone Number (0123456789)", "Street",
                      "City", "State(XY)", "Zip Code(12345)", "Email"]

        self.customer_credentials_labels = [[None for x in range(2)] for y in range(len(label_list))]

        # self.customer_credentials_labels[row][column]
        for column in range(2):
            for row in range(len(label_list)):
                if column == 1:
                    self.customer_credentials_labels[row][column] = Label(self.customer_result_frame,
                                                                          text="          ",
                                                                          font=("Arial", 14))
                    self.customer_credentials_labels[row][column].grid(row=1 + row, column=column, padx=(10, 0),
                                                                       sticky=W)
                else:
                    self.customer_credentials_labels[row][column] = Label(self.customer_result_frame,
                                                                          text=label_list[row],
                                                                          font=("Arial", 14))
                    self.customer_credentials_labels[row][column].grid(row=1 + row, column=column, padx=(10, 0),
                                                                       sticky=W)

    def search_database_phone_number(self):
        self.search_button.configure(state="disabled")
        try:
            phone_number = int(self.phone_search_textbox.get())
        except:
            messagebox.showerror("Phone Error", "Cant turn phone number to int")
        else:
            try:
                connection = sqlite3.Connection(self.database_location)

            except:
                messagebox.showerror("Database Connection", "Error connecting to database")
            else:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM customer WHERE phone =:phone_number",
                               {"phone_number": self.phone_search_textbox.get()})
            customer = cursor.fetchone()
            if customer is None:
                messagebox.showerror("Empty results", "No customers were found by that phone number.")
                self.search_button.configure(state="normal")
            else:
                self.display_customer_credentials(customer)

    def display_customer_credentials(self, database_result):
        for credential in range(8):
            self.customer_credentials_labels[credential][1].configure(text=database_result[credential])

        self.search_button.configure(state="normal")

    def edit_customer(self):
        pass

    def get_frame(self):
        return self.existing_customer_frame

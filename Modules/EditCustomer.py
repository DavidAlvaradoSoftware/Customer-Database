# I keep getting error = near "phone": syntax error
import sqlite3
from tkinter import *
from tkinter import messagebox
from Modules.ValidCredentialChecker import CheckCredentials


class EditCustomer:
    def __init__(self, root, database_location, customer):
        self.root = root
        self.database_location = database_location
        self.customer = customer

        self.edit_customer_window_pop_up = Toplevel(self.root)
        self.edit_customer_window_pop_up.geometry("600x400")

        self.edit_customer_title = Label(self.edit_customer_window_pop_up, text="Edit Customer", font=("Arial", 25))
        self.edit_customer_title.grid(row=0, column=0)
        self.create_customer_labels_and_textboxes()

        self.edit_customer_button = Button(self.edit_customer_window_pop_up, text="Update", bg='#FFFF33',
                                           command=self.add_edited_credentials_to_db)
        self.edit_customer_button.grid(row=9, column=1, pady=10)

    def create_customer_labels_and_textboxes(self):
        label_list = ["First Name", "Last Name",
                      "Phone Number (0123456789)", "Street",
                      "City", "State(XY)", "Zip Code(12345)", "Email"]

        self.customer_credentials_labels = [None] * 8
        self.customer_credentials_textboxes = [None] * 8

        for row in range(len(self.customer_credentials_labels)):
            self.customer_credentials_labels[row] = Label(
                self.edit_customer_window_pop_up, text=label_list[row], font=("Arial", 14))
            self.customer_credentials_labels[row].grid(row=row + 1, column=0, padx=(10, 0), sticky=W)

        for row in range(len(self.customer_credentials_textboxes)):
            self.customer_credentials_textboxes[row] = Entry(
                self.edit_customer_window_pop_up, width=50)
            self.customer_credentials_textboxes[row].grid(row=row + 1, column=1)
            self.customer_credentials_textboxes[row].insert(0, self.customer[row])

    def add_edited_credentials_to_db(self):
        self.disable_textboxes()
        valid_credentials = CheckCredentials(self.customer_credentials_textboxes)

        if valid_credentials.full_check() is True:
            if self.check_if_phone_is_in_use() is not True:
                response = messagebox.askquestion("Edit Customer",
                                                  "Are you sure you want to edit the customer credentials with: \n"
                                                  "First Name: " + self.customer_credentials_textboxes[0].get() + "\n"
                                                  "Last Name: " + self.customer_credentials_textboxes[1].get() + "\n"
                                                  "Phone: " + self.customer_credentials_textboxes[2].get() + "\n"
                                                  "Street: " + self.customer_credentials_textboxes[3].get() + "\n"
                                                  "City: " + self.customer_credentials_textboxes[4].get() + "\n"
                                                  "State: " + self.customer_credentials_textboxes[5].get() + "\n"
                                                  "Zip Code: " + self.customer_credentials_textboxes[6].get() + "\n"
                                                  "Email: " + self.customer_credentials_textboxes[7].get() + "\n")

                if response == "yes":
                    try:
                        connection = sqlite3.connect(self.database_location)
                        cursor = connection.cursor()
                        if int(self.customer[2]) != int(self.customer_credentials_textboxes[2].get()):
                            cursor.execute("UPDATE customer "
                                           "SET f_name =?, l_name =?, phone =?, "
                                           "street =?, city =?, state =?, "
                                           "zipcode =?, email =?"
                                           "WHERE phone =?",
                                           (
                                               self.customer_credentials_textboxes[0].get(),
                                               self.customer_credentials_textboxes[1].get(),
                                               self.customer_credentials_textboxes[2].get(),
                                               self.customer_credentials_textboxes[3].get(),
                                               self.customer_credentials_textboxes[4].get(),
                                               self.customer_credentials_textboxes[5].get(),
                                               self.customer_credentials_textboxes[6].get(),
                                               self.customer_credentials_textboxes[7].get(),
                                               self.customer[2]))
                        else:
                            cursor.execute("UPDATE customer "
                                           "SET f_name =?, l_name =?, "
                                           "street =?, city =?, state =?, "
                                           "zipcode =?, email =?"
                                           "WHERE phone =?",
                                           (
                                                self.customer_credentials_textboxes[0].get(),
                                                self.customer_credentials_textboxes[1].get(),
                                                self.customer_credentials_textboxes[3].get(),
                                                self.customer_credentials_textboxes[4].get(),
                                                self.customer_credentials_textboxes[5].get(),
                                                self.customer_credentials_textboxes[6].get(),
                                                self.customer_credentials_textboxes[7].get(),
                                                self.customer_credentials_textboxes[2].get()))
                        connection.commit()
                        connection.close()
                        messagebox.showinfo("Success", "Successfully updated customer information")
                    except Exception as e:
                        messagebox.showerror("Error updating customer", "There was an error updating customer "
                                                                        "information in the database: ")
                        print(e)
            else:
                messagebox.showerror("Edited phone number",
                                     "Unable to update database, the new phone number is already in use.")

    def disable_textboxes(self):
        for textbox in range(8):
            self.customer_credentials_textboxes[textbox].configure(state="disabled")

    def enable_textboxes(self):
        for textbox in range(8):
            self.customer_credentials_textboxes[textbox].configure(state="enabled")

    def check_if_phone_is_in_use(self):
        old_phone = int(self.customer[2])
        new_phone = int(self.customer_credentials_textboxes[2].get())

        if old_phone != new_phone:
            connection = sqlite3.Connection(self.database_location)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customer WHERE phone = :phone_number", {"phone_number": new_phone})

            results = cursor.fetchall()
            connection.close()

            if len(results) != 0:
                return True
            else:
                return False
        else:
            return False

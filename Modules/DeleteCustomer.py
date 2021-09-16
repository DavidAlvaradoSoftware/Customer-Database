import sqlite3
from tkinter import messagebox
import shutil
import os
from datetime import date, datetime


class DeleteCustomer:
    def __init__(self, root, database_location, customer):
        self.root = root
        self.database_location = database_location
        self.customer = customer
        self.successful_execution = None
        self.delete_customer()

    def delete_customer(self):
        if self.ask_permission() == "yes":
            try:
                connection = sqlite3.connect(self.database_location)
                cursor = connection.cursor()

                cursor.execute("DELETE FROM customer WHERE phone=?", (self.customer[2],))

                connection.commit()

            except Exception as e:
                messagebox.showerror("Error Deleting", "There was an error deleting customer from database.")
                self.successful_execution = False
                print(e)
            else:
                try:
                    if os.path.exists(os.getcwd() + "\\Old Customers\\" + self.customer[1] + " " +
                                      self.customer[2]):

                        new_folder_name = self.customer[8] + " " + datetime.now().strftime("%b-%d-%Y-%H-%M-%S")
                        os.rename(self.customer[8], new_folder_name)

                        shutil.move(new_folder_name, os.getcwd() + "\\Old Customers\\")

                except Exception as f:
                    self.successful_execution = False
                    print(f)
                else:
                    self.successful_execution = True

    def was_deletion_successful(self):
        return self.successful_execution

    def ask_permission(self):
        response = messagebox.askquestion("Edit Customer",
                                          "Are you sure you want to DELETE the customer credentials with: \n"
                                          "First Name: " + self.customer[0] + "\n"
                                          "Last Name: " + self.customer[1] + "\n"
                                          "Phone: " + self.customer[2] + "\n"
                                          "Street: " + self.customer[3] + "\n"
                                          "City: " + self.customer[4] + "\n"
                                          "State: " + self.customer[5] + "\n"
                                          "Zip Code: " + self.customer[6] + "\n"
                                          "Email: " + self.customer[7] + "\n")
        return response

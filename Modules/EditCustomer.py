import sqlite3
from tkinter import *
from tkinter import messagebox
from Modules.ValidCredentialChecker import CheckCredentials


class EditCustomer:
    def __init__(self, root, database_location):
        self.root = root
        self.database_location = database_location

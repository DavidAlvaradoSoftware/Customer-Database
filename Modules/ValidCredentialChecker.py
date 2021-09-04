import re
from tkinter import messagebox


class CheckCredentials:
    def __init__(self, credential_textbox_array):
        self.credential_check_results = [None] * 5
        self.types_of_checks = ["Empty Textboxes", "Special Characters",
                                "Invalid Phone Number", "Invalid State",
                                "Invalid Zip Code"]
        self.customer_credential_array = credential_textbox_array

        self.full_check()

    def full_check(self):
        self.credential_check_results[0] = self.is_any_textbox_empty()
        self.credential_check_results[1] = self.special_character_check()
        self.credential_check_results[2] = self.invalid_phone_number_check()
        self.credential_check_results[3] = self.invalid_state_check()
        self.credential_check_results[4] = self.invalid_zip_code_check()

        failed_check = False

        for result in range(len(self.credential_check_results)):
            if self.credential_check_results[result] is True:
                failed_check = True
                break

        if failed_check is True:
            self.show_error(self.types_of_checks, result)
            return False
        else:
            return True

    def is_any_textbox_empty(self):
        result = False
        for textbox in range(len(self.customer_credential_array)):
            if self.customer_credential_array[textbox].get() == '':
                result = True
                break

        return result

    def special_character_check(self):
        regex = re.compile('[(<@_!#$%^&*?/\|}{~:_>)]-')
        result = False
        for textbox in range(len(self.customer_credential_array)):
            if regex.search(self.customer_credential_array[textbox].get()) is not None:
                result = True
                break

        return result

    def invalid_phone_number_check(self):
        phone_number = self.customer_credential_array[2].get()

        if len(phone_number) != 10:
            return True

        try:
            int(phone_number)
        except ValueError:
            return True

    def invalid_state_check(self):
        state = self.customer_credential_array[6].get()
        allowed_characters = re.compile('[A-Z]')
        if len(state) != 2:
            return True
        else:
            if allowed_characters.search(state) is None:
                return True
            else:
                return False

    def invalid_zip_code_check(self):
        zip_code = self.customer_credential_array[7].get()

        if len(zip_code) != 5:
            return True
        else:
            try:
                int(zip_code)
            except ValueError:
                return True
            else:
                return False

    def show_error(self, types_of_errors, result):
        messagebox.showerror(types_of_errors[result], "An error occured when checking customer credentials."
                                                      "Type of error: " + types_of_errors[result] +
                                                      " make sure you follow the layout stated near "
                                                      "the empty text boxes.")

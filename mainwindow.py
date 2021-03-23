from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
import hashlib
import string
import csv
import smtplib
import random


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartWindow)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartWindow(Frame):
    def __init__(self, master):
        """Starwindow for app"""

        Frame.__init__(self, master)
        Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5, padx=20)
        Button(self, text="Login", font=('Helvetica', 15), command=lambda: master.switch_frame(LoginSystem))\
            .pack(pady=15)
        Button(self, text="Register", font=('Helvetica', 15), command=lambda: master.switch_frame(RegisterSystem))\
            .pack(pady=15)
        Button(self, text="Enter as guest", font=('Helvetica', 15), command=lambda: master.switch_frame(App))\
            .pack(pady=15)


class LoginSystem(Frame):
    """Login to account"""
    def __init__(self, master):
        Frame.__init__(self, master)

        # ----------------------app layout/upper frame----------------------
        self.upper_window = Frame(self, height=50, width=300)
        self.upper_window.pack()
        # Go back to start window
        Button(self.upper_window, text='🢀', relief=GROOVE, cursor='tcross',
               command=lambda: master.switch_frame(StartWindow)).place(x=0, y=0)

        # ----------------------app layout/middle frame----------------------
        self.main_window = Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack(pady=10)
        Label(self.title_frame, text='CHESS MASTER', font='arial 20').pack(expand=True)

        # Username (MIDDLE FRAME)
        self.username_frame = Frame(self.main_window)
        self.username_frame.pack(pady=20)

        ttk.Label(self.username_frame, text='Username', font='arial 11').pack(expand=True, side=LEFT)
        self.user_name_var = StringVar()
        self.username_entry = ttk.Entry(self.username_frame, textvariable=self.user_name_var)
        self.username_entry.pack(expand=True, side=LEFT, padx=10)

        # Password (MIDDLE FRAME)
        self.password_frame = Frame(self.main_window)
        self.password_frame.pack(pady=10)

        Label(self.password_frame, text='Password', font='arial 11').pack(expand=True, side=LEFT)
        self.password_var = StringVar()
        self.password_entry = ttk.Entry(self.password_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(expand=True, side=LEFT, padx=10)

        # Extra settings (MIDDLE FRAME)
        self.extra = Frame(self.main_window)
        self.extra.pack()
        # Show/hide password
        self.show_password_var = IntVar()
        self.show_password = Checkbutton(self.extra, text='Show password', font='arial 7 bold',
                                         variable=self.show_password_var, command=self.show)
        self.show_password.pack(side=LEFT, padx=30)
        # Forgot password
        self.forgot_password = Button(self.extra, text='Forgot your password?', font='arial 6 italic', fg='blue',
                                      command=lambda: master.switch_frame(ForgotPassword), relief=FLAT)
        self.forgot_password.pack(side=LEFT)

        # Login (MIDDLE FRAME)
        self.login_frame = Frame(self.main_window)
        self.login_frame.pack(pady=20)
        self.login_button = ttk.Button(self.login_frame, text='Login', command=self.verify_credentials)
        self.login_button.pack()

        # ----------------------app layout/lower frame----------------------
        self.lower_window = Frame(self, height=20)
        self.lower_window.pack()

    def show(self):
        """Show or hide passsword entry"""

        if self.show_password_var.get() == 1:
            self.password_entry.config(show='')

        else:
            self.password_entry.config(show='*')

    def verify_credentials(self):
        """Check password and username"""

        # Get username and password
        username = self.user_name_var.get().lower()
        password = self.password_var.get()

        # Hash password
        message = password.encode()
        user_hashed_password = hashlib.blake2b(message).hexdigest()
        found = False

        # search for hashed password and username in database
        with open('users.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for line in csv_reader:
                try:
                    if line[0] == username and user_hashed_password == line[1]:
                        found = True
                        break

                    else:
                        found = False

                except IndexError:
                    break

        # Check whether the account was found
        if found:
            messagebox.showinfo('Success', 'Successful login')
        else:
            messagebox.showerror('Error', 'Invalid credentials')


class RegisterSystem(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # ----------------------App layout/upper frame----------------------
        self.upper_window = Frame(self, height=50, width=350)
        self.upper_window.pack()
        Button(self.upper_window, text='🢀', relief=GROOVE, cursor='tcross',
               command=lambda: master.switch_frame(StartWindow)).place(x=0, y=0)

        # ----------------------App layout/middle frame----------------------
        self.main_window = Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack()
        Label(self.title_frame, text='REGISTER', font='arial 20').pack(expand=True)

        # New username (MIDDLE FRAME)
        self.new_user_frame = Frame(self.main_window)
        self.new_user_frame.pack(pady=10)

        ttk.Label(self.new_user_frame, text='New username\t ').pack(expand=True, side=LEFT)
        self.new_user_name_var = StringVar()
        self.new_username_entry = ttk.Entry(self.new_user_frame, textvariable=self.new_user_name_var)
        self.new_username_entry.pack(expand=True, side=LEFT)

        self.new_user_name_error_frame = Frame(self.main_window, height=1)
        self.new_user_name_error_frame.pack()
        self.new_user_name_error_var = StringVar()
        self.new_user_name_error = Label(self.new_user_name_error_frame, textvariable=self.new_user_name_error_var,
                                         fg='red', font='arial 7')

        # New password (MIDDLE FRAME)
        self.new_password_frame = Frame(self.main_window)
        self.new_password_frame.pack(pady=10)

        Label(self.new_password_frame, text='New password\t ').pack(expand=True, side=LEFT)
        self.new_password = StringVar()
        self.new_password_entry = ttk.Entry(self.new_password_frame, textvariable=self.new_password)
        self.new_password_entry.pack(expand=True, side=LEFT)

        self.password_error_frame = Frame(self.main_window, height=1)
        self.password_error_frame.pack()
        self.password_error_var = StringVar()
        self.password_error = Label(self.password_error_frame, textvariable=self.password_error_var,
                                    fg='red', font='arial 7')

        # Confirm new password (MIDDLE FRAME)
        self.confirm_password_frame = Frame(self.main_window)
        self.confirm_password_frame.pack(pady=10)

        Label(self.confirm_password_frame, text='Confirm pass\t ').pack(expand=True, side=LEFT)
        self.confirmed_password = StringVar()
        self.confirmed_password_entry = ttk.Entry(self.confirm_password_frame, textvariable=self.confirmed_password,
                                                  show="*")
        self.confirmed_password_entry.pack(expand=True, side=LEFT)

        self.confirmed_password_error_frame = Frame(self.main_window, height=1)
        self.confirmed_password_error_frame.pack()
        self.confirmed_password_error_var = StringVar()
        self.confirmed_password_error = Label(self.confirmed_password_error_frame,
                                              textvariable=self.confirmed_password_error_var, fg='red', font='arial 7')

        # Email (MIDDLE FRAME)
        self.email_frame = Frame(self.main_window)
        self.email_frame.pack(pady=10)

        self.email_var = StringVar()
        self.email_address = Label(self.email_frame, text='Email address\t')
        self.email_address.pack(side=LEFT)
        self.email_address_entry = Entry(self.email_frame, fg='grey', textvariable=self.email_var)
        self.email_var.set('@gmail.com')
        self.email_address_entry.pack(expand=True, side=LEFT)

        self.email_error_frame = Frame(self.main_window, height=1)
        self.email_error_frame.pack()
        self.email_error_var = StringVar()
        self.email_error = Label(self.email_error_frame, textvariable=self.email_error_var, fg='red', font='arial 7')

        # Date of birth (MIDDLE FRAME)
        self.dob_frame = Frame(self.main_window)
        self.dob_frame.pack(pady=10)

        self.dob = Label(self.dob_frame, text='Date of birth\t')
        self.dob.pack(side=LEFT)
        self.dob_entry = DateEntry(self.dob_frame, date_pattern='dd/MM/yyyy', width=17, bg="darkblue",
                                   fg="white", year=2000)
        self.dob_entry.pack(expand=True, side=LEFT)

        self.dob_error_frame = Frame(self.main_window, height=1)
        self.dob_error_frame.pack()
        self.dob_error_var = StringVar()
        self.dob_error = Label(self.dob_error_frame, textvariable=self.dob_error_var, fg='red', font='arial 7')

        # Register all details (MIDDLE FRAME)
        self.save_data_frame = Frame(self.main_window)
        self.save_data_frame.pack(pady=10)

        self.save_button = ttk.Button(self.save_data_frame, text='Save', command=self.store_new_data)
        self.save_button.pack()

        # ----------------------App layout/lower frame----------------------
        self.lower_frame = Frame(self, height=50)
        self.lower_frame.pack()

    @staticmethod
    def check_email(email):
        """Checks whether the email account user entered exists"""

        try:
            receiver_address = email  # Receiver email address
            subject = "Welcome"
            body = f"Hello from ChessMaster\n\nYour account has been succesfully registered!" \
                   f"\nWith regards," \
                   f"\n\nChessMaster Inc"
            # Endpoint for the SMTP Gmail server
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # Login with your Gmail account using SMTP
            smtp_server.login("pruebadelogin524@gmail.com", "logintest1234")
            # Combine the subject and the body onto a single message
            message = f"Subject: {subject}\n\n{body}"
            # Message sent in the above format (Subject:...\n\nBody)
            smtp_server.sendmail("pruebadelogin524@gmail.com", receiver_address, message)
            # Close our endpoint
            smtp_server.close()

            # if nothing went wrong it means the email account exist
            exists = True
        except:
            # if an exception occurs, the account doesn't exist
            exists = False

        return exists

    @staticmethod
    def calculate_age(dob):
        """Calculate the user age"""

        # get today's date
        today = date.today()

        # convert the age string into a list
        born = dob.split('/')
        date_of_birth = date(int(born[2]), int(born[1]), int(born[0]))

        # operation that calculates the difference between today and the birthdate (age)
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    @staticmethod
    def hash_pass(password):
        """Hash the password for better security"""

        message = password.encode()
        hashed_password = hashlib.blake2b(message).hexdigest()

        return hashed_password

    @staticmethod
    def check_pass(password):
        """Check if the password meets the requirements"""

        # lists of characters the password must contain
        alpha = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        numbers = [str(number) for number in range(11)]
        symbols = list('`¦¬!\"£$€%^&*()_+=-[]#\',./{}~@<>?|\\:')

        # variables for the check
        is_len = False
        is_alpha = 0
        is_lower = 0
        is_num = 0
        is_special = 0

        if 8 <= len(password) <= 20:
            is_len = True

        for letter in password:
            if letter in alpha:
                is_alpha += 1

            if letter in lower:
                is_lower += 1

            if letter in numbers:
                is_num += 1

            if letter in symbols:
                is_special += 1

        # if all requirements are met return true, else give false
        if is_len and is_alpha >= 2 and is_lower >= 2 and is_num >= 2 and is_special >= 2:
            return True

        else:
            return False

    def store_new_data(self):
        """Store the data in the database after checking it all"""

        requirements_met = 0

        # Check if username is valid
        username = self.new_user_name_var.get().lower()
        if 3 > len(username) < 20:
            # if invalid, display alert message
            self.new_user_name_error_var.set('Username must be between 3-20 characters')
            self.new_user_name_error.pack(expand=True)
        else:
            requirements_met += 1
            self.new_user_name_error.pack_forget()

        # Check if password is valid
        password = self.new_password.get()
        confirmed_password = self.confirmed_password.get()
        if not self.check_pass(password):
            # if invalid, display alert message
            self.password_error_var.set('Password requisites: 8-20 characters, 2 - symbols, numbers, upper, lower')
            self.password_error.pack(expand=True)
        else:
            requirements_met += 1
            self.password_error.pack_forget()

            # check if passwords match
            if password != confirmed_password:
                self.confirmed_password_error_var.set('Passwords do not match')
                self.confirmed_password_error.pack(expand=True)
            else:
                # if not, display alert message
                requirements_met += 1
                self.confirmed_password_error.pack_forget()

        # Check if email is valid
        email = self.email_var.get()
        if not self.check_email(email):
            # if invalid, display alert message
            self.email_error_var.set("Invalid email address")
            self.email_error.pack(expand=True)
        else:
            requirements_met += 1
            self.email_error.pack_forget()

        # Check date of birth is valid (age between 0-70)
        date_of_birth = self.dob_entry.get()
        age = self.calculate_age(date_of_birth)
        if 14 > age > 70:
            # if invalid, display alert message
            self.dob_error_var.set('You must be between 14-70 years of age')
            self.dob_error.pack()
        else:
            requirements_met += 1
            self.dob_error.pack_forget()

        # Verify all requirements were met
        if requirements_met == 5:
            # Store data into database
            with open('users.csv', 'a') as f:
                f.write(f'\n{username.lower()},{self.hash_pass(password)},{email},{age}')

            # ask user to leave or stay
            answer = messagebox.askyesno('Success', 'Your data has successfully been saved. Do you want to leave?')

            if answer:
                # switch if user wants to leave
                self.master.switch_frame(LoginSystem)
            else:
                # reset all entries blank if user wants to stay
                self.reset()
        else:
            messagebox.showerror('Error', 'Incomplete or invalid data has been entered')

    def reset(self):
        """Reset all register entries"""

        self.new_user_name_var.set('')
        self.new_password.set('')
        self.confirmed_password.set('')
        self.email_var.set('')


class ForgotPassword(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.passcode = None

        # ---------------------App layout/upper frame---------------------
        self.upper_window = Frame(self, height=50, width=350)
        self.upper_window.pack()
        Button(self.upper_window, text='🢀', relief=GROOVE, cursor='tcross',
               command=lambda: master.switch_frame(LoginSystem)).place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack()

        Label(self.title_frame, text='Recover password', font='arial 20').pack(expand=True)

        # Recover password (MIDDLE FRAME)
        self.recover_password_frame = Frame(self.main_window)
        self.recover_password_frame.pack(pady=10)

        Label(self.recover_password_frame, text='Email address\t ').pack(expand=True, side=LEFT)
        self.recover_password_var = StringVar()
        self.recover_password_entry = ttk.Entry(self.recover_password_frame, textvariable=self.recover_password_var)
        self.recover_password_entry.pack(expand=True, side=LEFT)

        self.recover_password_error_frame = Frame(self.main_window)
        self.recover_password_error_frame.pack()
        self.recover_password_error_var = StringVar()
        self.recover_password_error = Label(self.recover_password_error_frame,
                                            textvariable=self.recover_password_error_var, fg='red')

        # Button (MIDDLE FRAME)
        Button(self.main_window, text='continue', command=self.get_email).pack()

        # ---------------------App layout/lower frame---------------------
        self.lower_frame = Frame(self, height=50)
        self.lower_frame.pack()

    def check_email(self):
        """Check whether the email entered exists"""

        # Check if the email exists in the database
        with open('users.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(f)
            # loop each line in database
            for line in csv_reader:
                if line[2] == self.recover_password_var.get():
                    break
                else:
                    continue

        # Generate 4 digit random number
        code = [str(random.randint(0, 11)) for _ in range(4)]
        self.passcode = ''.join(code)

        # Send passcode to user
        receiver_address = self.recover_password_var.get()
        subject = "Passcode verification"
        body = f"Hello from ChessMaster!\n\nHere is yor passcode\n{self.passcode}\nWith regards,\n\nChessMaster Inc.r"
        # Endpoint for the SMTP Gmail server (Don't change this!)
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # Login with dummy Gmail account using SMTP
        smtp_server.login("pruebadelogin524@gmail.com", "logintest1234")
        # Let's combine the subject and the body onto a single message
        message = f"Subject: {subject}\n\n{body}"
        # We'll be sending this message in the above format (Subject:...\n\nBody)
        smtp_server.sendmail("pruebadelogin524@gmail.com", receiver_address, message)
        # Close our endpoint
        smtp_server.close()
        print('went well')

        # if passcode exists we store it in temporal file
        with open('temp/passcode', 'w') as f:
            f.write(self.passcode)

        with open('temp/email', 'w') as f:
            f.write(self.recover_password_var.get())

        # if nothing went wrong, the message has been sent
        return True

    def get_email(self):
        """Retrieve email input from user"""

        # Check if it valid
        valid = self.check_email()

        # If it is valid, we generate a new window
        if valid:
            self.master.switch_frame(VerifyPasscode)

        else:
            # if the email is invalid we add a warning message
            self.recover_password_error_frame.pack()
            self.recover_password_error.pack(pady=10)
            messagebox.showerror('Error', 'Unrecognized email address')
            self.recover_password_error_var.set("Invalid email address (Make sre you have registered)")


class VerifyPasscode(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # ---------------------App layout/upper frame---------------------
        self.upper_window = Frame(self, height=50, width=350)
        self.upper_window.pack()
        Button(self.upper_window, text='🢀', relief=GROOVE, cursor='tcross',
               command=lambda: master.switch_frame(StartWindow)).place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack()

        Label(self.title_frame, text='Code has been sent', font='arial 20').pack(expand=True)

        # Passcode (MIDDLE FRAME)
        Label(self.main_window, text='Check your email, a passcode has been sent.\nEnter yor 4-digit code here',
              font='arial 7 bold italic').pack(pady=10)

        self.passcode_var = StringVar()
        self.passcode_entry = ttk.Entry(self.main_window, textvariable=self.passcode_var)
        self.passcode_entry.pack(expand=True, pady=10)
        Button(self.main_window, text='continue', command=self.check_passcode).pack(expand=True)

        # ----------------------app layout/lower frame----------------------
        self.lower_window = Frame(self, height=20)
        self.lower_window.pack()

    def check_passcode(self):
        """Check if the passcode is correct"""

        # Get passcode from file
        with open('temp/passcode', 'r') as f:
            stored_passcode = f.read()

        if self.passcode_var.get() == stored_passcode:
            self.master.switch_frame(NewPassword)
        else:
            messagebox.showerror('Error', 'Incorrect passcode')


class NewPassword(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # ---------------------App layout/upper frame---------------------
        self.upper_window = Frame(self, height=50, width=350)
        self.upper_window.pack()
        Button(self.upper_window, text='🢀', relief=GROOVE, cursor='tcross',
               command=lambda: master.switch_frame(StartWindow)).place(x=0, y=0)

        # ---------------------App layout/middle frame---------------------
        self.main_window = Frame(self)
        self.main_window.pack()

        # Title (MIDDLE FRAME)
        self.title_frame = Frame(self.main_window)
        self.title_frame.pack()

        Label(self.title_frame, text='Succces!', font='arial 20').pack(expand=True)

        # Passcode (MIDDLE FRAME)
        Label(self.main_window, text='Enter your new password here.',
              font='arial 7 bold italic').pack(pady=10)

        self.new_pass_var = StringVar()
        self.new_pass_entry = ttk.Entry(self.main_window, textvariable=self.new_pass_var)
        self.new_pass_entry.pack(expand=True, pady=10)

        self.show_password = Checkbutton(self.main_window, text='Show Password', font='arial 7 bold',
                                         variable=self.new_pass_var, command=self.show)
        self.show_password.pack(side=LEFT, padx=30)

        Button(self.main_window, text='continue', command=self.set_new_pass).pack(expand=True)

        # ----------------------app layout/lower frame----------------------
        self.lower_window = Frame(self, height=20)
        self.lower_window.pack()

    def show(self):
        """Show or hide passsword entry"""

        if self.new_pass_var.get() == 1:
            self.new_pass_entry.config(show='')

        else:
            self.new_pass_entry.config(show='*')

    def set_new_pass(self):
        """set new password"""

        # get the email
        with open('temp/email', 'r') as f:
            email = f.read()

        # Read the original file
        with open('users.csv', 'r') as f:
            csv_reader = csv.reader(f)
            # convert the data to a list
            data = [line for line in csv_reader]

        # Replace the required items in the list
        for line in data:
            # Find the line containing the email address
            if line[2] == email:
                # Replace the password
                line[1] = self.hash_pass(self.new_pass_var.get())

        with open('users.csv', 'w') as f:
            for line in data:
                for char in line:
                    f.write(f'{char},')
                f.write('\n')

        self.master.switch_frame(LoginSystem)

    @staticmethod
    def hash_pass(password):
        """Hash the password for better security"""

        message = password.encode()
        hashed_password = hashlib.blake2b(message).hexdigest()

        return hashed_password


if __name__ == "__main__":
    app = App()
    app.mainloop()

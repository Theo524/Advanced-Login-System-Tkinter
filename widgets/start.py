import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from widgets.login import LoginSystem
from widgets.register import RegisterSystem


class StartApp(tk.Tk):
    def __init__(self):
        """Start of application"""

        tk.Tk.__init__(self)

        # key variables - result of login system
        self.logged_in = False
        self.mode = None
        self._credentials = ()

        # class attributes
        self.resizable(0, 0)
        self.geometry('500x600')
        self.title('Welcome')
        photo = tk.PhotoImage(file=os.getcwd() + "\\widgets\\app_img\\user_icon.png", master=self)
        self.iconphoto(False, photo)

        # themes
        self.style = ThemedStyle(self)
        self.style.theme_use('scidsand')

        # set paths for file handling
        self.database = os.getcwd() + '\\database\\users.db'
        self.temp_files = os.getcwd() + '\\temp'

        # other frames
        self._frame = None
        self.frames = {'start': StartWindow, 'login': LoginSystem, 'register': RegisterSystem}

        # starting frame
        self.switch_frame(self.frames['start'])

    def switch_frame(self, frame_class):
        """Switch current frame"""
        new_frame = frame_class(self, width=1000, height=620)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill='both')

    def close_win(self):
        """Close window"""
        self.destroy()

    @property
    def get_credentials(self):
        return self._credentials

    def __str__(self):

        if self.logged_in:
            msg = f'Logged in as {self.mode}'

        else:
            msg = 'Not logged in'

        return msg


class StartWindow(ttk.Frame):
    def __init__(self, master, **kwargs):
        """Start window for app"""

        ttk.Frame.__init__(self, master, **kwargs)
        self.master = master

        # container
        self.scene = ttk.Frame(self)
        self.scene.pack(pady=110)

        # themes
        self.master.style.configure('start_page.TButton',
                                    font=('Arial', 15))
        self.master.style.configure("Placeholder.TEntry",
                                    foreground='grey')

        # Title
        ttk.Label(self.scene, text="LOGIN SYSTEM",
                  font=('Arial', 30))\
            .pack(side="top", padx=30, pady=15)

        # Login Button
        ttk.Button(self.scene, text="Login",
                    command=self.login,
                   style='start_page.TButton', cursor='hand2')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Registration button
        ttk.Button(self.scene, text="Register",
                   command=self.register,
                   style='start_page.TButton', cursor='hand2')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Guest mode button
        ttk.Button(self.scene, text="Enter as guest",
                   command=self.set_mode_guest,
                   style='start_page.TButton')\
            .pack(pady=20, ipady=5, ipadx=10)

        # Just my name at the bottom
        tk.Label(self.scene, text="Developed by Theo Brown",
              font=('Calibri', 10))\
            .pack()

    def set_mode_guest(self):
        """Logged in as guest"""

        # Save state
        self.master.logged_in = True
        self.master.mode = 'guest'
        self.master.credentials = ('\'guest user\'',)

        # We quit the start_page and start_app to start the chess app in guest mode
        self.master.close_win()

    def login(self):
        """Displays login page"""

        # place 'LoginSystem' frame
        self.master.switch_frame(self.master.frames['login'])
        self.master.title('Login')

    def register(self):
        """Displays registration page"""

        # place 'RegisterSystem' frame
        self.master.switch_frame(self.master.frames['register'])
        self.master.title('Register')

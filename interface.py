import tkinter as tk
from tkinter import ttk
import keyring as kr


class UserFrame(ttk.Frame):
    """Initial application frame for user to input name"""
    def __init__(self, container):
        super().__init__(container)
        self._window = container
        self._window.window_size(300, 100)
        self._username = self.make_widgets()
        self.pack(expand=True)

    def make_widgets(self):
        """Adds entry and button to Frame to get username string."""
        # username entry with Return binding
        username = tk.StringVar()
        username_entry = ttk.Entry(self, textvariable=username)
        username_entry.bind('<Return>', self.initialize_user)
        username_entry.focus()
        username_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        # button
        get_name_button = ttk.Button(self, text="enter name")
        get_name_button['command'] = self.initialize_user
        get_name_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

        return username

    def initialize_user(self, event=None):
        """Handle 'enter name' button clicked or entry <Return> event."""

        # initialize KeyRing object with user string, return if no string
        user = self._username.get()
        if not user:
            return
        keyring = kr.KeyRing(user)

        # raise ControlFrame, terminate UserFrame
        ControlFrame(self._window, keyring, user).tkraise()
        self.destroy()


class ControlFrame(ttk.Frame):
    """Control frame of the application after user has entered name."""
    def __init__(self, container, keyring, user):
        super().__init__(container)
        self._window = container
        self._window.window_size(500, 500)
        self._keyring = keyring
        self._user = user
        self.pack(expand=True)

        # domain selection
        # username selection

    # TODO: select domain and username or add new
    # SQL query to populate combobox or listbox

    # TODO: get current password of selection

    # TODO: create new password for selection

    # TODO: copy password from selected username/domain to another

    # TODO: import/export data via JSON/CSV

    # TODO: close sql connection and exit program

    # TODO: close sql connection and change user


class App(tk.Tk):
    """Root window of application."""
    def __init__(self):
        super().__init__()

        # configure root window
        self.title('NakedKeyRing')
        self.iconbitmap('./icon/keyring.ico')

    def window_size(self, width, height):
        """Takes width and height. Centers application on screen."""
        offset_x = int(self.winfo_screenwidth()/2 - width/2)
        offset_y = int(self.winfo_screenheight()/2 - height/2)
        self.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        self.resizable(False, False)


if __name__ == '__main__':
    app = App()
    frame = UserFrame(app)
    tk.mainloop()

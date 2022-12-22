import tkinter as tk
from tkinter import ttk
import keyring as kr


class ProfileFrame(ttk.Frame):
    """Application frame to initialize Profile and associated KeyRing."""
    def __init__(self, app_window):
        super().__init__(app_window)
        self._window = app_window
        self._window.window_size(300, 100)
        self.pack(expand=True)
        self.make_widgets()

    def make_widgets(self):
        """Adds entry and button to Frame to get profile string."""

        def initialize_user(event=None):
            """Handler 'enter profile' button clicked or entry <Return> event."""

            # initialize KeyRing object with profile string, return if no string
            if event is None:
                profile = entered_string.get()
            else:
                profile = event.widget.get()
            if not profile:
                return
            keyring = kr.KeyRing(profile)

            # initialize and raise ManagerFrame, terminate ProfileFrame
            ManagerFrame(self._window, profile, keyring).tkraise()
            self.destroy()

        # username entry with Return binding
        entered_string = tk.StringVar()
        profile_entry = ttk.Entry(self, textvariable=entered_string)
        profile_entry.bind('<Return>', initialize_user)
        profile_entry.focus()
        profile_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        # button
        get_profile_button = ttk.Button(self, text="enter profile", command=initialize_user)
        get_profile_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)


class ManagerFrame(ttk.Frame):
    """Control frame of the application after user has entered name."""
    def __init__(self, app_window, profile, keyring):
        super().__init__(app_window)
        self._window = app_window
        self._profile = profile
        self._keyring = keyring

        self._window.window_size(300, 300)

        self.pack()

        self.make_widgets()

    def make_widgets(self):
        """"""
        def domain_selected(event):
            """Event handling for domain selection."""
            selected = event.widget.get()
            # sets username combox to queried values of existing distinct usernames
            username_combo['values'] = self._keyring.query_username(selected)

        # domain selection: label, sql query, combobox
        domain_label = ttk.Label(self, text='Domain')
        domain_label.pack()

        domain_query = self._keyring.query_domain()

        domain_combo = ttk.Combobox(self)
        domain_combo['values'] = domain_query
        domain_combo.bind('<<ComboboxSelected>>', domain_selected)
        domain_combo.pack()

        # username selection: label, sql query based on domain selection, combox
        username_label = ttk.Label(self, text='Username')
        username_label.pack()

        username_combo = ttk.Combobox(self)
        username_combo.pack()

        # horizontal separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(pady=5, fill='x')

        # TODO: get current password button

        # TODO: generate password button

        # TODO: password entry

        # TODO: export password list button

        # TODO: commit exit button: close sql connection


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
    frame = ProfileFrame(app)
    tk.mainloop()

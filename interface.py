import tkinter as tk
from tkinter import ttk
from string import ascii_uppercase, ascii_lowercase, digits
from random import choice, shuffle
import time
import keyring as kr


class ProfileFrame(ttk.Frame):
    """Initial frame of app.: gets Profile str. and initializes KeyRing object."""
    def __init__(self, app_window):
        super().__init__(app_window)
        self._window = app_window
        self._window.window_size(300, 100)
        self.pack(expand=True)
        self.run_widgets()

    def run_widgets(self):
        """Widgets to get Profile string."""

        def initialize_user(event=None):
            """Handler for 'enter profile' button clicked or entry <Return> event."""

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
        get_profile_button = ttk.Button(self, text="Enter Profile", command=initialize_user)
        get_profile_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)


class ManagerFrame(ttk.Frame):
    """Form interface for fetching/adding/updating data."""
    def __init__(self, app_window, profile, keyring):
        super().__init__(app_window)
        self._window = app_window
        self._profile = profile
        self._keyring = keyring
        self._window.window_size(300, 300)
        self.pack()
        self.run_widgets()

    def run_widgets(self):
        """Executes ManagerFrame assets."""

        def reset_displays(domain_field=False, username_field=False, key_field=False):
            """Clears display string associated combobox(es) and entry widgets."""
            if domain_field:
                domain_combo.set('')
            if username_field:
                username_combo.set('')
            if key_field:
                key_string.set('')

        def domain_update():
            """Updates Domain combobox list and clears display strings."""

            reset_displays(True)
            domain_combo.configure(values=self._keyring.fetch_query())
            username_update()

        def username_update():
            """Updates dates username combobox list and clears username, key displays."""

            reset_displays(False, True, True)
            domain = domain_combo.get()
            username_combo.configure(values=self._keyring.fetch_query(domain))

        def key_update():
            """Fetches and displays key."""

            domain = domain_combo.get()
            username = username_combo.get()
            key = self._keyring.fetch_query(domain, username)
            key = str(key[0])
            key_string.set(key)

        def selection(event):
            """Event handling for domain selection."""

            combobox = event.widget
            if combobox is domain_combo:
                username_update()
                reset_displays(False, True, True)
            elif combobox is username_combo:
                key_update()

        def generate_new_key():
            """Randomly generates a key and displays in key_combobox."""
            # TODO: dynamic length, contains, special based on options frame below
            length = 14
            contains = ("U", "L", "D", "S")
            special = "!@#$%^&*+=?[]()~`"

            # possible sets of characters which *contains will cross-reference
            characters = {
                "U": ascii_uppercase,
                "L": ascii_lowercase,
                "D": digits,
                "S": special
            }

            new_key_builder = []
            all_characters = ''

            for mand_char in contains:
                # add one of each mandatory character
                new_key_builder.append(choice(characters[mand_char]))
                # build total character set for next stage
                all_characters = all_characters + characters[mand_char]
                length -= 1

            # populate remaining length with random char from all_character set
            while length > 0:
                new_key_builder.append(choice(all_characters))
                length -= 1

            # shuffle, join to string, display
            shuffle(new_key_builder)
            new_key = ''.join(new_key_builder)
            key_string.set(new_key)

        def commit_key():
            """Commits key in key display to db."""

            domain = domain_combo.get()
            username = username_combo.get()
            key = key_entry.get()
            date_updated = time.strftime("%Y-%m-%d %H:%M:%S.000", time.localtime())

            update = (domain, username, key, date_updated)
            self._keyring.update_table(update)

            # clear combobox(es) and update domain query
            domain_update()

        # TODO: format widgets, make look pretty

        # domain selection: label, combobox = sql query result
        domain_label = ttk.Label(self, text='Domain')
        domain_label.pack()

        domain_combo = ttk.Combobox(self)
        domain_combo.bind('<<ComboboxSelected>>', selection)
        domain_combo.pack()

        # username selection: label, combobox = sql query (domain)
        username_label = ttk.Label(self, text='Username')
        username_label.pack()

        username_combo = ttk.Combobox(self)
        username_combo.bind('<<ComboboxSelected>>', selection)
        username_combo.pack()

        # horizontal separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(pady=5, fill='x')

        # key display: label, entry = sql query (domain, username, most recent)
        key_label = ttk.Label(self, text='Key')
        key_label.pack()

        key_string = tk.StringVar()
        key_entry = ttk.Entry(self, textvariable=key_string)
        key_entry.pack()

        # generate new key button
        generate_button = ttk.Button(self, text="Generate New", command=generate_new_key)
        generate_button.pack()

        # commit new Key
        commit_button = ttk.Button(self, text="Commit Key", command=commit_key)
        commit_button.pack()

        domain_update()

        # TODO: grey out widgets when entries have not been selected
        # TODO: export password list button (text, json, csv?)
        # TODO: commit exit button: close sql connection
        # TODO: add configure options(LabelFrame) to pass into keyring.create_new_key
        #  length(spinbox), contains(checkbox), special(entry
        # TODO: add status bar and messages


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

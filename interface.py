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
        self._window.window_size(250, 80)
        self.pack(expand=True)

        # username entry with Return binding
        self.entered_string = tk.StringVar()
        self.profile_entry = ttk.Entry(self, textvariable=self.entered_string)
        self.profile_entry.bind('<Return>', self.initialize_user)
        self.profile_entry.focus()
        self.profile_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        # button
        self.get_profile_button = ttk.Button(self, text="Enter Profile", command=self.initialize_user)
        self.get_profile_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

    def initialize_user(self, event=None):
        """Handler for 'enter profile' button clicked or entry <Return> event."""

        # initialize KeyRing object with profile string, return if no string
        if event is None:
            profile = self.entered_string.get()
        else:
            profile = event.widget.get()
        if not profile:
            return
        keyring = kr.KeyRing(profile)

        # initialize and raise ManagerFrame, terminate ProfileFrame
        ManagerFrame(self._window, profile, keyring).tkraise()
        self.destroy()


class ManagerFrame(ttk.Frame):
    """Form interface for fetching/adding/updating data."""
    def __init__(self, app_window, profile, keyring):
        super().__init__(app_window)
        self._window = app_window
        self._profile = profile
        self._keyring = keyring
        self._window.window_size(250, 325)
        self.pack(fill=tk.BOTH, padx=5, pady=5)

        top_field_options = {'fill': tk.X, 'padx': 10}

        # domain selection: label, combobox = sql query result
        self.domain_label = ttk.Label(self, text='Domain')
        self.domain_label.pack(top_field_options)

        self.domain_text = tk.StringVar()
        self.domain_text.trace('w', self.selection)
        self.domain_combo = ttk.Combobox(self, textvariable=self.domain_text)
        self.domain_combo.bind('<<ComboboxSelected>>', self.selection)
        self.domain_combo.pack(top_field_options)

        # username selection: label, combobox = sql query (domain)
        self.username_label = ttk.Label(self, text='Username')
        self.username_label.pack(top_field_options)

        self.username_text = tk.StringVar()
        self.username_text.trace('w', self.selection)
        self.username_combo = ttk.Combobox(self, textvariable=self.username_text)
        self.username_combo.bind('<<ComboboxSelected>>', self.selection)
        self.username_combo.pack(top_field_options)

        # horizontal separator
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.pack(**top_field_options, pady=10)

        # key display: label, entry = sql query (domain, username, most recent)
        self.key_label = ttk.Label(self, text='Key')
        self.key_label.pack(**top_field_options)

        self.key_string = tk.StringVar()
        self.key_entry = ttk.Entry(self, textvariable=self.key_string)
        self.key_entry.pack(**top_field_options)

        lower_frame_options = {'fill': tk.BOTH, 'side': tk.LEFT, 'padx': 10, 'pady': 10}
        button_options = {'fill': tk.BOTH, 'expand': True, 'pady': 3}
        # buttons frame
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(**lower_frame_options)

        # generate new key button
        self.generate_button = ttk.Button(self.buttons_frame,
                                          text="Generate New",
                                          command=self.generate_new_key)
        self.generate_button.pack(**button_options)

        # commit new Key
        self.commit_button = ttk.Button(self.buttons_frame,
                                        text="Save Key",
                                        command=self.commit_key)
        self.commit_button.pack(**button_options)

        # database export to .txt button
        self.export_txt_button = ttk.Button(self.buttons_frame,
                                            text="Export .txt",
                                            command=self.export_txt)
        self.export_txt_button.pack(**button_options)

        # key options: LabelFrame
        self.key_options = ttk.LabelFrame(self, text="Include:")
        self.key_options.pack(**lower_frame_options)

        options_config_single = {'anchor': tk.W, 'padx': 5, 'pady': 3}
        options_config_double ={'side': tk.LEFT, 'padx': 5, 'pady': 3}

        # contains lower alphabet checkbox
        self.lower_checkbox_v = tk.StringVar(value=ascii_lowercase)
        self.lower_checkbox = ttk.Checkbutton(self.key_options,
                                              text="lower a:z",
                                              variable=self.lower_checkbox_v,
                                              onvalue=ascii_lowercase,
                                              offvalue='')
        self.lower_checkbox.pack(**options_config_single)

        # contains upper alphabet checkbox
        self.upper_checkbox_v = tk.StringVar(value=ascii_uppercase)
        self.upper_checkbox = ttk.Checkbutton(self.key_options,
                                              text="upper A:Z",
                                              variable=self.upper_checkbox_v,
                                              onvalue=ascii_uppercase,
                                              offvalue='')
        self.upper_checkbox.pack(**options_config_single)

        # contains numeric checkbox
        self.numeric_checkbox_v = tk.StringVar(value=digits)
        self.numeric_checkbox = ttk.Checkbutton(self.key_options,
                                                text="numeric 0:9",
                                                variable=self.numeric_checkbox_v,
                                                onvalue=digits,
                                                offvalue='')
        self.numeric_checkbox.pack(**options_config_single)

        # contains special entry
        self.special_entry_v = tk.StringVar(value="!@#$%^&*+=`~?")
        self.special_entry = ttk.Entry(self.key_options,
                                       textvariable=self.special_entry_v)
        self.special_entry.pack(**options_config_single)

        # length label
        self.length_label = ttk.Label(self.key_options,
                                      text="Length:")
        self.length_label.pack(**options_config_double)

        # length spinbox
        self.length_value = tk.IntVar(value=14)
        self.length_spinbox = ttk.Spinbox(self.key_options,
                                          from_=4,
                                          to=30,
                                          textvariable=self.length_value,
                                          wrap=False)
        self.length_spinbox.pack(**options_config_double)

        # begin fetch sequence. requires all widgets to be placed
        self.domain_update()

    def reset_displays(self, domain_field=False, username_field=False, key_field=False):
        """Clears associated display strings, disables widgets below it."""

        if domain_field:
            self.domain_combo.set('')
        if username_field:
            self.username_combo.set('')
            self.username_combo.state(['disabled'])
        if key_field:
            self.key_string.set('')
            self.lower_checkbox_v.set(value=ascii_lowercase)
            self.upper_checkbox_v.set(value=ascii_uppercase)
            self.numeric_checkbox_v.set(value=digits)
            self.special_entry_v.set('!@#$%^&*+=`~?')

            self.key_entry.state(['disabled'])
            self.generate_button.state(['disabled'])
            self.commit_button.state(['disabled'])

            self.key_options.state(['disabled'])
            self.lower_checkbox.state(['disabled'])
            self.upper_checkbox.state(['disabled'])
            self.numeric_checkbox.state(['disabled'])
            self.special_entry.state(['disabled'])
            self.length_label.state(['disabled'])
            self.length_spinbox.state(['disabled'])

    def domain_update(self):
        """Updates Domain combobox list and clears display strings."""

        self.reset_displays(True, True, True)
        self.domain_combo.configure(values=self._keyring.fetch_query())
        self.domain_combo.focus()

    def username_update(self):
        """Updates dates username combobox list and clears username, key displays."""

        domain = self.domain_combo.get()
        self.username_combo.configure(values=self._keyring.fetch_query(domain))
        self.username_combo.state(['!disabled'])

    def key_update(self):
        """Fetches and displays key."""

        domain = self.domain_combo.get()
        username = self.username_combo.get()
        # domain and username have to both contain characters to query for key
        if domain and username:
            key = self._keyring.fetch_query(domain, username)
            if key:
                key = str(key[0])
                self.key_string.set(key)
        # allow for update/new addition regardless of query
        self.key_entry.state(['!disabled'])
        self.generate_button.state(['!disabled'])
        self.commit_button.state(['!disabled'])
        self.key_options.state(['!disabled'])
        self.lower_checkbox.state(['!disabled'])
        self.upper_checkbox.state(['!disabled'])
        self.numeric_checkbox.state(['!disabled'])
        self.special_entry.state(['!disabled'])
        self.length_label.state(['!disabled'])
        self.length_spinbox.state(['!disabled'])

    def selection(self, *args):
        """Event handling for domain/username selection."""
        combobox = None
        for arg in args:
            if type(arg) is tk.Event:
                combobox = arg.widget

        # reset/disable displays when combobox field is empty or changed
        if self.domain_text.get() == '' or combobox is self.domain_combo:
            self.reset_displays(False, True, True)
        if self.username_text.get() == '' or combobox is self.username_combo:
            self.reset_displays(False, False, True)

        # <<ComboboxSelected>> or custom characters entered, query activate displays
        if self.domain_text.get() != '' or combobox is self.domain_combo:
            self.username_update()
        if self.username_text.get() != '' or combobox is self.username_combo:
            self.key_update()

    def generate_new_key(self):
        """Randomly generates a key and displays in key_combobox."""
        print(type(self.length_spinbox.get()))
        length = int(self.length_spinbox.get())
        string_lists = [self.lower_checkbox_v,
                        self.upper_checkbox_v,
                        self.numeric_checkbox_v,
                        self.special_entry_v]
        new_key_builder = []
        all_characters = ''

        for category in string_lists:
            if category.get():
                # add one of each type of mandatory character
                new_key_builder.append(choice(category.get()))
                # build total character set for next stage
                all_characters = all_characters + category.get()
                length -= 1

        # populate remaining length with random char from all_character set
        while length > 0:
            new_key_builder.append(choice(all_characters))
            length -= 1

        # shuffle, join to string, display
        shuffle(new_key_builder)
        new_key = ''.join(new_key_builder)
        self.key_string.set(new_key)

    def commit_key(self):
        """Commits key in key display to db."""

        domain = self.domain_combo.get()
        username = self.username_combo.get()
        key = self.key_entry.get()
        date_updated = time.strftime("%Y-%m-%d %H:%M:%S.000", time.localtime())

        update = (domain, username, key, date_updated)
        self._keyring.update_table(update)

        # clear combobox(es) and update domain query
        self.domain_update()

    def export_txt(self):
        """Calls export function of Keyring to .txt file."""

        self._keyring.export_txt()


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

def make_widgets(self):
    """Adds entry and button to Frame to get profile string."""
    # username entry with Return binding
    entered_string = tk.StringVar()
    profile_entry = ttk.Entry(self, textvariable=entered_string)
    profile_entry.bind(
        '<Return>', lambda event: self.initialize_user(entered_string))
    profile_entry.focus()
    profile_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

    # button
    get_profile_button = ttk.Button(self, text="enter profile")
    get_profile_button['command'] = lambda: self.initialize_user(entered_string)
    get_profile_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)


def initialize_user(self, entered_string):
    """Handler 'enter profile' button clicked or entry <Return> event."""

    # initialize KeyRing object with user string, return if no string
    profile = entered_string.get()
    if not profile:
        return
    keyring = kr.KeyRing(profile)

    # initialize and raise ManagerFrame, terminate ProfileFrame
    ManagerFrame(self._window, profile, keyring).tkraise()
    self.destroy()
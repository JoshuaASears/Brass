import tkinter as tk
from tkinter import ttk
import keyring


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure root window
        self.title('NakedKeyChain')
        self.iconbitmap('./icon/keyring.ico')

        # size and center on screen
        window_width = 500
        window_height = 500
        offset_x = int(self.winfo_screenwidth()/2 - window_width/2)
        offset_y = int(self.winfo_screenheight()/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{offset_x}+{offset_y}')
        self.resizable(False, False)


if __name__ == '__main__':
    app = App()
    frame = MainFrame(app)
    tk.mainloop()

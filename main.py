import tkinter as tk
from scripts import interface


class App(tk.Tk):
    """Root window of application."""

    def __init__(self):
        super().__init__()

        # configure root window
        self.title('Brass')
        self.iconbitmap('Brass.ico')

    def window_size(self, width, height):
        """Takes width and height. Centers application on screen.
        Allows different frame classes to easily adjust size of window."""

        offset_x = int(self.winfo_screenwidth()/2 - width/2)
        offset_y = int(self.winfo_screenheight()/2 - height/2)
        self.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        self.resizable(False, False)


if __name__ == '__main__':
    app = App()
    frame = interface.ProfileFrame(app)
    tk.mainloop()

import tkinter as tk


class ventanaC(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Hola")

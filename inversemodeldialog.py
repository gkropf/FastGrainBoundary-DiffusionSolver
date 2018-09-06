import tkinter as tk

class InverseModelPage(tk.Frame):

    def __init__(self, parent,mainapp):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.config(bg=mainapp.Background1)


        self.label = tk.Label(self, text="Inverse Model")
        self.label.pack(pady=10, padx=10)
        self.config(bg=mainapp.Background1)

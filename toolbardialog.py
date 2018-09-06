import tkinter as tk

class ToolBar(tk.Frame):

    def __init__(self, parent,mainapp):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.config(bg='black')

        fileFrame = tk.Label(self, text='File')
        fileFrame.grid(row=0, column=0, sticky='e')

        viewFrame = tk.Label(self, text='View')
        viewFrame.config(bg='green')
        viewFrame.grid(row=0, column=1, sticky='w')
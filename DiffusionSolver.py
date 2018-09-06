import tkinter as tk
from tkinter import ttk

from forwardmodeldialog import *
from inversemodeldialog import *
from toolbardialog import *


class FastGrainDiffusionApp(tk.Frame):

    Background1 = '#c5ddeb'
    font_inputs = ("Helvetica", 11)
    font_sections = ("Helvetica", 11)
    font_labels = ("ariel", 12, "bold")

    def __init__(self,parent):

        tk.Frame.__init__(self,parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0,weight=1)
        parent.title('tk ##version 2.0')

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        self.maintabs = ttk.Notebook(self)
        self.maintabs.grid(row=1, column=0, sticky='nsew')

        # Add e

        self.page1 = ForwardModelPage(self,FastGrainDiffusionApp)
        self.maintabs.add(self.page1, text='Forward Model')

        self.page2 = InverseModelPage(self,FastGrainDiffusionApp)
        self.maintabs.add(self.page2, text='Inverse Model')

        self.page3 = tk.Frame()
        self.maintabs.add(self.page3, text='Temp History')

        self.toolbar = ToolBar(self,FastGrainDiffusionApp)
        self.toolbar.grid(row=0, column=0, sticky='nsew')















root = tk.Tk()
app = FastGrainDiffusionApp(root)
app.mainloop()


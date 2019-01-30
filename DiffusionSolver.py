import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from forwardmodeldialog import *
from inversemodeldialog import *
from toolbardialog import *


class FastGrainDiffusionApp(tk.Frame):

    def __init__(self,parent):

        tk.Frame.__init__(self,parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0,weight=1)
        parent.title('FGB Model')

        # Set global visual characteristics 
        self.Background1 = '#c5ddeb'
        self.font_inputs = tkFont.Font(family="Helvetica", size=11)
        self.font_sections = tkFont.Font(family="Helvetica", size=11)
        self.font_labels = tkFont.Font(family="monospace", size=11, weight='bold')
        self.font_buttons = tkFont.Font(family="monospace", size=11)
        self.font_message = tkFont.Font(family='monospace', size=11, weight='bold')
        self.font_mono1 = tkFont.Font(family='monospace', size=11)
        self.font_mono2 = tkFont.Font(family='monospace', size=11)
        self.font_mono2.configure(underline=True)
        self.font_inputs2 = tkFont.Font(family="monospace", size=13)
        self.font_large = tkFont.Font(family="monospace", size=16, weight='bold')



        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        self.maintabs = ttk.Notebook(self)
        self.maintabs.grid(row=1, column=0, sticky='nsew')


        self.page1 = ForwardModelPage(self)
        self.maintabs.add(self.page1, text='Forward Model')

        self.page2 = InverseModelPage(self)
        self.maintabs.add(self.page2, text='Inverse Model')

        self.page3 = tk.Frame()
        self.maintabs.add(self.page3, text='Temp History')


        self.toolbar = ToolBar(self)
        root.config(menu=self.toolbar)


root = tk.Tk()
app = FastGrainDiffusionApp(root)
app.mainloop()


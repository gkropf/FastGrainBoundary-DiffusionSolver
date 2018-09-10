import tkinter as tk
from tkinter import filedialog
from numpy import *






class ForwardModelInputs(tk.Frame):

    def loadmodel(self,inversepage,n):

        file_loc = filedialog.askopenfilename(filetypes=(("Model File", ".npz"), ("all files", "*.*")),
                                              defaultextension=".npz")
        if file_loc:
            self.forwardmodels_var[n].set(file_loc)
            npzfile = load(file_loc)
            numminerals = npzfile['arr_0'].shape[1]
            inversepage.set_nummin(n,numminerals)

        print('\n')



    def __init__(self,parent,mainapp):
        tk.Frame.__init__(self,parent)
        self.config(bg=mainapp.Background1)

        #self.grid_columnconfigure(0, weight=1)
        #for i in range(0,5):
        #    self.grid_rowconfigure(i, weight=1)


        tk.Label(self, text='Forward Models', font=mainapp.font_labels,
                 bg=mainapp.Background1).grid(row=0, column=0, padx=(4,0), pady=(4,0))
        tk.Frame(self, width=2, bg='black').grid(row=1, column=1, sticky='ns',
                                                 rowspan=5, padx=(3, 3))


        self.forwardmodels_var=dict()
        self.forwardmodels_lab=dict()

        for i in range(0,5):
            self.forwardmodels_var[i]=tk.StringVar(self)
            self.forwardmodels_var[i].set('')

            self.forwardmodels_lab[i]=tk.Label(self, textvariable=self.forwardmodels_var[i],
                                               anchor='w', font=mainapp.font_inputs)
            self.forwardmodels_lab[i].configure(bg='white', relief='sunken', height=1,
                                                width=25)
            self.forwardmodels_lab[i].grid(row=i+1, column=0, sticky='nsew', padx=(4,0))

            self.forwardmodels_lab[i].bind("<Enter>", lambda event, i=i, h=self.forwardmodels_lab[i]:
                                       h.configure(bg='#dbdbdb'))
            self.forwardmodels_lab[i].bind("<Leave>", lambda event, i=i, h=self.forwardmodels_lab[i]:
                                       h.configure(bg='white'))
            self.forwardmodels_lab[i].bind("<Button-1>", lambda event, i=i: self.loadmodel(parent,i))



    print('\n')


class ErrorFileInputs(tk.Frame):

    def __init__(self, parent, mainapp):
        tk.Frame.__init__(self, parent)
        self.config(bg=mainapp.Background1)

        for i in range(0,5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(0,8):
            self.grid_columnconfigure(j, weight=1)


        # Create error file inputs
        self.errfile_var=dict()
        self.errfile_lab=dict()

        for j in range(0, 8):
            tk.Label(self, text='Mineral '+str(j+1), font=mainapp.font_labels,
                     bg=mainapp.Background1).grid(row=0, column=j, pady=(4, 0))

            for i in range(0, 5):

                self.errfile_var[(i,j)]=tk.StringVar(self)
                self.errfile_var[(i,j)].set('')

                self.errfile_lab[(i,j)]=tk.Label(self, textvariable=self.errfile_var[(i,j)],
                                                 anchor='w', font=mainapp.font_inputs)
                self.errfile_lab[(i,j)].configure(bg='#c9c7c7', relief='sunken', width=15)
                self.errfile_lab[(i,j)].grid(row=i+1, column=j, sticky='nsew', padx=(0,4*(j==7)))










        self.bob = tk.StringVar(self)
        self.bob.set('a')


    def loaderror(self, inversepage,i,j):
        print(self.bob.get())
        print((i,j))

        print('')















class InverseModelPage(tk.Frame):


    def set_nummin(self,i,nmin):

        for j in range(0,nmin):
            self.errorfileframe.errfile_lab[(i, j)].configure(bg='white')
            self.errorfileframe.errfile_lab[(i, j)].bind("<Enter>", lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
            h.configure(bg='lightgrey'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Leave>", lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
            h.configure(bg='white'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Button-1>", lambda event, i=i, j=j:
            self.errorfileframe.loaderror(self, i, j))


        print('\n')


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #self.grid_columnconfigure(0, weight=100)
        #self.grid_columnconfigure(2, weight=400)
        self.config(bg=parent.Background1)


        self.label = tk.Label(self, text="Inverse Model")
        self.config(bg=parent.Background1)

        self.forwardmodelframe = ForwardModelInputs(self,parent)
        self.forwardmodelframe.grid(row=0, column=0, sticky='nsew')

        self.errorfileframe = ErrorFileInputs(self,parent)
        self.errorfileframe.grid(row=0, column=1, sticky='nsew')


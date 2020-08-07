import tkinter as tk
from tkinter import filedialog
from numpy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas
import glob


class InverseProgressWindow(tk.Toplevel):
    def __init__(self,mainapp,init_soln,init_sse,init_aLm):
        tk.Toplevel.__init__(self, mainapp)
        self.config(bg=mainapp.Background1)
        self.title('Inverse solver progress window')

        # Make current solutions plot
        frame1 = tk.Frame(self, relief='solid', borderwidth=3)
        self.fig1 = Figure()
        self.fig1.suptitle('Inverse Solution', weight='bold')

        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (m.y.)')
        self.ax1.set_ylabel('Temperature (C')

        self.line11 = self.ax1.plot(init_soln[:,0],init_soln[:,1],'b-', label='Current')[0]
        self.line12 = self.ax1.plot(init_soln[:,0],init_soln[:,1],'bs')[0]
        self.line13 = self.ax1.plot(init_soln[:,0],init_soln[:,1],'k--', label='Initial')
        self.ax1.legend()

        self.canvas1 = FigureCanvasTkAgg(self.fig1,frame1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas1._tkcanvas.pack(side='top', fill='both', expand=1)
        frame1.grid(row=2, column=0, padx=(10,10), pady=(5,10))

        # Make bar plot of objective values
        frame2 = tk.Frame(self, relief='solid', borderwidth=3)
        self.fig2 = Figure()
        self.fig2.suptitle('Model Fit', weight='bold')

        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlabel('LM Iteration')
        self.bar1 = self.ax2.bar(range(30),[init_sse+init_aLm]+29*[0],color='#373f47',
                                  label='Total objective value')
        self.bar2 = self.ax2.bar(range(30),[init_sse]+29*[0],color='#6c91c2',
                                  label='Weighted SSE')
        self.ax2.legend()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, frame2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.canvas2._tkcanvas.pack(side='top', fill='both', expand=1)
        frame2.grid(row=2, column=1, padx=(10,10), pady=(5,10))

        # Add text labels for current initial solution and derivative
        self.calc_var = tk.StringVar(self)
        self.calc_var.set("")
        self.calc_lab = tk.Label(self, textvariable=self.calc_var, font=mainapp.font_sections,
                                 bg=mainapp.Background1)
        self.calc_lab.grid(row=1, column=0, sticky='w', pady=(5,0), padx=(8,0))

        self.init_var = tk.StringVar(self)
        self.init_var.set("")
        self.init_lab = tk.Label(self, textvariable=self.init_var, font=mainapp.font_large,
                                 bg=mainapp.Background1)
        self.init_lab.grid(row=0, column=0, columnspan=2, sticky='nswe', pady=(15,15))

        self.update()


class InitialSolutions(tk.Frame):

    def loaddir(self,inversepage):
        dir_loc=tk.filedialog.askdirectory()+'/'
        self.folder_var.set(dir_loc)
        inversepage.set_numinitial(dir_loc)



    def __init__(self,parent,mainapp):
        tk.Frame.__init__(self, parent)
        self.config(bg=mainapp.Background1)

        self.head=tk.Label(self,text='Initial Solutions',bg=mainapp.Background1, font=mainapp.font_labels)
        self.head.grid(row=0, column=0, sticky='w', pady=(15,5), padx=(4,0))

        #make input folder selector
        self.folder_var = tk.StringVar(self)
        self.folder_var.set("Directory Location")

        self.folder_lab = tk.Label(self, textvariable=self.folder_var,
                                             anchor='w', font=mainapp.font_inputs)
        self.folder_lab.configure(bg='white', relief='sunken', height=1,
                                            width=110)
        self.folder_lab.grid(row=1, column=0, padx=(10, 0), pady=(0,4))

        self.folder_lab.bind("<Enter>", lambda event: self.folder_lab.configure(bg='#dbdbdb'))
        self.folder_lab.bind("<Leave>", lambda event: self.folder_lab.configure(bg='white'))
        self.folder_lab.bind("<Button-1>", lambda event: self.loaddir(parent))

        #make check marks for each possible solution
        self.container1=tk.Frame(self)
        self.container1.config(bg=mainapp.Background1)
        self.container1.grid(row=3, column=0)

        self.initial_vars=dict()
        self.initial_check=dict()
        self.initial_labs=dict()
        for i in range(0,6*5):
            self.initial_vars[i]=tk.IntVar(self)
            self.initial_labs[i]=tk.StringVar(self)
            self.initial_check[i] = tk.Checkbutton(self.container1, textvariable=self.initial_labs[i],
                                                font=mainapp.font_buttons,
                                                bg=mainapp.Background1,
                                                variable=self.initial_vars[i])
            self.initial_check[i].grid(row=int(i/6)+3, column=i%6, sticky='we', padx=(10,10), pady=(0,4*(int(i/6)==4)))
            self.initial_check[i].grid_remove()

        # make selection of C code option and smooth parameter
        self.container2=tk.Frame(self)
        self.container2.config(bg=mainapp.Background1)
        self.container2.grid(row=1, column=1, padx=(60,5))

        self.useC_var=tk.IntVar()
        self.useC_check=tk.Checkbutton(self.container2, text='Use Compiled C Code',
                                                font=mainapp.font_buttons,
                                                bg=mainapp.Background1,
                                                variable=self.useC_var)
        self.useC_check.grid(row=0, column=0, sticky='n')






    print('\n')


class ForwardModelInputs(tk.Frame):

    def loadmodel(self,inversepage,n):

        file_loc = filedialog.askopenfilename(filetypes=(("Model File", ".txt"), ("all files", "*.*")),
                                              defaultextension=".txt")
        if file_loc:
            self.forwardmodels_var[n].set(file_loc)
            inversepage.forwardmods[n]=dict()
            f=open(file_loc,'r')

            # get number of minerals from first line of file
            num_min=f.readline().strip().split(',')[1]
            inversepage.forwardmods[n]['NumMinerals']=num_min

            # read in all other lines as a dictionary
            for i in range(0,7+int(num_min)*11-1):
                line=f.readline().strip()
                (key,val)=line.split(',')
                inversepage.forwardmods[n][key]=val

            inversepage.set_nummin(n,int(num_min))

        print('\n')



    def __init__(self,parent,mainapp):
        tk.Frame.__init__(self,parent)
        self.config(bg=mainapp.Background1)

        tk.Label(self, text='Model Parameters', font=mainapp.font_labels,
                 bg=mainapp.Background1).grid(row=0, column=1, padx=(4,0), pady=(4,0))
        tk.Frame(self, width=2, bg='black').grid(row=1, column=2, sticky='ns',
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
            self.forwardmodels_lab[i].grid(row=i+1, column=1, sticky='nsew', padx=(4,0))

            self.forwardmodels_lab[i].bind("<Enter>", lambda event, i=i, h=self.forwardmodels_lab[i]:
                                       h.configure(bg='#dbdbdb'))
            self.forwardmodels_lab[i].bind("<Leave>", lambda event, i=i, h=self.forwardmodels_lab[i]:
                                       h.configure(bg='white'))
            self.forwardmodels_lab[i].bind("<Button-1>", lambda event, i=i: self.loadmodel(parent,i))


        # Create line erase buttons
        for i in range(0,5):
            self.delline=tk.Label(self, text='X', bg=mainapp.Background1, relief='raised')
            self.delline.grid(row=i+1, column=0, padx=(4,0))
            self.delline.bind("<Enter>", lambda event, h=self.delline:
                                                h.configure(bg='red'))
            self.delline.bind("<Leave>", lambda event, h=self.delline:
            h.configure(bg=mainapp.Background1))
            self.delline.bind("<Button-1>", lambda event, i=i: parent.deleteline(i))


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
                self.errfile_lab[(i,j)].grid(row=i+1, column=j, sticky='nsew', padx=(0,5*(j==7)))



    def loaderror(self, inversepage,i,j):

        curr_loc=self.errfile_var[(i,j)].get()
        file_loc = filedialog.askopenfilename(filetypes=(("Model File", ".txt"), ("all files", "*.*")),
                                              defaultextension=".txt", initialdir=curr_loc)
        if file_loc:
            self.errfile_var[(i,j)].set(file_loc)


        print('')


class InverseModelPage(tk.Frame):

    def create_progwind(self,mainapp,init_sol,init_sse,init_aLm):
        self.progwind = InverseProgressWindow(mainapp,init_sol,init_sse,init_aLm)


    def set_numinitial(self,dir_loc):
        list_files=sort(glob.glob(dir_loc+'*.txt'))
        n=len(dir_loc)
        self.num_initials=min(len(list_files),30)


        for i in range(0,self.num_initials):
            self.initsolutions.initial_labs[i].set(list_files[i][n:])
            self.initsolutions.initial_check[i].grid()

        for i in range(self.num_initials,30):
            self.initsolutions.initial_check[i].grid_remove()


    def set_nummin(self,i,nmin):

        for j in range(0,nmin):
            self.errorfileframe.errfile_lab[(i, j)].configure(bg='white')
            self.errorfileframe.errfile_lab[(i, j)].bind("<Enter>", lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
            h.configure(bg='lightgrey'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Leave>", lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
            h.configure(bg='white'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Button-1>", lambda event, i=i, j=j:
            self.errorfileframe.loaderror(self, i, j))

        for j in range(nmin,8):
            self.errorfileframe.errfile_lab[(i, j)].configure(bg='#c9c7c7')
            self.errorfileframe.errfile_lab[(i, j)].bind("<Enter>",
                                                         lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
                                                         h.configure(bg='#c9c7c7'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Leave>",
                                                         lambda event, i=i, h=self.errorfileframe.errfile_lab[(i, j)]:
                                                         h.configure(bg='#c9c7c7'))
            self.errorfileframe.errfile_lab[(i, j)].bind("<Button-1>", lambda event: 1+1)


        print('\n')


    def deleteline(self,n):

        self.forwardmodelframe.forwardmodels_var[n].set('')
        self.set_nummin(n,0)
        for j in range(0,8):
            self.errorfileframe.errfile_var[(n,j)].set('')



    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #self.grid_columnconfigure(0, weight=100)
        #self.grid_columnconfigure(2, weight=400)
        self.num_initials=0
        self.config(bg=parent.Background1)


        self.label = tk.Label(self, text="Inverse Model")
        self.config(bg=parent.Background1)

        self.forwardmodelframe = ForwardModelInputs(self,parent)
        self.forwardmodelframe.grid(row=0, column=0, sticky='nsew')

        self.errorfileframe = ErrorFileInputs(self,parent)
        self.errorfileframe.grid(row=0, column=1, sticky='nsew')

        tk.Label(self, text='-----------------', bg=parent.Background1).grid(row=1, columnspan=2)

        self.initsolutions = InitialSolutions(self,parent)
        self.initsolutions.grid(row=1, column=0, columnspan=2, sticky='nswe')

        # make list of dictionaries to store forward models in
        self.forwardmods=dict()


import tkinter as tk
import pandas
from numpy import *
from tkinter import filedialog
import matplotlib.pyplot as plt




class ModelCharFrame(tk.LabelFrame):

    def __init__(self,parent,mainapp):
        tk.LabelFrame.__init__(self, parent)
        self.config(bg=mainapp.Background1)
        self.config(text='Global Model Characteristics')
        self.config(font=mainapp.font_sections)

        # Construct model characteristics section elements.
        self.numminerals_var = tk.IntVar(self)
        self.numminerals_var.set(2)
        self.numminerals_label = tk.Label(self, text="Minerals",
                                          font=mainapp.font_labels,
                                          bg=mainapp.Background1)
        self.numminerals_input = tk.OptionMenu(self, self.numminerals_var, "2", "3",
                                               "4", "5", "6", "7", "8", command=parent.setnummin)
        self.numminerals_input.config(width=6, font=mainapp.font_inputs,
                                      relief='sunken', bd=1, bg='white', highlightthickness=0)

        self.coolingtype_var = tk.StringVar(self)
        self.coolingtype_var.set("Linear")
        self.coolingtype_label = tk.Label(self, text="Cooling Type",
                                          font=mainapp.font_labels,
                                          bg=mainapp.Background1)
        self.coolingtype_input = tk.OptionMenu(self, self.coolingtype_var, "Linear",
                                          "Inverse", "Custom", command=parent.getcoolingfile)
        self.coolingtype_input.config(width=6, font=mainapp.font_inputs,
                                      relief='sunken', bd=1, bg='white', highlightthickness=0)

        self.coolinghistory = tk.StringVar(self)
        self.coolinghistory.set('')

        self.wholerock_var = tk.StringVar(self)
        self.wholerock_var.set("")
        self.wholerock_label = tk.Label(self, text="Whole Rock",
                                        font=mainapp.font_labels,
                                        bg=mainapp.Background1)
        self.wholerock_input = tk.Entry(self, textvariable=self.wholerock_var)
        self.wholerock_input.config(width=6, font=mainapp.font_inputs)

        self.modelduration_var = tk.StringVar(self)
        self.modelduration_var.set("")
        self.modelduration_label = tk.Label(self, text="Model Duration",
                                            font=mainapp.font_labels,
                                            bg=mainapp.Background1)
        self.modelduration_input = tk.Entry(self, textvariable=self.modelduration_var)
        self.modelduration_input.config(width=6, font=mainapp.font_inputs)

        self.starttemp_var = tk.StringVar(self)
        self.starttemp_var.set("")
        self.starttemp_label = tk.Label(self, text="Starting Temp",
                                        font=mainapp.font_labels,
                                        bg=mainapp.Background1)
        self.starttemp_input = tk.Entry(self, textvariable=self.starttemp_var)
        self.starttemp_input.config(width=6, font=mainapp.font_inputs)

        self.timestep_var = tk.StringVar(self)
        self.timestep_var.set("")
        self.timestep_label = tk.Label(self, text="Time Step",
                                       font=mainapp.font_labels,
                                       bg=mainapp.Background1)
        self.timestep_input = tk.Entry(self, textvariable=self.timestep_var)
        self.timestep_input.config(width=6, font=mainapp.font_inputs)

        self.endtemp_var = tk.StringVar(self)
        self.endtemp_var.set("")
        self.endtemp_label = tk.Label(self, text="End Temp",
                                      font=mainapp.font_labels,
                                      bg=mainapp.Background1)
        self.endtemp_input = tk.Entry(self, textvariable=self.endtemp_var)
        self.endtemp_input.config(width=6, font=mainapp.font_inputs)


        # Place all model characteristics elements.
        self.numminerals_label.grid(row=0, column=1, sticky='nse', padx=(5,5), pady=(7,1.5))
        self.numminerals_input.grid(row=0, column=2, stick='nswe', padx=(5,10), pady=(7,1.5))

        self.coolingtype_label.grid(row=1, column=1, sticky='nse', padx=(5,5), pady=(1.5,1.5))
        self.coolingtype_input.grid(row=1, column=2, sticky='nswe', padx=(5,10), pady=(1.5,1.5))

        self.wholerock_label.grid(row=2, column=1, sticky='nse', padx=(5,5),pady=(1.5,4))
        self.wholerock_input.grid(row=2, column=2, sticky='nswe', padx=(5,10), pady=(1.5,4))

        self.modelduration_label.grid(row=0, column=3, sticky='nse', padx=(5,5), pady=(4,1.5))
        self.modelduration_input.grid(row=0, column=4, sticky='nswe', padx=(5,5), pady=(4,1.5))

        self.starttemp_label.grid(row=1, column=3, sticky='nse', padx=(5,5), pady=(1.5,1.5))
        self.starttemp_input.grid(row=1, column=4, sticky='nswe', padx=(5,5), pady=(1.5,1.5))

        self.timestep_label.grid(row=0, column=5, sticky='nse', padx=(5,5), pady=(7,1.5))
        self.timestep_input.grid(row=0, column=6, sticky='nswe', padx=(5,5), pady=(7,1.5))

        self.endtemp_label.grid(row=1, column=5, sticky='nse', padx=(5,5), pady=(1.5,1.5))
        self.endtemp_input.grid(row=1, column=6, sticky='nswe', padx=(5,5), pady=(1.5,1.5))


class RockCharFrame(tk.LabelFrame):

    def __init__(self,parent,mainapp):
        tk.LabelFrame.__init__(self, parent)
        self.config(bg=mainapp.Background1)
        self.config(text='Mineral Properties')
        self.config(font=mainapp.font_sections)
        tk.Frame(self).grid(row=20,column=0,columnspan=4,pady=(0,5))


        c_labels=['Monitor','Sample 2', 'Sample 3','Sample 4', 'Sample 5', 'Sample 6', 'Sample 7','Sample 8']
        self.column_labels=dict()
        for i in range(0,8):
            self.column_labels[i]=tk.Label(self, text=c_labels[i],
                                           font=mainapp.font_labels,
                                           bg=mainapp.Background1)


        self.mineralname_label = tk.Label(self, text="Name",
                                          font=mainapp.font_labels,
                                          bg=mainapp.Background1)
        self.mineralname_label.grid(row=0,column=1)
        self.mineralname_vars=dict()
        self.mineralname_inputs=dict()
        for i in range(0,8):
            self.mineralname_vars[i] = tk.StringVar(parent)
            self.mineralname_vars[i].set("")
            self.mineralname_inputs[i] = tk.Entry(self, textvariable=self.mineralname_vars[i])
            self.mineralname_inputs[i].config(width=8, font=mainapp.font_inputs)


        self.mineralmode_label = tk.Label(self, text="Mode",
                                          font=mainapp.font_labels,
                                          bg=mainapp.Background1)
        self.mineralmode_label.grid(row=0,column=2)
        self.mineralmode_vars=dict()
        self.mineralmode_inputs=dict()
        for i in range(0,8):
            self.mineralmode_vars[i] = tk.StringVar(parent)
            self.mineralmode_vars[i].set("")
            self.mineralmode_inputs[i] = tk.Entry(self, textvariable=self.mineralmode_vars[i])
            self.mineralmode_inputs[i].config(width=6, font=mainapp.font_inputs)


        self.mineralshape_label = tk.Label(self, text="Shape",
                                          font=mainapp.font_labels,
                                           bg=mainapp.Background1)
        self.mineralshape_label.grid(row=0,column=3)
        self.mineralshape_vars=dict()
        self.mineralshape_inputs=dict()
        for i in range(0,8):
            self.mineralshape_vars[i] = tk.StringVar(parent)
            self.mineralshape_vars[i].set("")
            self.mineralshape_inputs[i] = tk.OptionMenu(self, self.mineralshape_vars[i],
                                                        "Slab","Spherical")
            self.mineralshape_inputs[i].config(width=6, font=mainapp.font_inputs,
                                               relief='sunken', bd=1, bg='white', highlightthickness=0)
            self.mineralshape_vars[i].set("Slab")


        self.mineralrad_label = tk.Label(self, text="R",
                                         font=mainapp.font_labels,
                                         bg=mainapp.Background1)
        self.mineralrad_label.grid(row=0,column=4)
        self.mineralrad_vars=dict()
        self.mineralrad_inputs=dict()
        for i in range(0,8):
            self.mineralrad_vars[i] = tk.StringVar(parent)
            self.mineralrad_vars[i].set("")
            self.mineralrad_inputs[i] = tk.Entry(self, textvariable=self.mineralrad_vars[i])
            self.mineralrad_inputs[i].config(width=6, font=mainapp.font_inputs)


        self.mineralwid_label = tk.Label(self, text="W",
                                         font=mainapp.font_labels,
                                         bg=mainapp.Background1)
        self.mineralwid_label.grid(row=0,column=5)
        self.mineralwid_vars=dict()
        self.mineralwid_inputs=dict()
        for i in range(0,8):
            self.mineralwid_vars[i] = tk.StringVar(parent)
            self.mineralwid_vars[i].set("")
            self.mineralwid_inputs[i] = tk.Entry(self, textvariable=self.mineralwid_vars[i])
            self.mineralwid_inputs[i].config(width=6, font=mainapp.font_inputs)


        self.mineralfracA_label = tk.Label(self, text="A-frac",
                                           font=mainapp.font_labels,
                                           bg=mainapp.Background1)

        self.mineralfracA_label.grid(row=0,column=6)
        self.mineralfracA_vars=dict()
        self.mineralfracA_inputs=dict()
        for i in range(0,8):
            self.mineralfracA_vars[i] = tk.StringVar(parent)
            self.mineralfracA_vars[i].set(""+'0.0'*(i==0))
            self.mineralfracA_inputs[i] = tk.Entry(self, textvariable=self.mineralfracA_vars[i])
            self.mineralfracA_inputs[i].config(width=6, font=mainapp.font_inputs, state='disabled')

        self.mineralfracB_label = tk.Label(self, text="B-frac",
                                           font=mainapp.font_labels,
                                           bg=mainapp.Background1)
        self.mineralfracB_label.grid(row=0,column=7)
        self.mineralfracB_vars=dict()
        self.mineralfracB_inputs=dict()
        for i in range(0,8):
            self.mineralfracB_vars[i] = tk.StringVar(parent)
            self.mineralfracB_vars[i].set(""+'0.0'*(i==0))
            self.mineralfracB_inputs[i] = tk.Entry(self, textvariable=self.mineralfracB_vars[i])
            self.mineralfracB_inputs[i].config(width=6, font=mainapp.font_inputs, state='disabled')

        self.mineralfracC_label = tk.Label(self, text="C-frac",
                                           font=mainapp.font_labels,
                                           bg=mainapp.Background1)
        self.mineralfracC_label.grid(row=0,column=8)
        self.mineralfracC_vars=dict()
        self.mineralfracC_inputs=dict()
        for i in range(0,8):
            self.mineralfracC_vars[i] = tk.StringVar(parent)
            self.mineralfracC_vars[i].set(""+'0.0'*(i==0))
            self.mineralfracC_inputs[i] = tk.Entry(self, textvariable=self.mineralfracC_vars[i])
            self.mineralfracC_inputs[i].config(width=6, font=mainapp.font_inputs, state='disabled')

        self.fracsearch=dict()
        for i in range(1,8):
            self.fracsearch[i]=tk.Button(self, text='Frac'+str(i+1), command=lambda i=i:
            FracValueSearch(parent,mainapp,i))
            self.fracsearch[i].config(font=mainapp.font_buttons)


        self.diffparam1_label=tk.Label(self, text='D0',
                                       font=mainapp.font_labels,
                                       bg=mainapp.Background1)
        self.diffparam2_label=tk.Label(self, text='Q',
                                       font=mainapp.font_labels,
                                       bg=mainapp.Background1)
        self.diffparam1_label.grid(row=0, column=10)
        self.diffparam2_label.grid(row=0, column=11)

        self.diffparam1_vars=dict()
        self.diffparam2_vars=dict()
        self.diffparam1_input=dict()
        self.diffparam2_input=dict()

        for i in range(0,8):
            self.diffparam1_vars[i]=tk.StringVar(parent)
            self.diffparam1_vars[i].set("")
            self.diffparam2_vars[i]=tk.StringVar(parent)
            self.diffparam2_vars[i].set("")

            self.diffparam1_input[i]=tk.Entry(self, textvariable=self.diffparam1_vars[i],
                                              font=mainapp.font_inputs, state='disabled',
                                              width=6)
            self.diffparam2_input[i]=tk.Entry(self, textvariable=self.diffparam2_vars[i],
                                              font=mainapp.font_inputs, state='disabled',
                                              width=6)

        
        self.diffsearch=dict()
        for i in range(0,8):
            self.diffsearch[i]=tk.Button(self, text='Diff'+str(i+1), command=lambda i=i:
            DiffValueSearch(parent,mainapp,i))
            self.diffsearch[i].config(font=mainapp.font_buttons)

        self.oxcon_label=tk.Label(self, text='Oxcon',
                                  font=mainapp.font_labels,
                                  bg=mainapp.Background1)
        self.oxcon_label.grid(row=0, column=13)
        self.oxcon_vars=dict()
        self.oxcon_inputs=dict()
        for i in range(0,8):
            self.oxcon_vars[i]=tk.StringVar(parent)
            self.oxcon_vars[i].set("")

            self.oxcon_inputs[i]=tk.Entry(self, textvariable=self.oxcon_vars[i],
                                          font=mainapp.font_inputs, width=6)



class GraphingFrame(tk.LabelFrame):

    def __init__(self,parent,mainapp):
        tk.LabelFrame.__init__(self, parent)
        self.config(bg=mainapp.Background1)
        self.config(text='Graphing Options')
        self.config(font=mainapp.font_sections)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.plotsingle_chkvar=dict()
        self.plotsingle_check=dict()
        self.plotsingle_var=dict()
        self.plotsingle_input=dict()
        for i in range(0,8):
            self.plotsingle_chkvar[i]=tk.IntVar(parent)
            self.plotsingle_check[i]=tk.Checkbutton(self, text='Plot Mineral '+str(i+1),
                                                 font=mainapp.font_labels,
                                                 bg=mainapp.Background1,
                                                 variable=self.plotsingle_chkvar[i])
            self.plotsingle_var[i]=tk.StringVar(parent)
            self.plotsingle_input[i]=tk.Entry(self, textvariable=self.plotsingle_var[i],
                                              font=mainapp.font_inputs)

        self.plotall_chkvar=tk.IntVar(parent)
        self.plotall_check=tk.Checkbutton(self, text='Plot All',
                                          font=mainapp.font_labels,
                                          bg = mainapp.Background1,
                                          variable=self.plotall_chkvar,
                                          state='disabled')
        self.plotall_check.grid(row=9, column=0, stick='nsw', padx=(5,0))
        self.plotall_var=tk.StringVar(parent)
        self.plotall_input=tk.Entry(self, textvariable=self.plotall_var,
                                    font=mainapp.font_inputs)
        self.plotall_input.grid(row=10, column=0, sticky='nsw', padx=(11,0))

        self.plot=tk.Button(self, text='Produce Plots', font=mainapp.font_buttons,
                            command=lambda: PlotGraphs(parent))
        self.plot.grid(row=10, column=1, sticky='nsw')


def FracValueSearch(forwardpage, mainapp, but_num):

    # Create actual search function that finds path given two nodes and two lists of nodes.
    # This function will create edges from the two lists of nodes and then find shortest path.

    def find_path(list1, list2, node1, node2):

        # Find unique connection points.
        n = len(list1)
        edges = list(set((a, b) if a < b else (b, a) for a, b in zip(list1, list2)))

        # Initialize sets
        checked = set([])
        work_chains = [[node1]]
        final_path = []

        # Perform loops for Breadth-First vector style search algorithm
        while len(work_chains) > 0:
            cchain = work_chains[0]
            cnode = cchain[-1]
            checked = checked.union([cnode])
            nextsteps = list(set([x for y, x in edges if y == cnode and x != y] + [x for x, y in edges if
                                                                                   y == cnode and x != y]) - checked)
            del work_chains[0]
            for k in range(0, len(nextsteps)):
                if nextsteps[k] == node2:
                    final_path = cchain + [node2]
                    checked = checked.union([nextsteps[k]])
                else:
                    checked = checked.union([nextsteps[k]])
                    work_chains.append(cchain + [nextsteps[k]])

        # Start complete search (find all versions of edges)
        all_steps = []
        for k in range(0, len(final_path) - 1):
            min1 = final_path[k]
            min2 = final_path[k + 1]
            pairs = [(x, y) for x, y in zip(list1, list2)]
            poss_steps = [i for i in range(0, n) if (min1, min2) == pairs[i]]
            poss_steps = poss_steps + [-i for i in range(0, n) if (min2, min1) == pairs[i]]
            all_steps.append(poss_steps)

        return all_steps

    # This function will be called after every decision the user makes and appropriately
    # Creates all the window buttons and options

    def create_menus(fracdata,node1,node2):

        list1=[x[1] for x in fracdata]
        list2=[x[2] for x in fracdata]
        path=find_path(list1,list2,node1,node2)
        print(path)

        # clear all previous elements so new window can be created
        for child in mainwin.winfo_children():
            child.destroy()

        #create frame to place choose and manual
        useorenter=tk.Frame(mainwin, bg=mainapp.Background1)

        # used when table entries can't be found and allows manual entry
        def enter_manual(num):
            forwardpage.rockcharframe.mineralfracA_inputs[num].config(state='normal')
            forwardpage.rockcharframe.mineralfracB_inputs[num].config(state='normal')
            forwardpage.rockcharframe.mineralfracC_inputs[num].config(state='normal')
            mainwin.destroy()

        #place manual button
        Man=tk.Button(useorenter, text="Enter Manually", relief="groove",
                      font=mainapp.font_buttons, bg=mainapp.Background1)
        Man.bind('<Button-1>', lambda event: enter_manual(but_num))
        Man.grid(row=0, column=2, pady=(0,10))
        useorenter.grid(row=1,column=2)

        # check that there is a valid path
        if len(path) < 1:
            direc = tk.Label(mainwin, text='There does not exist any remaining path '
                                           'of studies that can link this mineral to your monitor.',
                             font=mainapp.font_message)
            direc.config(font=mainapp.font_message, bg=mainapp.Background1)
            direc.grid(row=0, column=2, padx=(10, 10), pady=(10, 10))
            return
        else:
            direc = tk.Label(mainwin, text='I have the following conversions available for mineral --> monitor',
                             font=mainapp.font_message)
            direc.config(font=mainapp.font_message, bg=mainapp.Background1)
            direc.grid(row=0, column=1, pady=(0, 0), columnspan=1)
            sep_top = tk.Label(mainwin, text="-" * 66)
            sep_top.config(font=mainapp.font_message, bg=mainapp.Background1)
            sep_top.grid(row=1, column=1, columnspan=1, pady=(0, 10))

        #create step locations and then flatten path list
        allpaths=path
        pathssize=[len(x) for x in allpaths]
        path=[x for y in path for x in y]
        n=len(path)
        m=len(allpaths)

        #swap any names and change sign of A,b,c values for negative path numbers
        for k in path:
            if k<0:
                k=abs(k)
                fracdata[k][1:3]=fracdata[k][2:0:-1]
                fracdata[k][7:10]=[str(-1*float(x)) for x in fracdata[k][7:10]]
                fracdata[k][3]=fracdata[k][3].split('-')[1]+'-'+fracdata[k][3].split('-')[0]
        path=[abs(x) for x in path] #make all pos now that table has been adjusted

        #create nice-looking equal length strings for display
        path=[0]+path
        opt=['' for x in path]
        optlist=[3,7,8,9,10,4]
        for k in optlist:
                #place approp white space inbetween
                optadd=[fracdata[abs(x)][k] for x in path]
                lengths=[len(x) for x in opt]
                maxl=max(lengths)+1+2*(k>1)
                opt = [opt[x] + ' ' * (maxl - len(opt[x])) + optadd[x] for x in range(0, len(opt))]

                #add space after all placed
                if k==optlist[-1]:
                        lengths=[len(x) for x in opt]
                        maxl=max(lengths)+1
                        opt=[opt[x]+' '*(maxl-len(opt[x])) for x in range(0,len(opt))]

        #create vector to hold choices for each mineral
        choices=zeros(len(allpaths))-1

        #functions to handle choosing and colver of hover
        def lock_choice(jump,jumpchoice):
                if choices[jump]>-1:
                     unlock_choice(jump,int(choices[jump]))
                path_opt[jump][jumpchoice].unbind('<Leave>')
                path_opt[jump][jumpchoice].config(bg='#A0A0A0')
                path_opt[jump][jumpchoice].bind('<Button-1>', lambda event, i=jump, j=jumpchoice: unlock_choice(i,j))
                choices[jump]=jumpchoice
                if (choices>-1).all():
                     fin_but[1].config(state='normal')

        def unlock_choice(jump,jumpchoice):
                choices[jump]=-1
                fin_but[1].config(state='disabled')
                path_opt[jump][jumpchoice].bind('<Leave>', lambda event, i=jump, j=jumpchoice: change_back(i,j))
                path_opt[jump][jumpchoice].bind('<Button-1>', lambda event, i=jump, j=jumpchoice: lock_choice(i,j))
                path_opt[jump][jumpchoice].config(bg=mainapp.Background1)

        def change_to(jump,jumpchoice):
                path_opt[jump][jumpchoice].config(bg='#A0A0A0')

        def change_back(jump,jumpchoice):
                path_opt[jump][jumpchoice].config(bg=mainapp.Background1)

        def notes_look(jump,jumpchoice):
             notes_but[jump][jumpchoice].config(relief="sunken")
             notes_win=tk.Toplevel()
             notes_win.config(bg=mainapp.Background1)
             curr_notes=fracdata[allpaths[jump][jumpchoice]][11]
             T=tk.Message(notes_win, text=curr_notes.replace('^',','), width=600)
             T.config(bg=mainapp.Background1, font=mainapp.font_mono1)
             T.grid(row=0, column=0, padx=(8,8), pady=(8,8))

        def unclick_note(jump,jumpchoice):
             notes_but[jump][jumpchoice].config(relief="groove")

        def change_note_to(jump,jumpchoice):
             notes_but[jump][jumpchoice].config(bg='#ececec')

        def change_note_back(jump,jumpchoice):
             notes_but[jump][jumpchoice].config(bg=mainapp.Background1)

        #create all buttons (as Labels so binds can be manually controlled and updated without .destroy())
        path_opt=dict()
        step_lab=dict()
        rem_checks=dict()
        Rem_checks=dict()
        notes_but=dict()

        rowtrack = 3
        for jump in range(0, m):
            # create label for current step
            step_lab[jump] = tk.Label(mainwin, text=fracdata[abs(allpaths[jump][0])][1] + ' --> ' +
                                      fracdata[abs(allpaths[jump][0])][2], font=mainapp.font_labels)
            step_lab[jump].grid(row=rowtrack, column=1, sticky='w', pady=(10,0))
            step_lab[jump].config(bg=mainapp.Background1)
            rowtrack = rowtrack + 1

            # create buttons for each option for current step
            path_opt[jump] = dict()
            rem_checks[jump] = dict()
            Rem_checks[jump] = dict()
            notes_but[jump] = dict()
            for jumpchoice in range(0, pathssize[jump]):
                # create checkmarks for delete buttons
                rem_checks[jump][jumpchoice] = tk.IntVar(mainwin)
                rem_checks[jump][jumpchoice].set(0)
                Rem_checks[jump][jumpchoice] = tk.Checkbutton(mainwin, text="", bg=mainapp.Background1,
                                                           variable=rem_checks[jump][jumpchoice])
                Rem_checks[jump][jumpchoice].grid(row=rowtrack, column=0)

                # create main button and place
                path_opt[jump][jumpchoice] = tk.Label(mainwin, text=opt[int(jumpchoice + sum(pathssize[0:jump]) + 1)],
                                                   relief="groove")
                path_opt[jump][jumpchoice].config(font=mainapp.font_mono1, bg=mainapp.Background1)
                path_opt[jump][jumpchoice].grid(row=rowtrack, column=1, stick='w', padx=(0, 10))

                # note button and place
                notes_but[jump][jumpchoice] = tk.Label(mainwin, text="---", font=mainapp.font_mono1, relief="groove",
                                                    bg=mainapp.Background1)
                notes_but[jump][jumpchoice].grid(row=rowtrack, column=2, padx=(4, 8), sticky='nsw')

                # make all appropriate path binds
                path_opt[jump][jumpchoice].bind('<Enter>', lambda event, i=jump, j=jumpchoice: change_to(i, j))
                path_opt[jump][jumpchoice].bind('<Leave>', lambda event, i=jump, j=jumpchoice: change_back(i, j))
                path_opt[jump][jumpchoice].bind('<Button-1>', lambda event, i=jump, j=jumpchoice: lock_choice(i, j))

                # make all appropriate notes binds
                notes_but[jump][jumpchoice].bind('<Button-1>', lambda event, i=jump, j=jumpchoice: notes_look(i, j))
                notes_but[jump][jumpchoice].bind('<Enter>', lambda event, i=jump, j=jumpchoice: change_note_to(i, j))
                notes_but[jump][jumpchoice].bind('<Leave>', lambda event, i=jump, j=jumpchoice: change_note_back(i, j))
                notes_but[jump][jumpchoice].bind('<ButtonRelease-1>',
                                                 lambda event, i=jump, j=jumpchoice: unclick_note(i, j))

                # update row tracker
                rowtrack = rowtrack + 1

        # create final run with current path function
        def use_curr():
            need_sub = [abs(allpaths[x][int(choices[x])]) for x in range(0, m)][::-1]
            final_factors = [float(x) for x in fracdata[need_sub[0]][7:10]]
            for i in range(1, m):
                final_factors = [float(fracdata[need_sub[i]][x + 7]) - final_factors[x] for x in range(0, 3)]
            # set fractionation factor values
            forwardpage.forwardparams['Min' + str(but_num) + '-Afrac'].set(final_factors[0])
            forwardpage.forwardparams['Min' + str(but_num) + '-Bfrac'].set(final_factors[1])
            forwardpage.forwardparams['Min' + str(but_num) + '-Cfrac'].set(final_factors[2])


            # destory window now that values are set
            mainwin.destroy()

        # create final removal function
        def rem_curr(curr_frac_data):
            need_remove = []
            for jump in range(0, m):
                for jumpc in range(0, pathssize[jump]):
                    if (rem_checks[jump][jumpc].get() == 1):
                        table_index = abs(allpaths[jump][jumpc])
                        need_remove.append(table_index)
            need_remove = sorted(need_remove)[::-1]  # put list in reverse order to handle deletes correctly
            new_data = curr_frac_data
            for i in need_remove:
                # del fracdata[i]
                new_data = delete(new_data, i, axis=0)
            # now rerun whole script without these elements
            create_menus(new_data, node1, node2)

        #create two final buttons
        fin_but=dict()
        fin_but[1]=tk.Button(useorenter, text="Use Current Mineral Studies Chosen",
                             bg=mainapp.Background1, font=mainapp.font_buttons, command=use_curr)
        fin_but[1].config(state='disabled')
        fin_but[2]=tk.Button(mainwin, text="Remove", bg=mainapp.Background1,
                             font=mainapp.font_buttons, command=lambda: rem_curr(fracdata))


        #place buttons
        fin_but[1].grid(row=0, column=1, stick='w', pady=(0,10))
        fin_but[2].grid(row=rowtrack+1, column=0, padx=(8,8), pady=(0,10))
        useorenter.grid(row=rowtrack+1, column=1, sticky='w')

        #place division line
        sep_bot = tk.Label(mainwin, text="---------------------------------------------------------------")
        sep_bot.config(font=mainapp.font_buttons, bg=mainapp.Background1)
        sep_bot.grid(row=rowtrack, column=0, columnspan=2, padx=(14,0), pady=(0,0), sticky='w')


    # Create window with first options
    a='ParameterTables/FractionationFactorsR.csv'
    fractiondata=pandas.read_csv(a, header=None).values.astype('str')
    n=len(fractiondata)

    # divide factors a and b by 10^6 and 10^3
    for x in fractiondata[1:n]:
        x[9]=str(float(x[9])/10**6)
        x[8]=str(float(x[8])/10**3)

    #make main window and run function to create all buttons
    mainwin = tk.Toplevel()
    mainwin.wm_title('Find Fractionation Values')
    mainwin.config(bg=mainapp.Background1)

    mineral1=forwardpage.forwardparams['Min0-Name'].get()
    mineral2=forwardpage.forwardparams['Min' + str(but_num) + '-Name'].get()
    create_menus(fractiondata, mineral1,mineral2)


def DiffValueSearch(forwardpage, mainapp, but_num):

    # used when table entries can't be found and allows manual entry
    def enter_manual(num):
        forwardpage.rockcharframe.diffparam1_input[num].config(state='normal')
        forwardpage.rockcharframe.diffparam2_input[num].config(state='normal')
        mainwin.destroy()

    #used when we wish to input parameters from selected table entry
    def enter_table(num):
        Ea=diffdata[num,5]
        if Ea=='nan':
            forwardpage.rockcharframe.diffparam2_vars[but_num].set('0')
        else:
            forwardpage.rockcharframe.diffparam2_vars[but_num].set(Ea)
        forwardpage.rockcharframe.diffparam1_vars[but_num].set(diffdata[num,6])
        mainwin.destroy()




    # read in file with diffusivities and initialize
    a='ParameterTables/ODiffusionR.csv'
    diffdata=pandas.read_csv(a, header=None).values.astype('str')
    mineralname=forwardpage.forwardparams['Min'+str(but_num)+'-Name'].get()
    n=len(diffdata)

    # search for all entries in file with given mineral name
    if len(mineralname)>0:
        loc_min=[i for i in range(0,n) if mineralname.lower() in diffdata[i,1].lower()]
        loc_min=[0]+loc_min
    else:
        loc_min=[]



    # create first window of options
    mainwin = tk.Toplevel()
    mainwin.wm_title('Find Diffusivity Parameters')
    mainwin.config(bg=mainapp.Background1)

    #create manual button and label
    win_caption = tk.Label(mainwin, text='' + mineralname,
                           bg=mainapp.Background1, font=mainapp.font_labels)
    ButtonMan = tk.Button(mainwin, text="Enter Manually", relief="groove",
                          bg=mainapp.Background1, font=mainapp.font_buttons)
    ButtonMan.bind('<Button-1>', lambda event: enter_manual(but_num))

    # Create menu of optional diffusion parameters to use
    m=len(loc_min)
    if m<1:

        win_caption.config(text='I have no available data for'+mineralname)
        #place items
        win_caption.grid(row=0, column=1, padx=(10,10), pady=(10,10))
        ButtonMan.grid(row=1, column=1, pady=(0,10))

    else:
        win_caption.config(text='I have the following table entries for '+mineralname+':')

        #keep only those element we are interested in
        colskeep=[1,2,3,4,6,5,8,10]
        datakeep=diffdata[loc_min,:]
        datakeep=datakeep[:,colskeep]

        #for each column make all text match maximum amount of white space
        for k in range(0,8):
            maxlength=max([len(datakeep[i,k]) for i in range(0,m)])
            for i in range(0,m):
                datakeep[i,k]=datakeep[i,k]+(maxlength+5-len(datakeep[i,k]))*' '

        #now that all text is same length, make buttons
        ChoiceButtons=dict()
        for i in range(0,m):
            ChoiceButtons[i]=tk.Button(mainwin, text=''.join(datakeep[i,:]),
                          bg=mainapp.Background1, font=mainapp.font_mono1, relief='groove')
            ChoiceButtons[i].grid(row=i+2, column=1, sticky='nswe', padx=(10,10), pady=(10*(i<1),10*(i<1)))
            if (i>0):
                ChoiceButtons[i].bind('<Button-1>', lambda event, i=i: enter_table(loc_min[i]))

        ChoiceButtons[0].config(relief='flat',activebackground=mainapp.Background1, font=mainapp.font_mono2)


        #place other elements
        win_caption.grid(row=1,column=0,columnspan=9)
        tk.Label(mainwin,text='----------------------------------------', bg=mainapp.Background1,
                 font=mainapp.font_buttons).grid(row=m+2,column=1,pady=(1,1))
        ButtonMan.grid(row=m+3, column=1,pady=(0,5))




def PlotGraphs(forwardpage):

    currentfig = 0
    tend=len(forwardpage.tarray)
    nmin=int(forwardpage.xarray.shape[1])
    duration=forwardpage.tarray[-1]

    for i in range(0,nmin):
        checkif=forwardpage.graphingframe.plotsingle_chkvar[i].get()
        if checkif == 1:
            currentfig=currentfig+1
            plt.figure(currentfig)
            plottimes = forwardpage.graphingframe.plotsingle_var[i].get()
            plottimes = [float(x) for x in plottimes.split(',')]
            legendtimes = [str(x)+'  million years' for x in plottimes]
            n=len(plottimes)
            for j in range(0,n):
                ygr=forwardpage.yarray[i,max(0,min(int((plottimes[j]/duration)*tend),tend-1)),:]
                xgr=forwardpage.xarray[:,i]
                plt.plot(xgr,ygr)
            plt.legend(legendtimes)
            plt.xlabel('x (cm)')
            plt.ylabel('Delta 18-O')
            plt.title('Plot of oxygen isotope ratios for '+
                      forwardpage.forwardparams['Min' + str(i) + '-Name'].get())

    if forwardpage.graphingframe.plotall_chkvar.get() == 1:
        currentfig=currentfig+1
        plt.figure(currentfig)
        plottimes = forwardpage.graphingframe.plotall_var.get()
        plottimes = [float(x) for x in plottimes.split(',')]
        legendtimes = [str(x)+' million years' for x in plottimes]
        plotindices = [max(0,min(tend-1,int((x/duration)*tend))) for x in plottimes]
        for t in plotindices:
            yworking = forwardpage.yarray[:, int(t), :]
            for m in range(0, nmin):
                plt.subplot(nmin, 1, m + 1)
                xgr=forwardpage.xarray[:,m]
                ygr=yworking[m,:]
                plt.plot(xgr,ygr)
        plt.legend(legendtimes)
    plt.show()






    a=3


class ForwardModelPage(tk.Frame):

    def getcoolingfile(self,cooltype):

        if cooltype=='Custom':
            # Read file and save to dictionary
            file_loc = filedialog.askopenfilename(filetypes=(("Plain Text", ".txt"), ("all files", "*.*")),
                                              defaultextension=".txt")
            if file_loc:
                self.forwardparams['CoolingFile'].set(file_loc)
            else:
                self.forwardparams['CoolingType'].set('Linear')


    def setnummin(self,n):
        for i in range(0,int(n)):
            self.rockcharframe.column_labels[i].grid(row=i+1, column=0)
            self.rockcharframe.mineralname_inputs[i].grid(row=i+1,column=1,sticky='nsew')
            self.rockcharframe.mineralmode_inputs[i].grid(row=i+1,column=2,sticky='nsew')
            self.rockcharframe.mineralshape_inputs[i].grid(row=i+1,column=3,sticky='nsew')
            self.rockcharframe.mineralrad_inputs[i].grid(row=i+1,column=4,sticky='nsew')
            self.rockcharframe.mineralwid_inputs[i].grid(row=i+1,column=5,sticky='nsew')
            self.rockcharframe.mineralfracA_inputs[i].grid(row=i+1,column=6,sticky='nsew')
            self.rockcharframe.mineralfracB_inputs[i].grid(row=i+1,column=7,sticky='nsew')
            self.rockcharframe.mineralfracC_inputs[i].grid(row=i+1,column=8,sticky='nsew')
            if (i>0):
                self.rockcharframe.fracsearch[i].grid(row=i+1, column=9)
            self.rockcharframe.diffparam1_input[i].grid(row=i+1,column=10, sticky='nsew')
            self.rockcharframe.diffparam2_input[i].grid(row=i+1,column=11, sticky='nsew')
            self.rockcharframe.diffsearch[i].grid(row=i+1, column=12)
            self.rockcharframe.oxcon_inputs[i].grid(row=i+1,column=13, sticky='nsew')


            self.graphingframe.plotsingle_check[i].grid(row=2*int(i/2), column=i%2, sticky='nsw', padx=(5,0))
            self.graphingframe.plotsingle_input[i].grid(row=2*int(i/2)+1, column=i%2, sticky='nsw', padx=(11,0))

        for i in range(int(n),8):
            self.rockcharframe.column_labels[i].grid_remove()
            self.rockcharframe.mineralname_inputs[i].grid_remove()
            self.rockcharframe.mineralmode_inputs[i].grid_remove()
            self.rockcharframe.mineralshape_inputs[i].grid_remove()
            self.rockcharframe.mineralrad_inputs[i].grid_remove()
            self.rockcharframe.mineralwid_inputs[i].grid_remove()
            self.rockcharframe.mineralfracA_inputs[i].grid_remove()
            self.rockcharframe.mineralfracB_inputs[i].grid_remove()
            self.rockcharframe.mineralfracC_inputs[i].grid_remove()
            if i>0:
                self.rockcharframe.fracsearch[i].grid_remove()
            self.rockcharframe.diffparam1_input[i].grid_remove()
            self.rockcharframe.diffparam2_input[i].grid_remove()
            self.rockcharframe.diffsearch[i].grid_remove()
            self.rockcharframe.oxcon_inputs[i].grid_remove()


    def setnumgraphs(self,n):
        for i in range(0,int(n)):
            self.graphingframe.plotsingle_check[i].configure(state='normal')
        for i in range(int(n),8):
            self.graphingframe.plotsingle_check[i].configure(state='disabled')
            self.graphingframe.plotsingle_chkvar[i].set(0)
        if n>0:
            self.graphingframe.plotall_check.configure(state='normal')
            self.graphingframe.plot.configure(state='normal')
        else:
            self.graphingframe.plotall_check.configure(state='disabled')
            self.graphingframe.plotall_chkvar.set(0)
            self.graphingframe.plot.configure(state='disabled')



    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.config(bg=parent.Background1)

        # Set weights for all rows and columns in frame
        for i in range(0,2):
            self.grid_rowconfigure(i, weight=1)
        for j in range(0,2):
            self.grid_columnconfigure(j, weight=1)


        # Create three main sections of forward model tab.

        self.modelcharframe = ModelCharFrame(self,parent)
        self.modelcharframe.grid(row=0, column=0, sticky='nsew', padx=(3,3), pady=(3,3))

        self.rockcharframe = RockCharFrame(self, parent)
        self.rockcharframe.grid(row=1, column=0, sticky='nsew', padx=(3,3), pady=(3,3))

        self.graphingframe = GraphingFrame(self, parent)
        self.graphingframe.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=(3,3), pady=(3,3))

        self.setnummin(2)
        self.setnumgraphs(0)

        # Create dicationary of all forward model parameters to be set and read for
        # import and export by the file dialog box

        # Create dictionary and save all model params to it.
        self.forwardparams = dict()
        self.forwardparams['NumMinerals'] = self.modelcharframe.numminerals_var
        self.forwardparams['CoolingType'] = self.modelcharframe.coolingtype_var
        self.forwardparams['CoolingFile'] = self.modelcharframe.coolinghistory
        self.forwardparams['WholeRock'] = self.modelcharframe.wholerock_var
        self.forwardparams['ModelDuration'] = self.modelcharframe.modelduration_var
        self.forwardparams['StartingTemp'] = self.modelcharframe.starttemp_var
        self.forwardparams['TimeStep'] = self.modelcharframe.timestep_var
        self.forwardparams['EndTemp'] = self.modelcharframe.endtemp_var

        # Save the rock parameters to dictionary for each mineral.
        for i in range(0,8):
            self.forwardparams['Min' + str(i) + '-Name'] = self.rockcharframe.mineralname_vars[i]
            self.forwardparams['Min' + str(i) + '-Mode'] = self.rockcharframe.mineralmode_vars[i]
            self.forwardparams['Min' + str(i) + '-Shape'] = self.rockcharframe.mineralshape_vars[i]
            self.forwardparams['Min' + str(i) + '-R'] = self.rockcharframe.mineralrad_vars[i]
            self.forwardparams['Min' + str(i) + '-W'] = self.rockcharframe.mineralwid_vars[i]
            self.forwardparams['Min' + str(i) + '-Afrac'] = self.rockcharframe.mineralfracA_vars[i]
            self.forwardparams['Min' + str(i) + '-Bfrac'] = self.rockcharframe.mineralfracB_vars[i]
            self.forwardparams['Min' + str(i) + '-Cfrac'] = self.rockcharframe.mineralfracC_vars[i]
            self.forwardparams['Min' + str(i) + '-Dparam1'] = self.rockcharframe.diffparam1_vars[i]
            self.forwardparams['Min' + str(i) + '-Dparam2'] = self.rockcharframe.diffparam2_vars[i]
            self.forwardparams['Min' + str(i) + '-Oxcon'] = self.rockcharframe.oxcon_vars[i]
















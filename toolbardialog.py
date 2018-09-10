import tkinter as tk
from tkinter import filedialog
from modelfunctions import *


def runcommand(main):

    curr_tab = main.maintabs.index("current")

    # If on first tab set model output to page 1 so that they can be used by graph button
    if curr_tab==0:
        x, y, t = run_forwardmodel(main.page1.forwardparams)
        main.page1.xarray=array(x)
        main.page1.yarray=array(y)
        main.page1.tarray=array(t)
        main.page1.graphingframe.plot.configure(state='normal')
        main.page1.setnumgraphs(array(x).shape[1])


    if curr_tab==1:
        print('working on it 1')

    if curr_tab==2:
        print('working on it 2')



    print('run the model and save in global')


def loadparameters(main):

    # Get file location to import.
    file_loc = filedialog.askopenfilename(filetypes=(("Plain Text", ".txt"), ("all files", "*.*")),
                                          defaultextension=".txt")

    # Get current tab and use appropriate export option.
    curr_tab = main.maintabs.index("current")

    # Set import features for first tab.
    if curr_tab==0 and file_loc:

        # Open file and read all parameters into model
        f=open(file_loc,'r').read().split('\n')
        f=[x.split(',') for x in f[0:-1]]

        for pairs in f:
            main.page1.forwardparams[pairs[0]].set(pairs[1])

        # Set the number of mineral's
        main.page1.setnummin(main.page1.forwardparams['NumMinerals'].get())


def saveparameters(main):

    # Get current tab and use appropriate export option.
    curr_tab=main.maintabs.index("current")

    # Get file location to save to
    file_loc = filedialog.asksaveasfilename(filetypes=(("Plain Text", ".txt"),
                                                       ("all files", "*.*")),
                                            defaultextension=".txt")

    # Set export button for first tab, and check that file location isn't empty.
    if curr_tab==0 and file_loc:

        f=open(file_loc,'w')
        for key in main.page1.forwardparams:
            f.write('{0},{1}\n'.format(key,main.page1.forwardparams[key].get()))
        f.close()


    # Set export button for second tab
    if curr_tab==1:
        print('In progress')

    # Set export button for third tab
    if curr_tab==2:
        print('In progress')


def exportmodelrun(main):

    curr_tab = main.maintabs.index("current")
    file_loc = filedialog.asksaveasfilename(filetypes=(("Numpy Obj", ".npz"),
                                                       ("all files", "*.*")),
                                            defaultextension=".npz")

    if curr_tab == 0 and file_loc:
         # Save all output from model run as numpy object
         savez(file_loc,main.page1.xarray,main.page1.yarray,main.page1.tarray)

    if curr_tab == 1:
        print('Export inverse model run')

    print('\n')


def importmodelrun(main):

    curr_tab = main.maintabs.index("current")
    file_loc = filedialog.askopenfilename(filetypes=(("Python Obj", ".npz"), ("all files", "*.*")),
                                          defaultextension=".npz")

    # If on first tab set model output to page 1 so that they can be used by graph button
    if curr_tab==0 and file_loc:

        npzfile = load(file_loc)
        main.page1.xarray=npzfile['arr_0']
        main.page1.yarray=npzfile['arr_1']
        main.page1.tarray=npzfile['arr_2']
        main.page1.setnummin(main.page1.xarray.shape[1])
        main.page1.setnumgraphs(main.page1.xarray.shape[1])



    print('\n')


def increasefont(main):

    # Update all font sizes
    incr=2

    size=main.font_inputs['size']
    main.font_inputs.configure(size=size+incr)

    size=main.font_sections['size']
    main.font_sections.configure(size=size+incr)

    size=main.font_labels['size']
    main.font_labels.configure(size=size+incr)

    size=main.font_buttons['size']
    main.font_buttons.configure(size=size+incr)

    size=main.font_message['size']
    main.font_message.configure(size=size+incr)

    size=main.font_mono1['size']
    main.font_mono1.configure(size=size+incr)





def decreasefont(main):

    # Update all font sizes
    incr = -2

    size = main.font_inputs['size']
    main.font_inputs.configure(size=size + incr)

    size = main.font_sections['size']
    main.font_sections.configure(size=size + incr)

    size = main.font_labels['size']
    main.font_labels.configure(size=size + incr)

    size = main.font_buttons['size']
    main.font_buttons.configure(size=size + incr)

    size = main.font_message['size']
    main.font_message.configure(size=size + incr)

    size = main.font_mono1['size']
    main.font_mono1.configure(size=size + incr)







class ToolBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label='Run', command=lambda: runcommand(parent))
        filemenu.add_command(label='Load Parameters', command=lambda: loadparameters(parent))
        filemenu.add_command(label='Save Parameters', command=lambda: saveparameters(parent))
        filemenu.add_command(label='Import Model Run', command=lambda: importmodelrun(parent))
        filemenu.add_command(label='Export Model Run', command=lambda: exportmodelrun(parent))

        viewmenu = tk.Menu(self, tearoff=0)
        viewmenu.add_command(label='Increase Font Size', command=lambda: increasefont(parent))
        viewmenu.add_command(label='Decrease Font Size', command=lambda: decreasefont(parent))



        self.add_cascade(label='File', menu=filemenu)
        self.add_cascade(label='View', menu=viewmenu)


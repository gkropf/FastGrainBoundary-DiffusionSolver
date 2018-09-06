import tkinter as tk



class ModelCharFrame(tk.LabelFrame):

    def __init__(self,parent,mainapp):
        tk.LabelFrame.__init__(self, parent)
        self.config(bg=mainapp.Background1)
        self.config(text='Global Model Characteristics')

        # Construct model characteristics section elements.
        self.numminerals_var = tk.IntVar(self)
        self.numminerals_var.set(2)
        self.numminerals_label = tk.Label(self, text="Minerals",
                                         font=mainapp.font_labels, bg='white')
        self.numminerals_input = tk.OptionMenu(self, self.numminerals_var, "2", "3",
                                               "4", "5", "6", "7", "8",
                                               command= parent.setnummin)

        self.coolingtype_var = tk.StringVar(self)
        self.coolingtype_var.set("Linear")
        self.coolingtype_label = tk.Label(self, text="Cooling Type",
                                          font=mainapp.font_labels, bg='purple')
        self.coolingtype_input = tk.OptionMenu(self, self.coolingtype_var, "Linear",
                                          "Inverse", "Custom")

        self.wholerock_var = tk.DoubleVar(self)
        self.wholerock_var.set("")
        self.wholerock_label = tk.Label(self, text="Whole Rock",
                                        font=mainapp.font_labels, bg='blue')
        self.wholerock_input = tk.Entry(self, textvariable=self.wholerock_var)

        self.modelduration_var = tk.DoubleVar(self)
        self.modelduration_var.set("")
        self.modelduration_label = tk.Label(self, text="Model Duration",
                                            font=mainapp.font_labels, bg='white')
        self.modelduration_input = tk.Entry(self, textvariable=self.modelduration_var)

        self.starttemp_var = tk.DoubleVar(self)
        self.starttemp_var.set("")
        self.starttemp_label = tk.Label(self, text="Starting Temp",
                                        font=mainapp.font_labels, bg='purple')
        self.starttemp_input = tk.Entry(self, textvariable=self.starttemp_var)

        self.timestep_var = tk.IntVar(self)
        self.timestep_var.set("")
        self.timestep_label = tk.Label(self, text="Time Step",
                                       font=mainapp.font_labels, bg='white')
        self.timestep_input = tk.Entry(self, textvariable=self.timestep_var)

        self.endtemp_var = tk.DoubleVar(self)
        self.endtemp_var.set("")
        self.endtemp_label = tk.Label(self, text="End Temp",
                                      font=mainapp.font_labels, bg='purple')
        self.endtemp_input = tk.Entry(self, textvariable=self.endtemp_var)


        # Place all model characteristics elements.
        self.numminerals_label.grid(row=0, column=1, sticky='e')
        self.numminerals_input.grid(row=0, column=2, stick='we')

        self.coolingtype_label.grid(row=1, column=1, sticky='e')
        self.coolingtype_input.grid(row=1, column=2, sticky='we')

        self.wholerock_label.grid(row=2, column=1, sticky='e')
        self.wholerock_input.grid(row=2, column=2, sticky='we')

        self.modelduration_label.grid(row=0, column=3, sticky='e')
        self.modelduration_input.grid(row=0, column=4, sticky='we')

        self.starttemp_label.grid(row=1, column=3, sticky='e')
        self.starttemp_input.grid(row=1, column=4, sticky='we')

        self.timestep_label.grid(row=0, column=5, sticky='e')
        self.timestep_input.grid(row=0, column=6, sticky='we')

        self.endtemp_label.grid(row=1, column=5, sticky='e')
        self.endtemp_input.grid(row=1, column=6, sticky='we')


class RockCharFrame(tk.LabelFrame):

    def __init__(self,parent,mainapp):
        tk.LabelFrame.__init__(self, parent)
        self.config(bg=mainapp.Background1)
        self.config(text='Mineral Properties')


        self.mineralname_label = tk.Label(self, text="Name",
                                          font=mainapp.font_labels)
        self.mineralname_label.grid(row=0,column=1)
        self.mineralname_vars=dict()
        self.mineralname_inputs=dict()
        for i in range(0,8):
            self.mineralname_vars[i] = tk.DoubleVar(parent)
            self.mineralname_vars[i].set("")
            self.mineralname_inputs[i] = tk.Entry(self, textvariable=self.mineralname_vars[i])


        self.mineralmode_label = tk.Label(self, text="Mode",
                                          font=mainapp.font_labels)
        self.mineralmode_label.grid(row=0,column=2)
        self.mineralmode_vars=dict()
        self.mineralmode_inputs=dict()
        for i in range(0,8):
            self.mineralmode_vars[i] = tk.DoubleVar(parent)
            self.mineralmode_vars[i].set("")
            self.mineralmode_inputs[i] = tk.Entry(self, textvariable=self.mineralmode_vars[i])


        self.mineralshape_label = tk.Label(self, text="Shape",
                                          font=mainapp.font_labels)
        self.mineralshape_label.grid(row=0,column=3)
        self.mineralshape_vars=dict()
        self.mineralshape_inputs=dict()
        for i in range(0,8):
            self.mineralshape_vars[i] = tk.DoubleVar(parent)
            self.mineralshape_vars[i].set("")
            self.mineralshape_inputs[i] = tk.OptionMenu(self, self.mineralshape_vars[i],
                                                        "Slab","Spherical")
            self.mineralshape_vars[i].set("Slab")


        self.mineralrad_label = tk.Label(self, text="R",
                                          font=mainapp.font_labels)
        self.mineralrad_label.grid(row=0,column=4)
        self.mineralrad_vars=dict()
        self.mineralrad_inputs=dict()
        for i in range(0,8):
            self.mineralrad_vars[i] = tk.DoubleVar(parent)
            self.mineralrad_vars[i].set("")
            self.mineralrad_inputs[i] = tk.Entry(self, textvariable=self.mineralrad_vars[i])


        self.mineralwid_label = tk.Label(self, text="W",
                                          font=mainapp.font_labels)
        self.mineralwid_label.grid(row=0,column=5)
        self.mineralwid_vars=dict()
        self.mineralwid_inputs=dict()
        for i in range(0,8):
            self.mineralwid_vars[i] = tk.DoubleVar(parent)
            self.mineralwid_vars[i].set("")
            self.mineralwid_inputs[i] = tk.Entry(self, textvariable=self.mineralwid_vars[i])


        self.mineralfraca_label = tk.Label(self, text="A frac",
                                          font=mainapp.font_labels)
        self.mineralfraca_label.grid(row=0,column=5)
        self.mineralfraca_vars=dict()
        self.mineralfraca_inputs=dict()
        for i in range(0,8):
            self.mineralfraca_vars[i] = tk.DoubleVar(parent)
            self.mineralfraca_vars[i].set("")
            self.mineralfraca_inputs[i] = tk.Entry(self, textvariable=self.mineralfraca_vars[i])

        tk.Label(self,text='Element-specific fractiontion options').grid(row=2,column=6)




class ForwardModelPage(tk.Frame):


    def setnummin(self,n):
        for i in range(0,int(n)):
            self.rockcharframe.mineralname_inputs[i].grid(row=i+1,column=1)
            self.rockcharframe.mineralmode_inputs[i].grid(row=i+1,column=2)
            self.rockcharframe.mineralshape_inputs[i].grid(row=i+1,column=3)
            self.rockcharframe.mineralrad_inputs[i].grid(row=i+1,column=4)
            #self.rockcharframe.mineralwid_inputs[i].grid(row=i+1,column=5)



        for i in range(int(n),8):
            self.rockcharframe.mineralname_inputs[i].grid_remove()
            self.rockcharframe.mineralmode_inputs[i].grid_remove()
            self.rockcharframe.mineralshape_inputs[i].grid_remove()
            self.rockcharframe.mineralrad_inputs[i].grid_remove()
            #self.rockcharframe.mineralwid_inputs[i].grid_remove()





    def __init__(self,parent,mainapp):
        tk.Frame.__init__(self,parent)


        # Create three main sections of forward model tab.

        self.modelcharframe = ModelCharFrame(self,mainapp)
        self.modelcharframe.grid(row=0, column=0, sticky='nsew')

        self.rockcharframe = RockCharFrame(self, mainapp)
        self.rockcharframe.grid(row=1, column=0, sticky='nsew')
        self.setnummin(2)










        #self.rockCharFrame = tk.LabelFrame(self, text='Properties of Minerals')
        #self.rockCharFrame.config(bg=mainapp.Background1,
        #                          font=mainapp.font_sections)
        #self.rockCharFrame.grid(row=1, column=0, sticky='nsew')

        #self.graphOptionsFrame = tk.LabelFrame(self, text='Properties of Minerals')
        #self.graphOptionsFrame.config(bg=mainapp.Background1,
        #                              font=mainapp.font_sections)
        #self.graphOptionsFrame.grid(row=0, column=1, rowspan=2, sticky='nsew')




from tkinter import *
from tkinter import filedialog
from numpy import *
import numpy.matlib
import matplotlib.pyplot as plt
import os, sys
import csv
from tkinter import ttk

# Visual theme controls
fonts = 12
titlefonts = ("Helvetica", 10)
fonts1 = ("helvetica", 11)
fonts2 = ("ariel", 12, "bold")
brs = ("Hevetica", 10)
runcmnds = ("Helvetica", 9)
background1 = '#c5ddeb'
bkgr2 = "white"



#### Funcion Block For GUI Interface (beg) ####

# This class and subsequent function allows the simplified creation of explanation text on widgest aa
# copied from http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml#e387
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    def showtip(self, text):
        "Display text ub tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


# function reloads gui (used when user picks new number of minerals)
def relo(event):
    FileHand.grid()
    ModelChar.grid()
    RockChar.grid()
    GraphChar.grid()
    nono.grid_remove()

# used when saving model params (incase a field is empty is saves it as a 0)
def getval(widget):
    try:
        a=widget.get()
    except TclError:
        a=0
    return a

# used to make sure model params its saving are non zero
def checkvalid():
    test=1
    test=test*getval(duration)
    test=test*getval(timestep)
    test=test*getval(modelend)
    test=test*getval(modelstart)

    if test==1:
        print('good')
    else:
        print('bad')

# removes unnecessary entry fields (when number of minerals is changed)
def removel(x):
    x=int(x)
    rocksl[x].grid_remove()
    for i in range(1,12):
        Rocks[x][i].grid_remove()

# adds entry fields (when number of minerals is changed)
def addl(x):
    x=int(x)
    rocksl[x].grid()
    for i in range(1,12):
        Rocks[x][i].grid()

def importf():
    a = filedialog.askopenfilename()
    importb.set(a)

def exportf():
    a = filedialog.asksaveasfilename()
    exportb.set(a)

def readjustn():
    a=nummin.get()
    for i in range(1,a+1):
        addl(i)
        lookupb[i].grid()
        lookupbb[i].grid()
    for i in range(a+1,9):
        removel(i)
        lookupb[i].grid_remove()
        lookupbb[i].grid_remove()

def readjust(event):
    readjustn()

def writedata():
    nm = exportb.get()
    fileobj = open(nm, "w")

    dat = ""
    dat = dat + " " +str(nummin.get())
    dat = dat + " " +str(duration.get())
    dat = dat + " " +str(timestep.get())
    dat = dat + " " +str(cooling.get())
    dat = dat + " " +str(modelstart.get())
    dat = dat + " " +str(modelend.get())
    dat = dat + " " +str(wrd180t.get())
    fileobj.write(dat)

    dat = " "
    for i in range(1,nummin.get()+1):
        for j in range(1,12):
            dat = dat+" "+str(rocks[i][j].get())


    fileobj.write(dat)
    fileobj.close()

def readdata():
    nm = importb.get()
    fileobj = open(nm, "r")
    dat = fileobj.read()
    dat = dat.split()
    print(len(dat))

    nummin.set(int(dat[0]))
    duration.set(float(dat[1]))
    timestep.set(float(dat[2]))
    cooling.set(dat[3])
    modelstart.set(float(dat[4]))
    modelend.set(float(dat[5]))
    wrd180t.set(float(dat[6]))

    k=7
    for i in range(1,int(dat[0])+1):
        for j in range(1,12):
            rocks[i][j].set(dat[k])
            k=k+1
    readjustn()
#### Function Block for GUI Interface (end) ####


### Creation Block for popup GUI (beg)###

def frac_search(but_num):
    mainwin = Toplevel()
    mainwin.wm_title('Find Fractionation Values')

    l = Label(mainwin, text='What')
    l.grid(row=0, column=0)
    print(but_num)

def diff_search(but_num):


    #change color of hover over
    def change_to(num):
        Possible_options[num].config(bg='#A0A0A0')

    def change_back(num):
        Possible_options[num].config(bg=background1)

    def set_diff_params(num):
        rocks[but_num][9].set(exp(float(cols[10][num])))
        rocks[but_num][10].set(float(cols[12][num]))
        mainwin.destroy()

    def final_options(num):
        readjust_diff(0)
        direc.config(text="Would you like to use your current selection or enter manually?")

        use_curr = Button(mainwin, text="Use Current Selection", relief='groove', bg=background1)
        use_curr.bind('<Button-1>', lambda event: set_diff_params(num))
        use_curr.grid(row=3, column=0)

        ent_man = Button(mainwin, text="Enter Manually (not recommended)", relief='groove', bg=background1)
        ent_man.grid(row=4, column=0)

    # set what options are available based on conversions
    def set_options(curr_min):
        if curr_min in conversions:
            options_list = conversions[curr_min]
            numopt = size(options_list)
            for i in range(1, numopt + 1):
                possible_options[i].set(options_list[i-1])
            readjust_diff(numopt)
        else:
            readjust_diff(0)
            direc.config(text="I have the following table entries for this mineral:")
            mat = find_in_table(curr_min)

            for i in range(0, min(5,size(mat))):
                text_col=''
                for j in range(1,17):
                    text_col=text_col+'  '+cols[j][mat[i]]
                possible_options[i+1].set(text_col)
            readjust_diff(min(5,size(mat)+1))
            Possible_options[1].bind('<Button-1>', lambda event: final_options(mat[0]))
            Possible_options[2].bind('<Button-1>', lambda event: final_options(mat[1]))
            Possible_options[3].bind('<Button-1>', lambda event: final_options(mat[2]))
            Possible_options[4].bind('<Button-1>', lambda event: final_options(mat[3]))
            Possible_options[5].bind('<Button-1>', lambda event: final_options(mat[4]))


    # add or removed unused options
    def readjust_diff(num):
        for i in range(1, num + 1):
            Possible_options[i].grid()
        for i in range(num + 1, 6):
            Possible_options[i].grid_remove()

    # choose current selection and readjust options
    def choose_opt(num):
        name_selec = possible_options[num].get()
        curnam = selection.get()
        selection.set(curnam+' > '+name_selec)

        set_options(name_selec)

    def find_in_table(min_name):
        matches = []
        for i in range(0, len(cols[1])):
            if str(min_name) in cols[1][i]:
                matches.append(i)
        return matches








    mainwin = Toplevel()
    mainwin.wm_title('Find Diffusion Parameters for Mineral')
    mainwin.config(bg=background1)

    curr_min = rocks[but_num][1].get()
    selection = StringVar(mainwin)
    selection.set('Current mineral: '+curr_min)
    Selection = Label(mainwin, textvariable=selection)
    Selection.config(font=titlefonts, bg=background1)
    direc = Label(mainwin, text="For your class of minerals I have the following options for subclass':")
    direc.config(font=fonts2, bg=background1)

    possible_options = dict()
    Possible_options = dict()
    for i in range(1,6):
        possible_options[i] = StringVar(mainwin)
        possible_options[i].set('Option'+str(i))
        Possible_options[i] = Label(mainwin, textvariabl=possible_options[i], relief="groove")
        Possible_options[i].config(font=titlefonts, bg=background1)

    Possible_options[1].bind('<Button-1>', lambda event: choose_opt(1))
    Possible_options[2].bind('<Button-1>', lambda event: choose_opt(2))
    Possible_options[3].bind('<Button-1>', lambda event: choose_opt(3))
    Possible_options[4].bind('<Button-1>', lambda event: choose_opt(4))
    Possible_options[5].bind('<Button-1>', lambda event: choose_opt(5))

    Possible_options[1].bind('<Enter>', lambda event: change_to(1))
    Possible_options[2].bind('<Enter>', lambda event: change_to(2))
    Possible_options[3].bind('<Enter>', lambda event: change_to(3))
    Possible_options[4].bind('<Enter>', lambda event: change_to(4))
    Possible_options[5].bind('<Enter>', lambda event: change_to(5))

    Possible_options[1].bind('<Leave>', lambda event: change_back(1))
    Possible_options[2].bind('<Leave>', lambda event: change_back(2))
    Possible_options[3].bind('<Leave>', lambda event: change_back(3))
    Possible_options[4].bind('<Leave>', lambda event: change_back(4))
    Possible_options[5].bind('<Leave>', lambda event: change_back(5))

    Selection.grid(row=1, column=0, sticky=W)
    direc.grid(row=2, column=0)
    for i in range(1,6):
        Possible_options[i].grid(row=i+2, column=0)
        Possible_options[i].grid_remove()


    set_options(curr_min)


#load diffusion for table lookup
a=os.path.dirname(sys.argv[0])
a=a+'/Diffusion.csv'

file = open(a, 'r')
#file = open('C:/Users/gabe_/Documents/PyCharm/Diffusion.csv', 'r')
dat = csv.reader(file)

rows = dict()
data = []

rnum = 0
for a in dat:
    rows[rnum]=a
    rnum=rnum+1

cols = []
for i in range(0,len(rows[0])):
    cols.append([])
    for j in range(0, len(rows)):
        cols[i].append(rows[j][i])


### Creation Block for popup GUI (end)###




#### Function Block for Diffusion Solver (beg) ####
def fluxbal(z, e, f, h, j, k, l):
    X = zeros([z])
    A = zeros([z, z])
    for m in range(0, z - 1):
        A[m, 0] = 1
        A[m, m + 1] = -1
    A[z - 1, :] = j * k * l * f
    B = zeros([z])
    B[0:z - 1] = h[1:z]
    B[z - 1] = sum(j * k * l * f * e)
    X = linalg.solve(A, B)
    return X


def octrave(b):
    file = open(b, 'r')
    str = file.read()
    rows = str.split('\n')
    rowb = len(rows)
    colb = len(rows[0].split('\t'))
    dat = zeros([rowb, colb])
    for i in range(0, rowb):
        dat[i, :] = rows[i].split('\t')
    if colb == 3:
        distance = dat[:, colb - 1]
    else:
        print('et')
        X0 = dat[0, colb - 2]
        Y0 = dat[0, colb - 1]
        ##select traverse origin
        origin = zeros([colb])
        origin[colb - 2] = X0
        origin[colb - 1] = Y0
        OR = numpy.matlib.repmat(origin, rowb, 1)
        # referance all coordinates to newly selected origin
        C = dat - OR
        N = C[:, colb - 2:colb]
        travend = C[rowb - 1, colb - 2:colb]
        distance = zeros([rowb])
        for i in range(0, rowb):
            distance[i] = dot(N[i, :], travend) / sqrt(pow(travend[0], 2) + pow(travend[1], 2))
    return [distance, dat[:, 0], dat[:, 1]]
#### Function Block for Diffusion Solver (end) ####


### Create conversion table for mineral searchs
conversions = dict()
conversions['feldspar'] = ['plagioclase','kfeldspar','KAISi3O8']
conversions['plagioclase'] = ['albite','anorthite']
conversions['kfeldspar'] = ['microcline','orthoclase','sanidine']

conversions['clay'] = ['kaolinite','smectite','inite']





# This is the main diffusion solver function
def runmain():

    loading.grid(row=3, column=1, columnspan=1, sticky=W)
    root.update()

    # get user defined info
    ttot = float(duration.get())
    dt = float(timestep.get())
    WRd180 = float(wrd180t.get())
    Tstart = float(modelstart.get())
    Tend = float(modelend.get())
    cool = 1
    nmin = int(nummin.get())
    de = 100

    plot1 = 1
    plot2 = 1

    # unit definitions and converions
    deltat = dt*3.1536e+13
    tend = math.ceil(ttot/dt)
    Tstart = Tstart + 273
    Tend = Tend + 273
    T0 = Tstart
    T = Tstart

    # initialize storage matrices
    mode = zeros([nmin])
    shape = zeros([nmin])
    L = zeros([nmin])
    w = zeros([nmin])
    r = zeros([nmin])
    SA = zeros([nmin])
    dx = zeros([nmin])
    gb = zeros([nmin])
    d180 = zeros([nmin])
    Afac = zeros([nmin])
    Bfac = zeros([nmin])
    Cfac = zeros([nmin])
    D0 = zeros([nmin])
    Q = zeros([nmin])
    D = zeros([nmin])
    fracfax = zeros([nmin])
    oxcon = zeros([nmin])
    R = 8.3144621  # J/K*ml

    ## get all rock properties

    # mineral 1 - monitor, quartz
    mode[0] = 0.20
    shape[0] = 2
    r[0] = 20
    L[0] = 2 * r[0]
    w[0] = 20
    dx[0] = r[0] / de
    gb[0] = math.ceil(L[0] / dx[0])
    Afac[0] = 0
    Bfac[0] = 0
    Cfac[0] = 0
    d180[0] = 99
    D0[0] = 3.4e-9
    Q[0] = 98000
    oxcon[0] = 0.0882

    # mineral 2 - alkali feldspar
    mode[1] = 0.76
    shape[1] = 1
    r[1] = 30
    L[1] = 2 * r[1]
    w[1] = 30
    dx[1] = r[1] / de
    gb[1] = math.ceil(L[1] / dx[1])
    Afac[1] = 0
    Bfac[1] = 0
    Cfac[1] = 1.0
    d180[1] = 99
    D0[1] = 7.6e-6
    Q[1] = 129500
    oxcon[1] = 0.0734

    # mineral 3 - titanite
    mode[2] = 0.01
    shape[2] = 1
    r[2] = 450
    L[2] = 2 * r[2]
    w[2] = 700
    dx[2] = r[2] / de
    gb[2] = math.ceil(L[2] / dx[2])
    Afac[2] = 0
    Bfac[2] = 0
    Cfac[2] = 3.66
    d180[2] = 99
    D0[2] = 2.05e-8
    Q[2] = 180000
    oxcon[2] = 0.0874

    # mineral 4 - augite
    mode[3] = 0.03
    shape[3] = 1
    r[3] = 30
    L[3] = 2 * r[3]
    w[3] = 30
    dx[3] = r[3] / de
    gb[3] = math.ceil(L[3] / dx[3])
    Afac[3] = 0
    Bfac[3] = 0
    Cfac[3] = 2.75
    d180[3] = 99
    D0[3] = 1.5e-6
    Q[3] = 226000
    oxcon[3] = 0.0892

    # convert input to micron
    L = L * 1e-4
    w = w * 1e-4
    r = r * 1e-4
    dx = dx * 1e-4
    maxdim = max(gb)
    # normalize mineral modes
    mode = mode.copy() / sum(mode)

    # caclculate mineral surface area
    for m in range(0, nmin):
        if shape[m] == 1:
            SA[m] = (4 * pi * pow(r[m], 2))
        else:
            if shape[m] == 2:
                SA[m] = 2 * L[m] * w[m]
            else:
                SA[m] = 2 * upi * r[m] * h[m]

    #initial conditions (starting concentration profiles)
        for m in range(0, nmin):
            fracfax[m] = Afac[m] + ((Bfac[m] * 1e3) / T0) + ((Cfac[m] * 1e6) / pow(T0, 2))

    #recalculate estimated whole rock based on disequilibrium phase (only works
    #for one diseq phase in this formulation; preferrably a low-volume/accessory phase)
    for m in range(0, nmin):
        if d180[m] < 99:
            WRd180 = WRd180 * (1 - mode[m]) + d180[m] * mode

    d180mon = WRd180 + dot(mode, fracfax)
    gbvalinit = zeros([nmin])
    for m in range(0, nmin):
        gbvalinit[m] = d180mon - fracfax[m]
    Told = zeros([nmin, int(max(gb))])
    for m in range(0, nmin):
        if d180[m] == 99:
            Told[m, 0:int(gb[m])] = gbvalinit[m]
        ###################elseif d18O == 100 %load precursor profile from text file
        #################### Told(m) = reshape(load(uigetfile('*.txt')),1,1:gb(m))
        else:
            Told[m, 0:int(gb[m])] = d180[m]

    #### Solve fully implicit
    #####define data storage matrices
    time = zeros([tend])
    Temphx = zeros([tend])
    Tnew = zeros([nmin, int(max(gb))])
    pregbval = zeros([nmin])
    result = zeros([nmin, tend, int(maxdim)])  # array for storing results for all
    # minerals, indices (m,t,i)
    DTdt = zeros([tend])

    loading.config(maximum=int(tend/10))
    for t in range(0, int(tend)):

        if(t%10==0):
          loading.step()
          root.update()
        if cool == 1:
            DTdt = (Tstart - Tend) / ttot  # linear in t
            T = T0 - (DTdt * (t + 1) * dt)
        else:
            k = ttot / ((1 / Tend) - (1 / Tstart))
            T = 1 / ((((t + 1) * dt) / k) + (1 / Tstart))
        D = D0 * exp(-Q / (R * T))
        fracfax = Afac + Bfac * (1e3 / T) + Cfac * (1e6 / pow(T, 2))
        coeff = D / dx
        ###checked to here good #################################################################################
        for m in range(0, nmin):
            if shape[m] == 1:  # spherical/isotropic diffusion geometry
                gb[m] = math.ceil(r[m] / dx[m]) + 1
                a = ones([int(gb[m])])
                a[int(gb[m]) - 1] = 2
                b = (-2 - ((dx[m] * dx[m])) / (D[m] * deltat)) * ones([int(gb[m])])
                c = ones([int(gb[m])])
                c[0] = 2
                d = -((dx[m] * dx[m]) / (D[m] * deltat)) * Told[m, 0:int(gb[m])]
                for i in range(1, int(gb[m]) - 1):
                    a[i] = (i - 1) / i
                    c[i] = (i + 1) / i
            else:  # slab/infinite plane diffusion geometry
                a = ones([int(gb[m])])
                a[int(gb[m]) - 1] = 2
                b = (-2 - ((dx[m] * dx[m])) / (D[m] * deltat)) * ones([int(gb[m])])
                c = ones([int(gb[m])])
                c[0] = 2
                d = -((dx[m] * dx[m]) / (D[m] * deltat)) * Told[m, 0:int(gb[m])]
            TD = diag(b) + diag(a[1:], -1) + diag(c[0:-1], 1)
            Tnew[m, 0:int(gb[m])] = linalg.solve(TD, d)
            pregbval[m] = Tnew[m, int(gb[m]) - 1]

        gbval = fluxbal(nmin, pregbval, coeff, fracfax, mode, SA, oxcon)
        for m in range(0, nmin):
            Tnew[m, int(gb[m]) - 1] = gbval[m]
            if shape[m] == 2:
                Tnew[m, 1] = gbval[m]
            Told[m, :] = Tnew[m, :]
            time[t] = t * dt
            Temphx[t] = T
            result[m, t, 0:int(gb[m])] = Told[m, 0:int(gb[m])]

    if plot1 == 1:
        # loc1 = os.path.dirname(sys.argv[0])
        # loc1 = loc1 + '/HA03_S1_T1.txt'
        loc1 = 'C:/Users/gabe_/Documents/PyCharm/HA03_S1_T1.txt'
        y = result[2, tend - 1, 0:int(gb[2])].reshape(1, int(gb[2]))
        a = octrave(loc1)
        plt.figure(1)
        plt.errorbar(a[0], a[1], a[2], fmt='o')
        u = 471  # distance in m
        u = u * 1e-4
        a = y[0:int(gb[2]) - 1]
        uvec = 1e4 * linspace(u, r[2] + u - dx[2], int(gb[2]))
        plt.plot(uvec, a[0, :], 'k-')
        v = 52
        v = v * 1e-4
        vvec = 1e4 * linspace(v, r[2] + v - dx[2], int(gb[2]))
        plt.plot(vvec, a[0, ::-1], 'k-')

    if plot2 == 1:
        plt.figure(2)
        for t in [0, tend - 2]:
            if t == 0:
                st = 'r-'
            else:
                st = 'b-'

            y = result[:, int(t), :].reshape(int(nmin), int(maxdim))
            for m in range(0, nmin):
                plt.subplot(nmin, 1, m + 1)
                tg = int(gb[m])
                if shape[m] == 1:
                    plt.plot(1e4 * linspace(r[m], 2 * r[m] - dx[m], tg), y[m, 0:tg], st)
                    plt.plot(1e4 * linspace(r[m], dx[m], tg), y[m, 0:tg], st)
                else:
                    plt.plot(1e4 * linspace(dx[m], L[m] - dx[m], tg), y[m, 0:tg], st)

        loading.grid_remove()
        plt.show()
        root.update()









### Create Main Window
root = Tk()
root.title("Diffusion Solver - Fast Grain Boundary Conditions")

## Create subsections of Main Window
# File handler window (import and export)
FileHand = LabelFrame(root, text="Import & Export Model Parameters", bg=background1)
FileHand.config(font=titlefonts)

# Model characteristics window (model characteristics ie runtime cooling rate)
ModelChar = LabelFrame(root, text="Global Model Characteristics", bg=background1)
ModelChar.config(font=titlefonts)

# Rock characteristics window (properties of each mineral ie diffusion and fractionation)
RockChar = LabelFrame(root, text="Properties of Minerals", bg=background1)
RockChar.config(font=titlefonts)

# Graphing options window
GraphChar = LabelFrame(root, text="Graphing Options", bg=background1)
GraphChar.config(font=titlefonts)

#loading bar creation
#mystyle = ttk.Style()
#mystyle.theme_use('clam')
#mystyle.configure("red.Horizontal.TProgressbar", foreground='blue', background='red')
loading = ttk.Progressbar(root, mode='determinate', length='2i', maximum=8000)

# now we create the elements in each of these four subsections of the main window

## File handler elements
importl = Label(FileHand, text="Import")
importl.config(font=fonts2, bg=background1)
importb = StringVar(root)
importb.set("")
Importb = Entry(FileHand, textvariable=importb, width=40, font=fonts2)
Importb.config(font=fonts1)
ImpBut = Button(FileHand, text="Browse", command=importf)
ImpBut.config(font=brs)
exportl = Label(FileHand, text="Export", bg=background1)
exportl.config(font=fonts2)
exportb = StringVar(root)
exportb.set("")
Exportb = Entry(FileHand, textvariable=exportb, width=40, font=fonts2)
Exportb.config(font=fonts1)
ExpBut = Button(FileHand, text="Browse", command=exportf)
ExpBut.config(font=brs)
comm = Frame(FileHand)
runb = Button(comm, text="Run", command=runmain)
runb.config(font=runcmnds)
openb = Button(comm, text="Open", command=readdata)
openb.config(font=runcmnds)
saveb = Button(comm, text="Save", command=writedata)
saveb.config(font=runcmnds)


## Model characteristics elements
coollabel = Label(ModelChar,text="Cooling Type", bg=background1)
coollabel.config(font=fonts2)
cooling = StringVar(root)
cooling.set("Linear")
Cooling = OptionMenu(ModelChar, cooling, "Linear", "Inverse", "Custom")
Cooling.config(font=fonts1, bg="white", relief="sunken", activebackground=bkgr2, bd=1,
               highlightthickness=0)
Cooling["menu"].config(bg="white")

numlabel = Label(ModelChar, text="Minerals", bg=background1)
numlabel.config(font=fonts2)
nummin = IntVar(root)
nummin.set("2")
Nummin = OptionMenu(ModelChar, nummin, "2", "3", "4", "5", "6", "7", "8", command=readjust)
Nummin.config(font=fonts1, bg="white", relief="sunken", activebackground=bkgr2, bd=1,
              highlightthickness=0)
Nummin["menu"].config(bg="white")

durlabel = Label(ModelChar, text="Model Duration", bg=background1)
durlabel.config(font=fonts2)
duration = DoubleVar(root)
duration.set("")
Duration = Entry(ModelChar, textvariable=duration, width=10)

timlabel = Label(ModelChar, text="Time Step", bg=background1)
timlabel.config(font=fonts2)
timestep = DoubleVar(root)
timestep.set("")
Timestep = Entry(ModelChar, textvariable=timestep, width=10, font=fonts1)

wrdlabel = Label(ModelChar, text="Whole Rock", bg=background1)
wrdlabel.config(font=fonts2)
wrd180t = DoubleVar(root)
wrd180t.set("")
Wrd180t = Entry(ModelChar, textvariable=wrd180t, width=10, font=fonts1)

startlabel = Label(ModelChar, text="Starting Temp", bg=background1)
startlabel.config(font=fonts2)
modelstart = DoubleVar(root)
modelstart.set("")
Modelstart = Entry(ModelChar, textvariable=modelstart, width=10, font=fonts1)

endlabel = Label(ModelChar, text="End Temp", bg=background1)
endlabel.config(font=fonts2)
modelend = DoubleVar(root)
modelend.set("")
Modelend = Entry(ModelChar, textvariable=modelend, width=10, font=fonts1)


## Rock characteristics elements
rocks = dict()
Rocks = dict()
rocksl = dict()
for i in range(1,9):
    rocks[i] = dict()
    Rocks[i] = dict()

    rocksl[i] = Label(RockChar, text='Sample '+str(i))
    rocksl[i].config(font=fonts2, bg=background1)
rocksl[1].config(text='Monitor')

for i in range(1,9):
    for j in range(1,12):
        if j in [1,3]:
            rocks[i][j] = StringVar()
        else:
            rocks[i][j] = DoubleVar(root)
            rocks[i][j].set("")
        if j not in [3,6,7,8,9,10]:
         Rocks[i][j] = Entry(RockChar, textvariable=rocks[i][j], width=5, font=fonts1)
        else:
            if j==3:
                rocks[i][j].set('Slab')
                Rocks[i][j] = OptionMenu(RockChar, rocks[i][j], "Slab", "Cylindrical", "Spherical")
                Rocks[i][j].config(font=fonts1, bg="white", relief="sunken", activebackground=bkgr2, bd=1,
                                   highlightthicknes=0)
                Rocks[i][j]["menu"].config(bg="white")

            else:
                Rocks[i][j] = Label(RockChar, textvariable=rocks[i][j], bg='#dedede', relief="sunken", bd=1, font=fonts1)

#################
#################BIG NO NO
#################

rockpropnam=[' Name',' Mode','Shape','  R  ','  W  ','Afrac','Bfrac','Cfrac',' D0 ','  Q  ','Oxcon']
rockproplab = dict()
for i in range(1,12):
    rockproplab[i] = Label(RockChar, text=rockpropnam[i-1])
    rockproplab[i].config(font=fonts2, bg=background1)

#make look up buttons
lookupb = dict()
lookupbb =  dict()
# temporary fix to allow passable arguements
#for i in range(1,9):
#    lookupb[i] = Button(RockChar, text='Frac'+str(i), command = popup_search)
#    #lookupb[i].bind("<Button-1>",popup_search[i])
#    lookupbb[i] = Button(RockChar, text='Diff'+str(i))

lookupb[1] = Button(RockChar, text='Frac1', command= lambda: frac_search(1))
lookupbb[1] = Button(RockChar, text='Diff1', command= lambda: diff_search(1))
lookupb[2] = Button(RockChar, text='Frac2', command= lambda: frac_search(2))
lookupbb[2] = Button(RockChar, text='Diff2', command= lambda: diff_search(2))
lookupb[3] = Button(RockChar, text='Frac3', command= lambda: frac_search(3))
lookupbb[3] = Button(RockChar, text='Diff3', command= lambda: diff_search(3))
lookupb[4] = Button(RockChar, text='Frac4', command= lambda: frac_search(4))
lookupbb[4] = Button(RockChar, text='Diff4', command= lambda: diff_search(4))
lookupb[5] = Button(RockChar, text='Frac5', command= lambda: frac_search(5))
lookupbb[5] = Button(RockChar, text='Diff5', command= lambda: diff_search(5))
lookupb[6] = Button(RockChar, text='Frac6', command= lambda: frac_search(6))
lookupbb[6] = Button(RockChar, text='Diff6', command= lambda: diff_search(6))
lookupb[7] = Button(RockChar, text='Frac7', command= lambda: frac_search(7))
lookupbb[7] = Button(RockChar, text='Diff7', command= lambda: diff_search(7))
lookupb[8] = Button(RockChar, text='Frac8', command= lambda: frac_search(8))
lookupbb[8] = Button(RockChar, text='Diff8', command= lambda: diff_search(8))



## Graphing options elements
GraphChar = LabelFrame(root, text="Graphing Options", bg=background1)
GraphChar.config(font=titlefonts)

Graph1=Checkbutton(GraphChar, text="Graph Option1", font=("helvetica", fonts), bg=background1)
Graph2=Checkbutton(GraphChar, text="Graph Option2", font=("helvetica", fonts), bg=background1)
Graph3=Checkbutton(GraphChar, text="Graph Option3", font=("helvetica", fonts), bg=background1)
Graph4=Checkbutton(GraphChar, text="Graph Option4", font=("helvetica", fonts), bg=background1)


# Now we make the tooltips to explain all buttons and entry fields
createToolTip(numlabel,"Number of minerals in sample")
createToolTip(durlabel, "Duration of model in millions of years")
createToolTip(timlabel, "incremental time step in diffusion solver in milions of years, ie 5e-6")
createToolTip(coollabel, "This creates temperature profile")
createToolTip(startlabel, "Beginning temperature in C")
createToolTip(endlabel, "Ending temperature in C")
createToolTip(wrdlabel, "Estimate of whole rock")

for i in range(1,12):
    createToolTip(rockproplab[i], "Explanation of "+rockpropnam[i-1]+" parameter")

for i in range(1,9):
    createToolTip(rocksl[i], "Properties of mineral sample "+str(i))

createToolTip(runb, "Run model with current parameters")
createToolTip(openb, "Import parameters from previously saved file in import")
createToolTip(saveb, "Save current parameters to file in export")

#Now we place everything on the main window

#place main frames
FileHand.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, stick=W+E)
ModelChar.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, stick=W+E)
RockChar.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, stick=W+E)
GraphChar.grid(row=0, column=2, rowspan=3, padx=5, pady=5, ipadx=5, ipady=5, stick=N+S)



#place everything file frame
importl.grid(row=0, column=1)
Importb.grid(row=0, column=2)
ImpBut.grid(row=0,column=3)

exportl.grid(row=1, column=1)
Exportb.grid(row=1, column=2)
ExpBut.grid(row=1,column=3)

comm.grid(row=2, column=1, columnspan=1, pady=(10,0), padx=(10,0))
runb.grid(row=0, column=3)
openb.grid(row=0, column=1)
saveb.grid(row=0, column=2)

wt=10
t1=10
t2=20
t3=20

#place everything in model frame
numlabel.grid(row=0, column=1, stick=E, padx=(t1,0))
Nummin.grid(row=0, column=2, stick=W+E, padx=(wt,0))

durlabel.grid(row=0, column=3, stick=E, padx=(t2,0))
Duration.grid(row=0, column=4, stick=W+E, padx=(wt,0))

timlabel.grid(row=0, column=5, stick=E, padx=(t3,0))
Timestep.grid(row=0, column=6, stick=W+E, padx=(wt,0))

coollabel.grid(row=1, column=1, stick=E, padx=(t1,0))
Cooling.grid(row=1, column=2, stick=W+E, padx=(wt,0))

startlabel.grid(row=1, column=3, stick=E, padx=(t2,0))
Modelstart.grid(row=1, column=4, stick=W+E, padx=(wt,0))

endlabel.grid(row=1, column=5, stick=E, padx=(t3,0))
Modelend.grid(row=1, column=6, stick=W+E, padx=(wt,0))

wrdlabel.grid(row=2, column=1, stick=E, padx=(t1,0))
Wrd180t.grid(row=2, column=2, stick=W+E, padx=(wt,0))




#place everything rock frame

for i in range(1,9):
  rocksl[i].grid(row=i, column=1)
for i in range(1,12):
  rockproplab[i].grid(row=0, column=i+1+(i>8)+(i==11))

for i in range(1,9):
    for j in range(1,12):
        Rocks[i][j].grid(row=i, column=j+1+(j>8)+(j==11), stick=N+S+W+E)

for i in range(1,9):
    lookupb[i].grid(row=i, column=10)
    lookupbb[i].grid(row=i, column=13)

readjustn()

Graph1.grid(row=1, column=0)
Graph2.grid(row=2, column=0)




# start main loop
root.config(bg=background1)
root.mainloop()
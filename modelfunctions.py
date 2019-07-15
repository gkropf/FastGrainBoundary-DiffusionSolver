import time as systime
from numpy import *
from tkinter import ttk
import pandas
from scipy import interpolate
from scipy import optimize
import matplotlib.pyplot as plt
import os

# This is the main diffusion solver function that uses python, this results in a 3d array that has the
# output at every timestep.
def forwardmodel_slow(mainapp):

    #read parameters and create loading bar
    loadingbar=ttk.Progressbar(mainapp.page1.graphingframe, mode='determinate', length='2i', maximum=1000)
    loadingbar.grid(row=20, column=0, padx=(5,0), pady=(50,5), sticky='sw')
    params=mainapp.page1.forwardparams
    mainapp.update()

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


    # get user defined info
    ttot = float(params['ModelDuration'].get())
    dt = float(params['TimeStep'].get())
    WRd180 = float(params['WholeRock'].get())
    Tstart = float(params['StartingTemp'].get())
    Tend = float(params['EndTemp'].get())
    nmin = int(params['NumMinerals'].get())
    de = 100

    cool_file=params['CoolingFile'].get()
    if params['CoolingType'].get() == "Custom":
        # read data in as matrix without using pandas
        file = open(cool_file, 'r', encoding='ISO-8859-1')
        raw = file.read()
        raw_lines = raw.split('\n')
        raw_data = [x.split(',') for x in raw_lines[0:-1]]
        segs = array([[float(x) for x in y] for y in raw_data])

        # compute cooling steps
        [rw, cl] = segs.shape;
        segtimes = divide(segs[:, 0], dt)
        segtimes = [int(round(x)) for x in segtimes]
        SegDTdt = []
        for p in range(0, rw):
            thisseg = ones(segtimes[p]) * segs[p][1]
            SegDTdt = concatenate((SegDTdt, thisseg))
        tend = sum(segtimes);
        ttot = tend * dt;

    # unit definitions and converions
    deltat = dt * 3.1536e+13
    tend = math.ceil(ttot / dt)
    Tstart = Tstart + 273
    Tend = Tend + 273
    T0 = Tstart
    T = Tstart

    # initialize storage matrices
    mode = zeros([nmin])
    shape = zeros([nmin]).astype(int)
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

    for j in range(0, nmin):
        mode[j] = float(params['Min' + str(j) + '-Mode'].get())
        if params['Min' + str(j) + '-Shape'].get() == "Spherical":
            shape[j] = 1
        if params['Min' + str(j) + '-Shape'].get() == "Slab":
            shape[j] = 2
        r[j] = params['Min' + str(j) + '-R'].get()
        L[j] = 2 * r[j]
        w[j] = params['Min' + str(j) + '-W'].get()
        dx[j] = r[j] / de
        gb[j] = math.ceil(L[j] / dx[j])
        Afac[j] = params['Min' + str(j) + '-Afrac'].get()
        Bfac[j] = params['Min' + str(j) + '-Bfrac'].get()
        Cfac[j] = params['Min' + str(j) + '-Cfrac'].get()
        D0[j] = params['Min' + str(j) + '-Dparam1'].get()
        Q[j] = params['Min' + str(j) + '-Dparam2'].get()
        oxcon[j] = params['Min' + str(j) + '-Oxcon'].get()
        d180[j] = 99

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
            SA[m] = 2 * L[m] * w[m]


        # initial conditions (starting concentration profiles)
        for m in range(0, nmin):
            fracfax[m] = Afac[m] + ((Bfac[m] * 1e3) / T0) + ((Cfac[m] * 1e6) / pow(T0, 2))

    # recalculate estimated whole rock based on disequilibrium phase (only works
    # for one diseq phase in this formulation; preferrably a low-volume/accessory phase)
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
        else:
            Told[m, 0:int(gb[m])] = d180[m]

    #### Solve fully implicit
    #####define data storage matrices
    time = zeros([tend])
    Temphx = zeros([tend])
    Tnew = zeros([nmin, int(max(gb))])
    pregbval = zeros([nmin])
    result = zeros([nmin, tend, int(maxdim)])  # array for storing results for all

    loadingbar.config(maximum=int(tend / 10))
    for t in range(0, int(tend)):

        if (t % 10 == 0):
            loadingbar.step()
            mainapp.update()
        if params['CoolingType'].get() == "Linear":
            DTdt = (Tstart - Tend) / ttot  # linear in t
            T = T0 - (DTdt * (t + 1) * dt)
        elif params['CoolingType'].get() == "Inverse":
            k = ttot / ((1 / Tend) - (1 / Tstart))
            T = 1 / ((((t + 1) * dt) / k) + (1 / Tstart))
        else:
            DTdt = SegDTdt[t];
            T = T - (DTdt * dt);

        D = D0 * exp(-Q / (R * T))
        fracfax = Afac + Bfac * (1e3 / T) + Cfac * (1e6 / pow(T, 2))
        coeff = D / dx

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

    # create global variables to store results in
    loadingbar.destroy()
    global yresult, timeresult, xresult
    yresult = result
    xsteps = yresult.shape[2]
    xresult = zeros((xsteps, nmin))
    timeresult = linspace(0, 1, yresult.shape[1]) * ttot
    for i in range(0, nmin):
        if shape[i] == 1:
            xresult[:, i] = 1e4 * linspace(dx[i], 2 * r[i] - dx[i], xsteps)
            onesidey = result[i, :, 0:int(xsteps / 2)]
            yresult[i, :, 0:2 * int(xsteps / 2)] = concatenate((onesidey[:, ::-1], onesidey), axis=1)
        else:
            xresult[:, i] = 1e4 * linspace(dx[i], L[i] - dx[i], xsteps)

    #print(systime.time() - start_time)
    #print(array(xresult).shape)
    #print(array(yresult).shape)
    #print(array(timeresult).shape)


    return xresult, yresult, timeresult


# This is the main diffusion solver that uses C, this results in a 2d array that has only the last time step.
def forwardmodel_fast(file_param,cool_array):

    unique_ID=1
    df=pandas.DataFrame(cool_array)
    df.to_csv(str(unique_ID)+".txt", sep=",", header=None, index=None)

    os.system("./Cmodel/RunModel "+file_param+" "+str(unique_ID)+".txt "+str(unique_ID)+"X.txt "+str(unique_ID)+"Y.txt")

    #now read input from C code output
    X=pandas.read_csv(str(unique_ID)+"X.txt", sep=',', header=None).values
    Y=pandas.read_csv(str(unique_ID)+"Y.txt", sep=',', header=None).values

    #remove text files that have been created
    os.system("rm 1.txt")
    os.system("rm 1Y.txt")
    os.system("rm 1X.txt")


    return X, Y



# These are all the functions for computing the inverse solution
def calc_single_diffs(xmod, ymod, error_file):

    # compute traverse for file
    def octrav(error_file):
        replacedat = pandas.read_csv(error_file, sep=' ', header=None).values

        return replacedat[:,0], replacedat[:,1], replacedat[:,2]

    xactual, yactual, uncert = octrav(error_file)

    # keep only right hand side, and where values are in range of model change to mean for actual
    ind_keep = [i for i in range(len(xactual)) if xactual[i] > 0 and xactual[i] < xmod[-1]]
    xactual = xactual[ind_keep]
    yactual = yactual[ind_keep]
    uncert = uncert[ind_keep]

    if len(ind_keep)>0:
        # find interpolation for each point
        coef=interpolate.splrep(xmod,ymod)
        y_corr=interpolate.splev(xactual,coef)

        #return differences divided by sigma
        diff = divide(y_corr-yactual,uncert)
    else:
        diff=[]

    return list(diff)


def calc_residuals(mainapp,cool_array,reg_alpha):

    # record all difference from each mineral within each sample
    D_total=[]
    for i in mainapp.page2.forwardmods:

        # if cool history has negative temps give high residuals
        if any(cool_array[:,1]<100):
            fakecool=array([[0,700],[1,500]])
            xdata, ydata = forwardmodel_fast(mainapp.page2.forwardmodelframe.forwardmodels_var[i].get(), fakecool)
            ydata = ydata+300
        else:
            xdata, ydata = forwardmodel_fast(mainapp.page2.forwardmodelframe.forwardmodels_var[i].get(), cool_array)

        for k in range(0,8):
            error_file=mainapp.page2.errorfileframe.errfile_var[(i,k)].get()
            if error_file:
                D_total=D_total+calc_single_diffs(xdata[:,k],ydata[:,k],error_file)

    residuals=array(D_total).reshape((-1,1))+(.33/25)*(499-min(min(cool_array[:,1]),499))**2

    # compute regularization term for cooling history
    N = len(residuals)
    m = len(cool_array)

    #create L matrix to be used as constraint, currently constructed to penalize 2nd derivative
    L=zeros((m-2,m))
    for i in range(0,m-2):
        L[i,i:i+3]=[1, -2, 1]

    #stack to make K vector
    res=vstack((residuals,matmul(reg_alpha*L,cool_array[:,1]).reshape(-1,1)))
    return res.reshape(N+m-2)


def calc_jacob(mainapp,cool_array,curr_res,reg_alpha,past_SSE,past_aLm):

    # Calculate current sse and smoothness
    m=len(cool_array)
    curr_res=calc_residuals(mainapp,cool_array,reg_alpha)
    curr_SSE=sum(curr_res[0:-(m-2)]**2)
    curr_aLm=sum(curr_res[-(m-2):]**2)
    past_SSE.append(curr_SSE)
    past_aLm.append(curr_aLm)

    # Update progress figures
    mainapp.page2.progwind.line11.set_data(cool_array[:,0],cool_array[:,1])
    mainapp.page2.progwind.line12.set_data(cool_array[:,0],cool_array[:,1])
    limx1, limx2 = min(cool_array[:,0]), max(cool_array[:,0])
    limy1, limy2 = min(cool_array[:,1]), max(cool_array[:,1])

    mainapp.page2.progwind.ax1.set_ylim([limy1-.03*limy2, 1.03*limy2])
    mainapp.page2.progwind.ax1.set_xlim([limx1-.03*limx2, 1.03*limx2])

    # Update 30 most recent objective values into bar plot. The bar graph does not have a built in function
    # to update the number of entries.
    num_iter=len(past_SSE)
    if num_iter<31:
        for i in range(len(past_SSE)):
            mainapp.page2.progwind.bar2[i].set_height(past_SSE[i]+past_aLm[i])
            mainapp.page2.progwind.bar2[i].set_height(past_SSE[i])
    else:
        for i in range(num_iter-30,num_iter):
            k = i+(num_iter-30)
            mainapp.page2.progwind.bar2[i].set_height(past_SSE[k]+past_aLm[k])
            mainapp.page2.progwind.bar2[i].set_height(past_SSE[k])


    mainapp.page2.progwind.canvas1.draw()
    mainapp.page2.progwind.canvas2.draw()
    mainapp.update()

    N=len(curr_res)
    deltac=1;

    J=zeros([N,m-2])
    for i in range(1,m-1):
        mainapp.page2.progwind.calc_var.set("calculating Jacobian column "+str(i)+" of "+str(m-2))
        mainapp.update()
        new_cool=cool_array.copy()
        new_cool[i,1]=new_cool[i,1]+deltac
        deriv=(calc_residuals(mainapp,new_cool,reg_alpha)-curr_res)/deltac
        J[:,i-1]=deriv.reshape(N)

    return J


# This function runs the inverse solver for the minerals, initial profiles given
def find_inverses(mainapp):

    alpha=0.04032227

    for i in range(0,mainapp.page2.num_initials):
        if (mainapp.page2.initsolutions.initial_vars[i].get()==1):
            file_loc=mainapp.page2.initsolutions.folder_var.get()+mainapp.page2.initsolutions.initial_labs[i].get()
            initial_sol=pandas.read_csv(file_loc, sep=',', header=None).values
            m=len(initial_sol)


            # Calculate initial residuals and smoothness, and create progress plots that will be updated
            # each time the Jac function is called.
            initial_res=calc_residuals(mainapp,initial_sol,alpha)
            initial_SSE=sum(initial_res[0:-(m-2)]**2)
            initial_aLm=sum(initial_res[-(m-2):]**2)

            past_sse=[initial_SSE]
            past_aLm=[initial_aLm]
            mainapp.page2.create_progwind(mainapp,initial_sol,initial_SSE,initial_aLm)
            mainapp.page2.progwind.init_var.set("Running LM algorithm with starting solution: /"+
                                                mainapp.page2.initsolutions.initial_labs[i].get())




            # Create residual and jacobian function that accepts single array as input (for built in optimize function)
            def usey_residuals(cool_y):
                full_soln=initial_sol.copy()
                full_soln[1:-1,1]=cool_y
                return calc_residuals(mainapp, full_soln, alpha)

            def usey_jacob(soln_y):
                full_soln=initial_sol.copy()
                full_soln[1:-1,1]=soln_y
                curr_res=calc_residuals(mainapp, full_soln, alpha)
                return calc_jacob(mainapp, full_soln, curr_res, alpha, past_sse, past_aLm)

            # Now find solution and convert it back into 2D array
            initial_solny=initial_sol[1:-1,1].copy()
            sol=optimize.least_squares(usey_residuals, initial_solny , jac=usey_jacob, method='lm', gtol=1e-9)
            final_sol=initial_sol.copy()
            final_sol[1:-1,1]=sol.x

            # Save final solution to Outputs folder
            final_df = pandas.DataFrame(final_sol)
            final_df.columns = ['Time', 'Temperature']
            save_location = 'Output/'+mainapp.page2.initsolutions.initial_labs[i].get()[:-4]+'_results_in_this_sol.csv'
            final_df.to_csv(save_location, header=True, index=None)
            
            # Calculate objective values and SSE
            final_res=calc_residuals(mainapp,final_sol,alpha)
            final_SSE=sum(final_res[0:-(m-2)]**2)
            final_aLm=sum(final_res[-(m-2):]**2)

            # Get magnitude of final gradient function
            K=calc_jacob(mainapp,final_sol,calc_residuals(mainapp,final_sol,alpha),alpha,past_sse,past_aLm)
            Kmag=linalg.norm(matmul(transpose(K),final_res))
            mainapp.page2.progwind.destroy()







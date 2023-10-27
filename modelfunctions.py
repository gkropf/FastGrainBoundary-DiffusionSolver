import matplotlib
matplotlib.use("TkAgg")
import time as systime
from numpy import *
from tkinter import ttk
import pandas
from scipy import interpolate
from scipy import optimize
import matplotlib.pyplot as plt
import os
import subprocess

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
        print(rw)
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
    # print(array(xresult).shape)
    #print(array(yresult).shape)
    #print(array(timeresult).shape)

    return xresult, yresult, timeresult


# This is the main diffusion solver that uses C, this results in a 2d array that has only the last time step.
def forwardmodel_fast(file_param,cool_array):

    unique_ID=1
    df=pandas.DataFrame(cool_array)
    df.to_csv(str(unique_ID)+".txt", sep=",", header=None, index=None)

    # Check if RunModel has already been compiled or not, if not it compiles it.
    if os.path.exists("./Cmodel/RunModel") == True:
    	os.system("./Cmodel/RunModel "+file_param+" "+str(unique_ID)+".txt "+str(unique_ID)+"X.txt "+str(unique_ID)+"Y.txt")
    else:
    	os.system("gcc -Wall -o ./Cmodel/RunModel ./Cmodel/RunForwardModel.c")
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
        diff = y_corr-yactual
    else:
        diff=[]

    return list(diff)


def calc_residuals(mainapp,cool_array):

    # record all difference from each mineral within each sample
    Diff_total=[]
    for i in mainapp.page2.forwardmods:

        # if cool history has negative temps give high residuals
        if any(cool_array[:,1]<100):
            fakecool=array([[0,700],[1,500]])
            xdata, ydata = forwardmodel_fast(mainapp.page2.forwardmodelframe.forwardmodels_var[i].get(), fakecool)
            ydata = ydata+300
        else:
            xdata, ydata = forwardmodel_fast(mainapp.page2.forwardmodelframe.forwardmodels_var[i].get(), cool_array)
        Output_x = pandas.DataFrame(xdata)
        Output_x.to_csv('Output_x' + str(i) + '.csv')
        Output_y = pandas.DataFrame(ydata)
        Output_y.to_csv('Output_y' + str(i) + '.csv')


        for k in range(0,8):
            error_file=mainapp.page2.errorfileframe.errfile_var[(i,k)].get()
            if error_file:
                Diff_total = Diff_total + calc_single_diffs(xdata[:,k],ydata[:,k],error_file)


    # residuals=array(D_total).reshape((-1,1))+(.33/25)*(499-min(min(cool_array[:,1]),499))**2

    # # compute regularization term for cooling history
    # N = len(residuals)
    # m = len(cool_array)

    # #create L matrix to be used as constraint, currently constructed to penalize 2nd derivative
    # L=zeros((m-2,m))
    # for i in range(0,m-2):
    #     L[i,i:i+3]=[1, -2, 1]

    # #stack to make K vector
    # res=vstack((residuals,matmul(reg_alpha*L,cool_array[:,1]).reshape(-1,1)))
    return Diff_total


# def calc_jacob(mainapp,cool_array,curr_res,reg_alpha,past_SSE,past_aLm):

#     # Calculate current sse and smoothness
#     m=len(cool_array)
#     curr_res=calc_residuals(mainapp,cool_array,reg_alpha)
#     curr_SSE=sum(curr_res[0:-(m-2)]**2)
#     curr_aLm=sum(curr_res[-(m-2):]**2)
#     past_SSE.append(curr_SSE)
#     past_aLm.append(curr_aLm)

#     # Update progress figures
#     mainapp.page2.progwind.line11.set_data(cool_array[:,0],cool_array[:,1])
#     mainapp.page2.progwind.line12.set_data(cool_array[:,0],cool_array[:,1])
#     limx1, limx2 = min(cool_array[:,0]), max(cool_array[:,0])
#     limy1, limy2 = min(cool_array[:,1]), max(cool_array[:,1])

#     mainapp.page2.progwind.ax1.set_ylim([limy1-.03*limy2, 1.03*limy2])
#     mainapp.page2.progwind.ax1.set_xlim([limx1-.03*limx2, 1.03*limx2])

#     # Update 30 most recent objective values into bar plot. The bar graph does not have a built in function
#     # to update the number of entries.
#     num_iter=len(past_SSE)
#     if num_iter<31:
#         for i in range(len(past_SSE)):
#             mainapp.page2.progwind.bar2[i].set_height(past_SSE[i]+past_aLm[i])
#             mainapp.page2.progwind.bar2[i].set_height(past_SSE[i])
#     else:
#         for i in range(num_iter-30,num_iter):
#             k = i+(num_iter-30)
#             mainapp.page2.progwind.bar2[i].set_height(past_SSE[k]+past_aLm[k])
#             mainapp.page2.progwind.bar2[i].set_height(past_SSE[k])


#     mainapp.page2.progwind.canvas1.draw()
#     mainapp.page2.progwind.canvas2.draw()
#     mainapp.update()

#     N=len(curr_res)
#     deltac=1;

#     J=zeros([N,m-2])
#     for i in range(1,m-1):
#         mainapp.page2.progwind.calc_var.set("calculating Jacobian column "+str(i)+" of "+str(m-2))
#         mainapp.update()
#         new_cool=cool_array.copy()
#         new_cool[i,1]=new_cool[i,1]+deltac
#         deriv=(calc_residuals(mainapp,new_cool,reg_alpha)-curr_res)/deltac
#         J[:,i-1]=deriv.reshape(N)

#     return J

def check_rate(cool_new, params):
    """ Check that the rates of heating or cooling isn't higher that 100 degC/Ma """

    # Get the time between each point
    dt = (cool_new[-1,0] - cool_new[0,0]) / len(cool_new)

    # Reads params
    i = params['iteration']
    u = params['u']
    sigma = params['sigma']

    # Check the rate by comparing the selected point 
    point_i = cool_new[i,1] + u * sigma
    point_ip = cool_new[i+1,1]
    point_im = cool_new[i-1,1]

    if sqrt(((point_im - point_i) / dt)**2) >= 100 or sqrt(((point_i - point_ip) / dt)**2) >= 100:
        print('Looks like the cooling was too high')
        return True
    else:
        print('Looks like the cooling was fine')
        return False

def transition_model(cool_array, mainapp, iteration):
    ### The tranistion model defines how to move temperature points for the ttermal history###
    move_selection = 1

    # move_selection = random.randint(1,3)  # Randomly select the modification of the cooling history
    if move_selection == 1:
    # Move temperature for a point
        m=len(cool_array)
        sigma = random.normal(0,1)
        i = random.randint(1,m-1)
        cool_new=cool_array.copy()
        u = 10
        params = {'iteration' : i,'u' : u, 'sigma' : sigma}
        cool_new[i,1]=cool_new[i,1] + u * sigma

    elif move_selection == 2:
    # Add a T-t point
        cool_new[i,1]=cool_new[i,1] + u * sigma

    elif move_selection ==3:
    # Remove a T-t point
        cool_new[i,1]=cool_new[i,1] + u * sigma


    return cool_new, params


def prior(cool):
    ### Computes the prior ratio
    dT = []
    for i in range(len(cool)-1):
        dT.append((cool[i+1,1] - cool[i,1])**2)
    # prior_move_T = 1 / (max(cool[:,1]) - min(cool[:,1]))
    prior_move_T = 1 / (sum(dT))
    print(prior_move_T)

    return prior_move_T


def manual_log_like_normal(diff, error):
    ###Computes the likelihood of the data given a sigma (new or current) according to equation (2)
    LL = []
    pyi = 3.141592653589793
    for i in range(len(diff)):
        LL.append(-log(error[i] * sqrt(2 * pyi))-0.5*(((diff[i]))**2) / ((error[i]**2)))

    return sum(LL)


#Defines whether to accept or reject the new sample
def acceptance(cool_array, new_cool):
    if new_cool>cool_array:
        return True
    else:
        # return False
        accept=random.uniform(0,1)
        if accept >= 0.25:
            return False
        else:
            return True


def reduced_chi2(diff, error, cool_array):
    """ Computes the MSWD or reduced chi2 at each iteration using 
    the difference between measured andmodelled values and the error on the measured value"""
    chi2 = []
    for i in range(len(diff)):
        chi2.append((diff[i] / error[i]) ** 2)
    MSWD = sum(chi2)/(len(diff) - len(cool_array))

    return MSWD


def error_function(error_file):

    for k in range(0,8):
        error_file=mainapp.page2.errorfileframe.errfile_var[(i,k)].get()
        if error_file:
            Uncert = Uncert + calc_single_diffs(xdata[:,k],ydata[:,k],error_file)

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

        return uncert


def metropolis_hastings(likelihood_computer,prior, transition_model, init_Tt, iterations, mainapp, acceptance_rule):
    # likelihood_computer(residuals,uncertainties): returns the likelihood that this thermal history produced the oxygenisotope zoning
    # transition_model(x): a function that draws a sample from a symmetric distribution and returns it
    # iterations: number of accepted to be generated
    # acceptance_rule(cool,cool_new): decides whether to accept or reject the new thermal history
    cool_array = init_Tt
    diff = calc_residuals(mainapp, cool_array)
    uncert = 0.14 * ones((len(diff), 1))
    cool_accepted = []
    cool_rejected = []
    MSWD_accepted = []
    MSWD_rejected = []
    log_like = []
    prior_list = []
    i_accepted = []
    i_rejected = []
    cool_post_burnin = []
    for i in range(iterations):
        cool_new, params =  transition_model(cool_array, mainapp, i)
        cool_post_burnin.append(cool_new)
        new_diff = calc_residuals(mainapp, cool_new)
        MSWD = reduced_chi2(diff, uncert, cool_new)
        cool_lik = likelihood_computer(diff, uncert)
        log_like.append(cool_lik)
        prior_list.append(prior(cool_array))
        cool_new_lik = likelihood_computer(new_diff, uncert)
        if (acceptance_rule(cool_lik + log(prior(cool_array)),cool_new_lik + log(prior(cool_new)))):        
            cool_array = cool_new
            diff = new_diff
            cool_accepted.append(cool_new)
            MSWD_accepted.append(MSWD)
            i_accepted.append(i)
        else:
            cool_rejected.append(cool_array)
            MSWD_rejected.append(MSWD)
            i_rejected.append(i)   
                
    return array(cool_accepted), array(cool_rejected), array(MSWD_accepted), array(MSWD_rejected), i_accepted, i_rejected, array(cool_post_burnin), log_like, prior_list

# This function runs the inverse solver for the minerals, initial profiles given
def find_inverses(mainapp):

    for i in range(0,mainapp.page2.num_initials):
        if (mainapp.page2.initsolutions.initial_vars[i].get()==1):
            file_loc=mainapp.page2.initsolutions.folder_var.get()+mainapp.page2.initsolutions.initial_labs[i].get()
            initial_sol=pandas.read_csv(file_loc, sep=',', header=None).values

    nb_iterations = 20000
    cool_accepted, cool_rejected, MSWD_accepted, MSWD_rejected, i_accepted, i_rejected, cool_post_burnin, log_likelihood, prior_list = metropolis_hastings(manual_log_like_normal,prior,transition_model,initial_sol,nb_iterations,mainapp,acceptance)


    fig = plt.figure(figsize=(15,8))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    for i in range(len(cool_post_burnin)):
        t_post = []
        T_post = []
        for j in range(len(cool_post_burnin[i])):
            t_post.append(cool_post_burnin[i][j,0])
            T_post.append(cool_post_burnin[i][j,1])
        ax1.plot(t_post,T_post, 'k--', label='accepted')
        if i == 0:
            Data_post = pandas.DataFrame({'Time' : t_post, 'T_cool0' : T_post})
        else:
            Data_post = Data_post.assign(T_cool=T_post)
            Data_post = Data_post.rename(columns={'T_cool' : 'T_cool' + str(i+1)})
    Data_post.to_csv('Data_post_Burn-in.csv', index=False)
    Data_log_LL = pandas.DataFrame({'Iteration' : range(nb_iterations), 'Log_LL' : log_likelihood, 'Prior' : prior_list})
    Data_log_LL.to_csv('Log_Likelihood.csv', index=False)
    ax2.scatter(range(nb_iterations), log_likelihood)
    ax2.set_xlabel('Iteration #')
    ax2.set_ylabel('Log likelihood')
    init_t = []
    init_T = []
    for j in range(len(initial_sol)):
        init_t.append(initial_sol[j,0])
        init_T.append(initial_sol[j,1])
    ax1.plot(init_t,init_T, 'b--', label='initial')
    ax1.set_ylabel("Temperature (˚C)")
    ax1.set_xlabel("Time (Ma)")
    plt.show()



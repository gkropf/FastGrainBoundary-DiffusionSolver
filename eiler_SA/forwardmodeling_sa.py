# ===============================================================================
# Copyright 2019 Gabriel Kropf and Gabriel Parrish
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
from numpy import *
from tkinter import ttk
import pandas
from scipy import interpolate
from scipy import optimize
import matplotlib.pyplot as plt
import os
# ============= standard library imports ========================
from modelfunctions import forwardmodel_fast, forwardmodel_slow, find_inverses




def forward_model_slow_bulk(params):

    """
    A forward model implementation that accepts a dictionary params based on a standard params .txt file
    :param params: Dictionary
    :return: 3 arrays of the model results
    """

    print('running forward model slow bulk for params file: {}'.format(params))

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

    # get user defined info TODO - remove .get() method
    ttot = float(params['ModelDuration'])
    dt = float(params['TimeStep'])
    WRd180 = float(params['WholeRock'])
    Tstart = float(params['StartingTemp'])
    Tend = float(params['EndTemp'])
    nmin = int(params['NumMinerals'])
    de = 100

    cool_file = params['CoolingFile']
    print('cool file is {}'.format(cool_file))
    if params['CoolingType'] == "Custom":
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
        mode[j] = float(params['Min' + str(j) + '-Mode'])
        if params['Min' + str(j) + '-Shape'] == "Spherical":
            shape[j] = 1
        if params['Min' + str(j) + '-Shape'] == "Slab":
            shape[j] = 2
        r[j] = params['Min' + str(j) + '-R']
        L[j] = 2 * r[j]
        w[j] = params['Min' + str(j) + '-W']
        dx[j] = r[j] / de
        gb[j] = math.ceil(L[j] / dx[j])
        Afac[j] = params['Min' + str(j) + '-Afrac']
        Bfac[j] = params['Min' + str(j) + '-Bfrac']
        Cfac[j] = params['Min' + str(j) + '-Cfrac']
        D0[j] = params['Min' + str(j) + '-Dparam1']
        Q[j] = params['Min' + str(j) + '-Dparam2']
        oxcon[j] = params['Min' + str(j) + '-Oxcon']
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

    # loadingbar.config(maximum=int(tend / 10))
    for t in range(0, int(tend)):

        # if (t % 10 == 0):
        #     loadingbar.step()
        #     mainapp.update()
        if params['CoolingType'] == "Linear":
            DTdt = (Tstart - Tend) / ttot  # linear in t
            T = T0 - (DTdt * (t + 1) * dt)
        elif params['CoolingType'] == "Inverse":
            k = ttot / ((1 / Tend) - (1 / Tstart))
            T = 1 / ((((t + 1) * dt) / k) + (1 / Tstart))
        else:
            # print('SegDTdt[t]')
            # SegDTdt = []
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
    # loadingbar.destroy()
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

    # print(systime.time() - start_time)
    # print(array(xresult).shape)
    # print(array(yresult).shape)
    # print(array(timeresult).shape)

    return xresult, yresult, timeresult

def write_params_file(params_dict, output_path, filename):
    """
    The script outputs a .txt parameter file that can be read by make_params_dict() function
    :param params_dict: dictionary of standard DiffuisionSolver parameters
    :param output_path: a string showing the location of the directory the file should go to
    :param filename: string naming the .txt_file
    :return:
    """

    # todo - make this ordered rather than dict based

    wpath = os.path.join(output_path, '{}.txt'.format(filename))

    with open(wpath, 'w') as wfile:
        for k, v in params_dict.items():
            wfile.write('{},{}\n'.format(k, v))

def make_params_dict(params):
    """

    :param params: a path to a standard formatted .txt file such as is output
     from save parameters function in DiffusionSolver
    :return: dictionary of the model parameters to be used in forward_model_slow_bulk()
    """

    fwd_model_parameters = {}

    with open(params, 'r') as rfile:
        for line in rfile:
            # print('{}'.format(line))
            param_val = line.split(',')
            # print('param {}  value {}'.format(param_val[0], param_val[1]))
            fwd_model_parameters[param_val[0]] = param_val[1][0:-1]

    print(fwd_model_parameters['CoolingType'])
    print(len(fwd_model_parameters['CoolingType']))

    return fwd_model_parameters

def find_nearest(array, value):
    """
    Get the index of the value nearest another value in numpy array
    :param array:
    :param value:
    :return:
    """
    array = asarray(array)
    idx = (abs(array - value)).argmin()
    return idx

def generate_synthetic_data(x_arr, y_arr, noise, sample_locations, output_location, output_name):
    """

    :param x_arr: distance across lattice
    :param y_arr: from late time
    :param noise: as a decimal
    :param sample_locations: a list of distances in cm where we grab samples as distances from the end of the crystal
    :return:
    """

    print(x_arr)
    print('noise {}'.format(noise))
    print('sample locations {}'.format(sample_locations))

    print(x_arr.shape)
    print(y_arr.shape)

    yvals = []
    xvals = []
    for val in sample_locations:
        min_indx = find_nearest(x_arr, val)
        yvals.append(y_arr[min_indx])
        xvals.append(x_arr[min_indx])

    print('yvals {}'.format(yvals))
    print('xvals {}'.format(xvals))

    yvals = array(yvals)
    xvals = array(xvals)

    # Add noise
    #
    noise_arr = random.normal(0.0, noise, len(yvals))
    print('noise arr \n {}'.format(noise_arr))
    yvals_noise = yvals + (yvals * noise_arr)
    print('noisy yvals \n {}'.format(yvals_noise))

    uncertainty = full(noise_arr.shape, noise)


    # write the noisy file to a txt file

    wfilepath = os.path.join(output_location, '{}_sampled_noisy.txt'.format(output_name))

    with open(wfilepath, 'w') as wfile:

        for d, o, un in zip(xvals, yvals, uncertainty):
            wfile.write('{} {} {}\n'.format(d, o, un))

    print('done writing to {}'.format(wfilepath))






if __name__ == "__main__":

    # path to the paramter style file
    chloe_model_params = '/Users/dcadol/Desktop/academic_docs_II/FGB_model/JohnEiler/Eiler94_Amphibolite.txt'

    fwd_model_parameters = make_params_dict(params=chloe_model_params)

    xresult, yresult, timeresult = forward_model_slow_bulk(fwd_model_parameters)

    print(array(xresult).shape)
    print(array(yresult).shape)
    print(array(timeresult).shape)


    # TODO - Find a way to store these and then do the visualizations...
    # For now just store them as .npy arrays
    filename = os.path.split(chloe_model_params)[1]
    output = os.path.split(chloe_model_params)[0]
    save_tag = filename.split('.')[0]

    # Save each array as a .npy file
    save(os.path.join(output, '{}_x.npy'.format(save_tag)), xresult)
    save(os.path.join(output, '{}_y.npy'.format(save_tag)), yresult)
    save(os.path.join(output, '{}_time.npy'.format(save_tag)), timeresult)


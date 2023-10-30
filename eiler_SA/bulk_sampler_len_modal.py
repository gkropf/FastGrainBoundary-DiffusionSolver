import os
import numpy as np
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file, sample_locator, generate_synthetic_data

file_root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/modality_len_results_fwd/'
# HORNBLENDE
horn_output_location = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/full_sampled/hornblende'
# sample_mineral = 'horn'
# PLAG
plag_output_location= '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/full_sampled/plagioclase'
# sample_mineral = 'plag'
# 0.3 - base case

plagioclase_mode_start = 0.1
# 0.6 - base case
hornblende_mode_start = 0.9

plag_length_start = 200.0
horn_length_start = 500.0

lengthstep = 100.0
# this will be the step by which we change the relative mode of plag to hornblende
step = 0.1

leng_div = int((max(horn_length_start, plag_length_start) - min(horn_length_start, plag_length_start))/lengthstep)
div = int(max(hornblende_mode_start, plagioclase_mode_start) / step)
print(div)


xfile_lst = []
yfile_lst = []
xname_lst = []
yname_lst = []

for j in range(leng_div + 1):

    delta_len = float(j * lengthstep)

    plag_len = plag_length_start + delta_len
    horn_len = horn_length_start - delta_len

    # for each length, change the modality around
    for i in range(div):
        # print(i)

        # subract from plag and and to hornblende to change the relative concentration
        delta_mode = float(i * step)
        # delta_mode = round(delta_mode, 1)
        plag_mode = plagioclase_mode_start + delta_mode
        plag_mode = round(plag_mode, 1)
        hornb_mode = hornblende_mode_start - delta_mode
        hornb_mode = round(hornb_mode, 1)

        print('plag mode: {}, hornb mode {}'.format(plag_mode, hornb_mode))

        filename = 'eiler94_p{}_h{}_pl{}_hl{}'.format(str(plag_mode)[-1], str(hornb_mode)[-1], int(plag_len), int(horn_len))

        vars = ['x', 'y']

        for v in vars:
            # print('plag mode: {}, hornb mode {}'.format(plag_mode, hornb_mode))
            filename = 'eiler94_p{}_h{}_pl{}_hl{}_{}.npy'.format(str(plag_mode)[-1], str(hornb_mode)[-1], int(plag_len), int(horn_len), v)
            print(filename)
            name = filename.split('.')[0]
            # name_lst.append(name)

            if v == 'x':
                xarrpath = os.path.join(file_root, filename)
                xfile_lst.append(xarrpath)
                xname_lst.append(name)
            if v == 'y':
                yarrpath = os.path.join(file_root, filename)
                yfile_lst.append(yarrpath)
                yname_lst.append(name)

    print(xfile_lst, '\n', yfile_lst)

###=========== SAMPLING ================

# year in MA we want to see
year_ma = 44
time_step = 0.0005

# convert the year into the index for the y array. Subtract one bc the y array starts at index 0
year_index = int(round(((year_ma / time_step) - 1), 1))

print(len(xfile_lst), len(yfile_lst), len(xname_lst), len(yname_lst))

for x_arr_file, y_arr_file, xn, yn in zip(xfile_lst, yfile_lst, xname_lst, yname_lst):

    x_arr = np.load(x_arr_file)
    y_arr = np.load(y_arr_file)

    x_quartz = x_arr[:, 0]
    # print(x_quartz)
    y_quartz = y_arr[0, year_index, :]

    x_plag = x_arr[:, 1]
    y_plag = y_arr[1, year_index, :]

    x_horn = x_arr[:, 2]
    y_horn = y_arr[2, year_index, :]

    x_mag = x_arr[:, 3]
    y_mag = y_arr[3, year_index, :]

    plag_sample_locations = sample_locator(x_plag)
    horn_sample_locations = sample_locator(x_horn)

    outname = '{}_{}'.format('plag', xn)
    generate_synthetic_data(x_arr=x_plag, y_arr=y_plag, noise=0.14, sample_locations=plag_sample_locations,
                                output_location=plag_output_location, output_name=outname)
    outname = '{}_{}'.format('horn', xn)
    generate_synthetic_data(x_arr=x_horn, y_arr=y_horn, noise=0.14, sample_locations=horn_sample_locations,
                            output_location=horn_output_location, output_name=outname)
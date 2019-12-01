import os
import numpy as np
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file, sample_locator, generate_synthetic_data

file_root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/modality_len_results_fwd/blockA'

output_root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/modality_len_results_fwd_sampled/blockA/'
if not os.path.exists(output_root):
    os.mkdir(output_root)

y_files = []
x_files = []
time_files = []
xname_lst = []
yname_lst = []
for i in os.listdir(file_root):

    p = os.path.join(file_root, i)
    n = i.split('.')[0]
    if i.endswith('_x.npy'):
        x_files.append(p)
        xname_lst.append(n)
    elif i.endswith('_y.npy'):
        y_files.append(p)
        yname_lst.append(n)
    elif i.endswith('_time.npy'):
        time_files.append(p)
        # time_name_lsit

yfile_lst = sorted(y_files)
yname_lst = sorted(yname_lst)
xfile_lst = sorted(x_files)
xname_lst = sorted(xname_lst)
time_files = sorted(time_files)

print(yfile_lst)
print(yname_lst)
print(xfile_lst)
print(xname_lst)


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
                                output_location=output_root, output_name=outname)
    outname = '{}_{}'.format('horn', xn)
    generate_synthetic_data(x_arr=x_horn, y_arr=y_horn, noise=0.14, sample_locations=horn_sample_locations,
                            output_location=output_root, output_name=outname)
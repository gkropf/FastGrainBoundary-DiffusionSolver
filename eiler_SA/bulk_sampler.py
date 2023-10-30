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
import os
import numpy as np
# ============= standard library imports ========================
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file
from eiler_SA.forwardmodeling_sa import make_params_dict, generate_synthetic_data, write_params_file

if __name__ == "__main__":

    file_root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/modality_fwd_results/'
    # # HORNBLENDE
    # output_location = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/sa_sampled/hornblende'
    # sample_mineral = 'horn'
    #PLAG
    output_location= '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/sa_sampled/plagioclase'
    sample_mineral = 'plag'
    xfile_lst = []
    yfile_lst = []
    xname_lst = []
    yname_lst = []
    ### ================ MODALITY ================
    # build Filenames for modality SA
    plagioclase_mode_start = 0.1
    hornblende_mode_start = 0.9
    step = 0.1
    div = int(max(hornblende_mode_start, plagioclase_mode_start) / step)
    print(div)
    for i in range(div):

        # subract from plag and and to hornblende to change the relative concentration
        delta_mode = float(i * step)
        # delta_mode = round(delta_mode, 1)
        plag_mode = plagioclase_mode_start + delta_mode
        plag_mode = round(plag_mode, 1)
        hornb_mode = hornblende_mode_start - delta_mode
        hornb_mode = round(hornb_mode, 1)

        vars = ['x', 'y']

        for v in vars:
            print('plag mode: {}, hornb mode {}'.format(plag_mode, hornb_mode))
            filename = 'eiler94_p{}_h{}_{}.npy'.format(str(plag_mode)[-1], str(hornb_mode)[-1], v)
            name = 'eiler94_p{}_h{}'.format(str(plag_mode)[-1], str(hornb_mode)[-1])
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

        # TODO - Function to generate automatic and consistent plag hornblende sample locations

        plag_sample_locations = [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
        horn_sample_locations = [3500, 3600, 3700, 3800, 3900, 4000]

        outname = '{}_{}'.format(sample_mineral, xn)

        if sample_mineral == 'plag':

            generate_synthetic_data(x_arr=x_plag, y_arr=y_plag, noise=0.14, sample_locations=plag_sample_locations,
                            output_location=output_location, output_name=outname)

        elif sample_mineral == 'horn':
            generate_synthetic_data(x_arr=x_horn, y_arr=y_horn, noise=0.14, sample_locations=horn_sample_locations,
                            output_location=output_location, output_name=outname)
# ===============================================================================
# Copyright 2019 Jan Hendrickx and Gabriel Parrish
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
import matplotlib.pyplot as plt
# ============= standard library imports ========================
from eiler_SA.forwardmodeling_sa import make_params_dict, generate_synthetic_data, write_params_file

#root = '/Users/dcadol/Desktop/academic_docs_II/FGB_model/JohnEiler/plag_hornblende_sensitivity'
root = r'/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/original_eiler/'

# year in MA we want to see
year_ma = 44
time_step = 0.0005

# convert the year into the index for the y array. Subtract one bc the y array starts at index 0
year_index = int(round(((year_ma / time_step) - 1), 1))

print('year index {}'.format(year_index))

x_path = os.path.join(root, 'Eiler94_Amphibolite_x.npy')
y_path = os.path.join(root, 'Eiler94_Amphibolite_y.npy')
time_path = os.path.join(root, 'Eiler94_Amphibolite_time.npy')

param_path = os.path.join(root, 'Eiler94_Amphibolite.txt')
param_dict = make_params_dict(param_path)

x_arr = np.load(x_path)
y_arr = np.load(y_path)
t_arr = np.load(time_path)

print('x shape: {}, y shape {}, t shape {}'.format(x_arr.shape, y_arr.shape, t_arr.shape))

# quartz
plt.plot(x_arr[:, 0], y_arr[0, year_index, :])
#plt.show()

# TODO - construct inverse thingy

# 1) Start with a known time-temp history - in our case linear
# 2) Run the forward model
# 3) Keep a sample of forward model outputs at late-time
# 4) Add noise to the data (100% - full noise & 20% - low noise)
# 5) Run the inverse solver on the noisy data with an initial time-temp solution


# Of the last time slice of the forward model we take data as a txt file, only keeping some points
# | Distance | D18O | Uncertainty |

x_quartz = x_arr[:, 0]
# print(x_quartz)
y_quartz = y_arr[0, year_index, :]

x_plag = x_arr[:, 1]
y_plag = y_arr[1, year_index, :]

x_horn = x_arr[:, 2]
y_horn = y_arr[2, year_index, :]

x_mag = x_arr[:, 3]
y_mag = y_arr[3, year_index, :]

quartz_sample_locations = [1500, 1600, 1700, 1800, 1900, 2000]
plag_sample_locations = [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
horn_sample_locations = [3500, 3600, 3700, 3800, 3900, 4000]
mag_sample_locations = [400, 500, 600]

output_location = root

name = 'Eiler94_Amphibolite_plag_lownoise'

print('x plagioclase', x_plag)
generate_synthetic_data(x_arr=x_plag, y_arr=y_plag, noise=0.01, sample_locations=plag_sample_locations,
                        output_location=output_location, output_name=name)




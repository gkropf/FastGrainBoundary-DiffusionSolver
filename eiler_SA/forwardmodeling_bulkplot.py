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


# root = '/Users/dcadol/Desktop/academic_docs_II/FGB_model/JohnEiler/plag_hornblende_sensitivity'
root = '/home/dan/Documents/Eiler_94/plag_hornblende_sensitivity'

rname = 'Eiler94_Amphibolite'

# years in MA we want to see
year_ma = [10, 20, 45]
time_step = 0.0005

# convert the year into the index for the y array. Subtract one bc the y array starts at index 0
yindex_lst = []
for y in year_ma:

    # y-1 accounts for the fact that the year is in order of a python index, so starts at 0 and not 1 like time
    y_index = int(round((((y - 1) / time_step) - 1), 1))
    yindex_lst.append(y_index)

print('year index {}'.format(yindex_lst))

x_path = os.path.join(root, '{}_x.npy'.format(rname))
y_path = os.path.join(root, '{}_y.npy'.format(rname))
time_path = os.path.join(root, '{}_time.npy'.format(rname))

param_path = os.path.join(root, '{}.txt'.format(rname))
param_dict = make_params_dict(param_path)

x_arr = np.load(x_path)
y_arr = np.load(y_path)
t_arr = np.load(time_path)

print('x shape: {}, y shape {}, t shape {}'.format(x_arr.shape, y_arr.shape, t_arr.shape))

# quartz
fig, ax = plt.subplots()
for year_index, y in zip(yindex_lst, year_ma):
    ax.plot(x_arr[:, 0], y_arr[0, year_index, :], label='{} million years'.format(y))
ax.set_title('Plot of Oxygen Isotope Ratios for Quartz - {}'.format(rname))
ax.set_ylabel('Delta 18-O')
ax.set_xlabel('x (mm)')
plt.legend(loc='best')
plt.grid(True)
plt.savefig(os.path.join(root, 'quartz_{}.png'.format(rname)))
plt.show()


# Plag
fig, ax = plt.subplots()
for year_index, y in zip(yindex_lst, year_ma):
    ax.plot(x_arr[:, 1], y_arr[1, year_index, :], label='{} million years'.format(y))
ax.set_title('Plot of Oxygen Isotope Ratios for Plagioclase - {}'.format(rname))
ax.set_ylabel('Delta 18-O')
ax.set_xlabel('x (mm)')
plt.legend(loc='best')
plt.grid(True)
plt.savefig(os.path.join(root, 'plag_{}.png'.format(rname)))
plt.show()

# Hornblende
fig, ax = plt.subplots()
for year_index, y in zip(yindex_lst, year_ma):
    ax.plot(x_arr[:, 2], y_arr[2, year_index, :], label='{} million years'.format(y))
ax.set_title('Plot of Oxygen Isotope Ratios for Hornblende - {}'.format(rname))
ax.set_ylabel('Delta 18-O')
ax.set_xlabel('x (mm)')
plt.legend(loc='best')
plt.grid(True)
plt.savefig(os.path.join(root, 'hornblende_{}.png'.format(rname)))
plt.show()

# titanite
fig, ax = plt.subplots()
for year_index, y in zip(yindex_lst, year_ma):
    ax.plot(x_arr[:, 3], y_arr[3, year_index, :], label='{} million years'.format(y))
ax.set_title('Plot of Oxygen Isotope Ratios for Titanite - {}'.format(rname))
ax.set_ylabel('Delta 18-O')
ax.set_xlabel('x (mm)')
plt.legend(loc='best')
plt.grid(True)
plt.savefig(os.path.join(root, 'titanite_{}.png'.format(rname)))
plt.show()



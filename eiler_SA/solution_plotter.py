import os
import pandas as pd
import matplotlib.pyplot as plt

root = 'file:///home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/Output/yyy'

file1 = 'initial_eiler_94_2_results_in_this_sol.csv'

file2 = 'initial_eiler_94_results_in_this_sol.csv'

names = ['file1', 'file2']
file_lst = [file1, file2]
color_lst = ['red', 'green']

fig, ax = plt.subplots()

# TODO - here is where you plot the solution
# ax.plot(time, temp, color='black', label=True solution)

for i, j, c in zip(names, file_lst, color_lst):
    fpath = os.path.join(root, j)

    df = pd.read_csv(fpath, header=0)

    ax.plot(df.Time, df.Temperature, color=c, label='initial_sol_{}'.format(i))

plt.legend()
plt.show()




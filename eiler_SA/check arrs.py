import numpy as np
import os

root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/modality/modality_len_results_fwd/'
rname = 'eiler94_p8_h2_pl400_hl300'
param_root = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/mode_length_configs_cooling/'

numpy_xarr = os.path.join(root, '{}_x.npy'.format(rname))
numpy_xarr = np.load(numpy_xarr)
numpy_yarr = os.path.join(root, '{}_y.npy'.format(rname))
numpy_yarr = np.load(numpy_yarr)
numpy_tarr = os.path.join(root, '{}_time.npy'.format(rname))
numpy_tarr = np.load(numpy_tarr)

print('np x \n', numpy_xarr, '\n np y \n', numpy_yarr, '\nnp t \n', numpy_tarr)

print(len(numpy_xarr), len(numpy_yarr), len(numpy_tarr))
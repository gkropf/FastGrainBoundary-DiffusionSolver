import os
from eiler_SA.forwardmodeling_sa import make_params_dict, forward_model_slow_bulk
#
# param_path = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/Examples/Ex_Params4.txt'
# fwd_model_params = make_params_dict(params=param_path)
#
# print('running the slow model with a cooling file')
# xresult, yresult, timeresult = forward_model_slow_bulk(fwd_model_params, coolfile=True)

# param_path = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/mode_length_configs/eiler94_p1_h9_pl200_hl500.txt'
# fwd_model_params = make_params_dict(params=param_path)
# print(fwd_model_params)
# # xresult, yresult, timeresult = forward_model_slow_bulk(fwd_model_params, coolfile=False)
#
# # print(len(xresult), len(yresult), len(timeresult))

param_path = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/mode_length_chloe_cooling/blockA/eiler94_p10_h80_pl1500_hl2000.txt'
fwd_model_params = make_params_dict(params=param_path)
print(fwd_model_params)
xresult, yresult, timeresult = forward_model_slow_bulk(fwd_model_params, coolfile=True)

print(len(xresult), len(yresult), len(timeresult))
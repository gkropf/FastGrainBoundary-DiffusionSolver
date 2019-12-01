import os
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file

chloe_model_params = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/original_eiler/Eiler94_Amphibolite.txt'

output = os.path.split(chloe_model_params)[0]

output = os.path.join(output, 'mode_length_temp')

fwd_model_parameters = make_params_dict(chloe_model_params)

print(fwd_model_parameters)
#
# # TODO - first change the parameters of the plag vs hornblende modalities
print(fwd_model_parameters['Min1-Mode'])

# 0.3 - base case
plag_mode_key = 'Min1-Mode'
plagioclase_mode = float(fwd_model_parameters[plag_mode_key])
plagioclase_mode_start = 0.1
# 0.6 - base case
hornb_mode_key = 'Min2-Mode'
hornblende_mode = float(fwd_model_parameters[hornb_mode_key])
hornblende_mode_start = 0.8

plag_length_key = 'Min1-W'
plag_length = float(fwd_model_parameters[plag_length_key])
plag_length_start = 200.0

horn_length_key = 'Min2-R'
horn_length = float(fwd_model_parameters[horn_length_key])
horn_length_start = 10000.0

lengthstep = 100.0
# this will be the step by which we change the relative mode of plag to hornblende
step = 0.05

leng_div = int((max(horn_length_start, plag_length_start) - min(horn_length_start, plag_length_start))/lengthstep)

div = int(max(hornblende_mode_start, plagioclase_mode_start) / step)
print(div)

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

        # at each step in sensitivity set the new mode value (as a string) in the parameters to the new values
        fwd_model_parameters[plag_mode_key] = str(plag_mode)
        fwd_model_parameters[hornb_mode_key] = str(hornb_mode)
        fwd_model_parameters[horn_length_key] = str(horn_len)
        fwd_model_parameters[plag_length_key] = str(plag_len)

        # now write to file
        filename = 'eiler94_p{}_h{}_pl{}_hl{}'.format(str(plag_mode)[-1], str(hornb_mode)[-1], int(plag_len), int(horn_len))
        write_params_file(fwd_model_parameters, output, filename)
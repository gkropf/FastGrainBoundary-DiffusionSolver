import os
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file

chloe_model_params = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/original_eiler/Eiler94_Amphibolite.txt'
output = os.path.split(chloe_model_params)[0]
output = os.path.join(output, 'mode_length_chloe')

fwd_model_parameters = make_params_dict(chloe_model_params)

print(fwd_model_parameters)
#
# # TODO - first change the parameters of the plag vs hornblende modalities
print(fwd_model_parameters['Min1-Mode'])

# 0.3 - base case
plag_mode_key = 'Min1-Mode'
plagioclase_mode = int(input('Plag Mode: '))
pm = plagioclase_mode/100.0


# 0.6 - base case
hornb_mode_key = 'Min2-Mode'
hornblende_mode = int(input('Hornblend Mode: '))
hm = hornblende_mode/100.0

plag_length_key = 'Min1-W'
plag_length = input('Plag Length: ')

horn_length_key = 'Min2-R'
horn_length = input('Hornblende Length: ')

# at each step in sensitivity set the new mode value (as a string) in the parameters to the new values
fwd_model_parameters[plag_mode_key] = str(pm)
fwd_model_parameters[hornb_mode_key] = str(hm)
fwd_model_parameters[horn_length_key] = str(horn_length)
fwd_model_parameters[plag_length_key] = str(plag_length)

print('params to write')
print(fwd_model_parameters)

# now write to file
filename = 'eiler94_p{}_h{}_pl{}_hl{}'.format(str(plagioclase_mode), str(hornblende_mode), int(plag_length), int(horn_length))
write_params_file(fwd_model_parameters, output, filename)
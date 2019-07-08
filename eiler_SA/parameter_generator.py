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
# ============= standard library imports ========================
from eiler_SA.forwardmodeling_sa import make_params_dict, write_params_file

if __name__ == "__main__":

    chloe_model_params = '/home/dan/Documents/Eiler_94/eiler_forward_params/Eiler94_Amphibolite.txt'

    output = os.path.split(chloe_model_params)[0]

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
    hornblende_mode_start = 0.9

    # this will be the step by which we change the relative mode of plag to hornblende
    step = 0.1

    div = int(max(hornblende_mode_start, plagioclase_mode_start) / step)
    print(div)
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

        # now write to file
        filename = 'eiler94_p{}_h{}'.format(str(plag_mode)[-1], str(hornb_mode)[-1])
        write_params_file(fwd_model_parameters, output, filename)



    # # TODO - then change the sizes of the plag and hornblende crystals in another test.
import os


"""Once you've made a ton of config files changing mode and length based off a config template add a cooling file to
 those parameter files with this script. Once you've run this script, run frwrd_bulk_run.py"""

config_file_locations = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/mode_length_chloe/blockD/'
config_output = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/mode_length_chloe_cooling/blockD/'
if not os.path.exists(config_output):
    os.mkdir(config_output)
cooling_file_location = '/home/gabriel/PycharmProjects/FastGrainBoundary-DiffusionSolver/sensitivity_analysis/cooling_file_GELP.txt'
# cooling_file_startemp = 650.0
# cooling_file_endtemp = 200.0
# cooling_file_timestep = 0.0005

for file in os.listdir(config_file_locations):

    print('adding a cooling file to config file: {}'.format(file))

    path = os.path.join(config_file_locations, file)

    lines_to_write = []
    with open(path, 'r') as rfile:

        for line in rfile:
            if line.startswith('CoolingFile,'):
                line = 'CoolingFile,'
                line = '{}{}\n'.format(line, cooling_file_location)
                lines_to_write.append(line)
            elif line.startswith('CoolingType,'):
                type_str = line.split(',')[0]
                line = '{},Custom\n'.format(type_str)
                lines_to_write.append(line)
            # elif line.startswith('ModelDuration'):
            #     pass
            # elif line.startswith('EndTemp'):
            #     lines_to_write.append('EndTemp,{}\n'.format(cooling_file_endtemp))
            # elif line.startswith('StartingTemp'):
            #     lines_to_write.append('StartingTemp,{}\n'.format(cooling_file_startemp))
            # elif line.startswith('TimeStep'):
            #     lines_to_write.append('TimeStep,{}\n'.format(cooling_file_timestep))
            else:
                lines_to_write.append(line)

    outpath = os.path.join(config_output, file)
    print(lines_to_write)
    with open(outpath, 'w') as wfile:

        for line in lines_to_write:
            wfile.write(line)


print('done!!!')

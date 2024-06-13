import os
from helper.print_progress_bar import printProgressBar
from helper.parsers import parse_strokes_from_inkml_file
import numpy as np

files = ['__datasets__/FA_1.1/no_text/FA_Test.txt', '__datasets__/FA_1.1/no_text/FA_Train.txt','__datasets__/FA_1.1/no_text/FA_Validation.txt', '__datasets__/FC_1.0/no_text/FC_Test.txt', '__datasets__/FC_1.0/no_text/FC_Train.txt', '__datasets__/FC_1.0/no_text/FC_Validation.txt']

file_paths = []
max_x = 0
min_x = np.inf
max_y = 0
min_y = np.inf

for name_file_path in files:
    with open(name_file_path) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line.endswith('.inkml'):
                file_paths.append(os.path.dirname(name_file_path) + '/' + line)


for i, path in enumerate(file_paths):
    strokes = parse_strokes_from_inkml_file(path)
    for stroke in strokes:
        for point in stroke:
            if point['x'] > max_x:
                max_x = point['x']
            if point['x'] < min_x:
                min_x = point['x']
            if point['y'] > max_y:
                max_y = point['y']
            if point['y'] < min_y:
                min_y = point['y']
    

print('Max x:', max_x)
print('Min x:', min_x)
print('Max y:', max_y)
print('Min y:', min_y)

# Max x: 59414
# Min x: 0
# Max y: 49756
# Min y: 0
       
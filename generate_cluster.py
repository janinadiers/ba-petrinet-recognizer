import os
from helper.parsers import parse_strokes_from_inkml_file
from scripts.define_clusters import define_clusters, visualize_clusters

file_paths = []
for name_file_path in ['./__datasets__/FC_1.0/no_text/FC_Train.txt', './__datasets__/FC_1.0/no_text/FC_Validation.txt']:
    with open(name_file_path) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line.endswith('.inkml'):
                file_paths.append(os.path.dirname(name_file_path) + '/' + line)

all_circle_features = []            
for i, path in enumerate(file_paths):
    content = parse_strokes_from_inkml_file(path)
    circle_features, rectangle_features = define_clusters(path, content)
    all_circle_features.extend(circle_features)

visualize_clusters(all_circle_features)


    
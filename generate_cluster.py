import os
from helper.parsers import parse_strokes_from_inkml_file
from helper.normalizer import resample_strokes
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
all_rectangle_features = []
all_ellipse_features = []
all_parallelogram_features = []
all_line_features = []
all_double_circle_features = []
all_diamond_features = []

labels = []           
for i, path in enumerate(file_paths[:40]):
    content = parse_strokes_from_inkml_file(path)
    resampled_strokes = resample_strokes(content)
    circle_features, rectangle_features, ellipse_features = define_clusters(path, resampled_strokes)
    all_circle_features.extend(circle_features)
    all_rectangle_features.extend(rectangle_features)
    all_ellipse_features.extend(ellipse_features)
    # all_parallelogram_features.extend(parallelogram_features)
    # all_line_features.extend(line_features)
    # all_double_circle_features.extend(double_circle_features)
    # all_diamond_features.extend(diamond_features)
    
    
labels += [0 for i in range(len(all_circle_features))]
all_circle_features.extend(all_rectangle_features)
labels += [1 for i in range(len(all_rectangle_features))]
all_circle_features.extend(all_ellipse_features)
labels += [2 for i in range(len(all_ellipse_features))]
# all_circle_features.extend(all_parallelogram_features)
# labels += [3 for i in range(len(all_parallelogram_features))]
# all_circle_features.extend(all_line_features)
# labels += [3 for i in range(len(all_line_features))]
# all_circle_features.extend(all_double_circle_features)
# labels += [5 for i in range(len(all_double_circle_features))]
# all_circle_features.extend(all_diamond_features)
# labels += [6 for i in range(len(all_diamond_features))]
# print(len(all_circle_features), len(labels))     
visualize_clusters(all_circle_features, labels)


    
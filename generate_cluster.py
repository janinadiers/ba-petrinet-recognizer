import os
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth
from helper.normalizer import resample_strokes
from scripts.define_clusters import visualize_clusters, get_features, calculate_ellipse_parameters_n_dimensional
from helper.utils import distance, hellinger_distance, pearsons_correlation, get_strokes_from_candidate
import numpy as np
from grouper.shape_grouper.optimized_grouper import group
import json



file_paths = []
for name_file_path in ['./__datasets__/FC_1.0/no_text/FC_Train.txt', './__datasets__/FC_1.0/no_text/FC_Validation.txt', './__datasets__/FA_1.1/no_text/FA_Train.txt', './__datasets__/FA_1.1/no_text/FA_Validation.txt']:
    with open(name_file_path) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line.endswith('.inkml'):
                file_paths.append(os.path.dirname(name_file_path) + '/' + line)

all_circle_features = [] 
all_rectangle_features = []
all_no_shape_features = []

labels = []           
for i, path in enumerate(file_paths):
    content = parse_strokes_from_inkml_file(path)
    resampled_strokes = resample_strokes(content)
    candidates = group(resampled_strokes)

    # circle_features, rectangle_features, no_shape_features = get_features(path, resampled_strokes, candidates)
    circle_features, rectangle_features= get_features(path, resampled_strokes, candidates)

    all_circle_features.extend(circle_features)
    all_rectangle_features.extend(rectangle_features)
    # all_no_shape_features.extend(no_shape_features)

    
labels += [0 for i in range(len(all_circle_features))]
labels += [1 for i in range(len(all_rectangle_features))]
# labels += [2 for i in range(len(all_no_shape_features))]

circle_cluster_center = np.array(all_circle_features).mean(axis=0)
circle_correlation_values = [pearsons_correlation(vector, circle_cluster_center) for vector in all_circle_features]

similarity_circle = min(circle_correlation_values)
circle_F1, circle_F2, circle_S, angle= calculate_ellipse_parameters_n_dimensional(all_circle_features, circle_cluster_center)

rectangle_cluster_center = np.array(all_rectangle_features).mean(axis=0)
# get the minimum pearsons correlation value
rectangle_correlation_values = [pearsons_correlation(vector, rectangle_cluster_center) for vector in all_rectangle_features]
similarity_rectangle = min(rectangle_correlation_values)
rectangle_F1, rectangle_F2, rectangle_S, angle= calculate_ellipse_parameters_n_dimensional(all_rectangle_features, rectangle_cluster_center)

result_obj = {
    'circle': {
        'F1': list(circle_F1),
        'F2': list(circle_F2),
        'S': circle_S,
        'cluster_center': list(circle_cluster_center),
        'similarity': similarity_circle,
    },
    'rectangle': {
        'F1': list(rectangle_F1),
        'F2': list(rectangle_F2),
        'S': rectangle_S,
        'cluster_center': list(rectangle_cluster_center),
        'similarity': similarity_rectangle,
    }
}
 
# write results into json file
with open(f'rejector/clusters.json', 'a') as f:
    json.dump(result_obj, f, indent=4)

all_circle_features.extend(all_rectangle_features)
# all_circle_features.extend(all_no_shape_features)   

# visualize_clusters(all_circle_features, labels)


    
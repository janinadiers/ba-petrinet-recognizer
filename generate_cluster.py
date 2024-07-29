import os
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth, parse_ratio_from_inkml_file
from helper.normalizer import resample_strokes, convert_coordinates
from scripts.define_clusters import visualize_clusters, get_features, calculate_ellipse_parameters_n_dimensional, visualize_feature_separation
from helper.utils import distance, hellinger_distance, pearsons_correlation, get_strokes_from_candidate
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from grouper.shape_grouper.optimized_grouper import group
import json




file_paths = []
# for name_file_path in ['./__datasets__/PN_1.0/PN_Test.txt']:
for name_file_path in ['./__datasets__/FC_1.0/no_text/FC_Train.txt', './__datasets__/FC_1.0/no_text/FC_Validation.txt',  './__datasets__/FA_1.1/no_text/FA_Train.txt', './__datasets__/FA_1.1/no_text/FA_Validation.txt']:
    with open(name_file_path) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if line.endswith('.inkml'):
                file_paths.append(os.path.dirname(name_file_path) + '/' + line)

all_circle_features = [] 
all_rectangle_features = []
all_no_shape_features = []

# FC: 476 Diagrams, FA: 216, PN: 48
fc_paths = file_paths[:47]
fa_paths = file_paths[476:498]
pn_paths = file_paths[692 :697]
# take every tenth file from FA and FC and every file from PN

labels = []           
# for path in fc_paths + fa_paths + pn_paths:
for path in file_paths:
    print('Processing file', path)
    content = parse_strokes_from_inkml_file(path)
    print('content ready')
    
    if 'FC' in path:
        ratio = [59414,49756]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        print('strokes converted')
        resampled_content = resample_strokes(converted_strokes)
        print('strokes resampled')
        candidates = group(resampled_content)
        print('candidates generated')
    elif 'FA' in path:
        ratio = [48484,26442]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        print('strokes converted')
        resampled_content = resample_strokes(converted_strokes)
        print('strokes resampled')
        candidates = group(resampled_content)
        print('candidates generated')
    elif 'PN' in path:
        ratio = parse_ratio_from_inkml_file(path)
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        print('strokes converted')
        resampled_content = resample_strokes(converted_strokes)
        print('strokes resampled')
        candidates = group(resampled_content)
        print('candidates generated')
    

    # circle_features, rectangle_features, no_shape_features = get_features(path, resampled_content, candidates)
    circle_features, rectangle_features= get_features(path, resampled_content, candidates)
    print('features extracted')
    all_circle_features.extend(circle_features)
    all_rectangle_features.extend(rectangle_features)
    # all_no_shape_features.extend(no_shape_features)
    
labels += ['circle' for i in range(len(all_circle_features))] 
labels += ['rectangle' for i in range(len(all_rectangle_features))]


# all_circle_features.extend(all_rectangle_features)
        
# all_no_shape_features = [item for item in all_no_shape_features if item is not None]
# labels += ['shape' for i in range(len(all_circle_features))]
# labels += ['no-shape' for i in range(len(all_no_shape_features))]

circle_cluster_center = np.array(all_circle_features).mean(axis=0)
rectangle_cluster_center = np.array(all_rectangle_features).mean(axis=0)

# no_shape_cluster_center = np.array(all_no_shape_features).mean(axis=0)

# circle_cosine_similarity_values = []
circle_pearsons_correlation_values = []

for vector in all_circle_features:
    similarity = cosine_similarity([vector], [list(circle_cluster_center)])
    circle_pearsons_correlation_values.append(similarity)
   
circle_pearsons_correlation = min(circle_pearsons_correlation_values)
circle_hellinger_distance_values = []
for vector in all_circle_features:
    distance = hellinger_distance(vector, list(circle_cluster_center))
    circle_hellinger_distance_values.append(distance)
circle_hellinger_distance = max(circle_hellinger_distance_values)


# rectangle_cosine_similarity_values = []
rectangle_pearsons_correlation_values = []

for vector in all_rectangle_features:
    similarity = cosine_similarity([vector], [list(rectangle_cluster_center)])
    # rectangle_cosine_similarity_values.append(similarity)
    rectangle_pearsons_correlation_values.append(similarity)
   
# rectangle_cosine_similarity = min(rectangle_cosine_similarity_values)
rectangle_pearsons_correlation = min(rectangle_pearsons_correlation_values)
rectangle_hellinger_distance_values = []
for vector in all_rectangle_features:
    distance = hellinger_distance(vector, list(rectangle_cluster_center))
    rectangle_hellinger_distance_values.append(distance)
rectangle_hellinger_distance = max(rectangle_hellinger_distance_values)

# no_shape_cosine_similarity_values = []
# for vector in all_no_shape_features:
#     similarity = cosine_similarity([vector], [list(no_shape_cluster_center)])
#     print('similarity', similarity)
#     no_shape_cosine_similarity_values.append(similarity)
# no_shape_cosine_similarity = min(no_shape_cosine_similarity_values)
# no_shape_hellinger_distance_values = []
# for vector in all_no_shape_features:
#     distance = hellinger_distance(vector, list(no_shape_cluster_center))
#     print('hellinger_distance', distance)
#     no_shape_hellinger_distance_values.append(distance)
# no_shape_hellinger_distance = max(shape_hellinger_distance_values)
print(circle_pearsons_correlation, rectangle_pearsons_correlation)

result_obj = {
    'circle': {
        'cluster_center': circle_cluster_center[0],
        'similarity': circle_pearsons_correlation[0][0],
        'distance': circle_hellinger_distance,
    },
    'rectangle': {
        'cluster_center': rectangle_cluster_center[0],
        'similarity': rectangle_pearsons_correlation[0][0],
        'distance': rectangle_hellinger_distance,
    }
}
 
#write results into json file
with open(f'rejector/clusters2.json', 'a') as f:
    json.dump(result_obj, f, indent=4)
    
# all_circle_features.extend(all_no_shape_features)   

# print('all_circle_features', len(all_circle_features), len(labels))
# visualize_feature_separation(all_circle_features, labels)
# print(all_circle_features)
# visualize_clusters(all_circle_features, labels)


    
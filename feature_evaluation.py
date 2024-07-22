import os
import scipy.stats as stats
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth, parse_ratio_from_inkml_file
from grouper.shape_grouper.optimized_grouper import group as grouper
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features
from helper.normalizer import resample_strokes, convert_coordinates
import numpy as np

feature_names = None

def pearson_correlation(labels, features):
    # Ensure labels and features are numpy arrays of floats
    print(features)
    try:
        labels = np.array(labels, dtype=np.float64)
        features = np.array(features, dtype=np.float64)
    except ValueError as e:
        print(f"Error converting to numpy arrays: {e}")
        return

    # Filter out None values and NaNs
    zipped = zip(labels, features)
    filtered = [(label, feature) for label, feature in zipped if not label == None and not feature == None]

    # Check if there are enough data points left after filtering
    if len(filtered) < 2:
        print("Not enough valid data points to calculate Pearson correlation.")
        return

    # Unzip the filtered pairs back into separate lists
    filtered_labels, filtered_features = zip(*filtered)

    # Convert to numpy arrays
    filtered_labels = np.array(filtered_labels)
    filtered_features = np.array(filtered_features)

    # Calculate Pearson correlation coefficient
    try:
        correlation, p_value = stats.pearsonr(filtered_labels, filtered_features)
        print(f"Pearson correlation coefficient: {correlation}")
        print(f"P-value: {p_value}")
    except Exception as e:
        print(f"Error calculating Pearson correlation: {e}")
        
def prepare_data(path):
    
    global feature_names
    content = parse_strokes_from_inkml_file(path)
    if 'FC' in path:
        ratio = [59414,49756]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
    if 'FA' in path:
        ratio = [48484,26442]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
    if 'PN' in path:
            ratio = parse_ratio_from_inkml_file(path)
            converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
            resampled_content = resample_strokes(converted_strokes)
            candidates = grouper(resampled_content)
    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'circle': 0, 'rectangle': 1}
    for candidate in candidates:
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    if shape_name == 'ellipse' or shape_name == 'circle':
                        result = get_circle_rectangle_features(candidate,resampled_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                        features.append(result['features'][0])
                        labels.append(label_mapping['circle'])
                    elif shape_name == 'rectangle':
                        result = get_circle_rectangle_features(candidate,resampled_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                        features.append(result['features'][0])
                        labels.append(label_mapping['rectangle'])
       
        
    return features, labels


def prepare_data2(path):
    global feature_names
    content = parse_strokes_from_inkml_file(path)
    if 'FC' in path:
        ratio = [59414,49756]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
    if 'FA' in path:
        ratio = [48484,26442]
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
    if 'PN' in path:
        ratio = parse_ratio_from_inkml_file(path)
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
   
    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'shape': 0, 'no_shape': 1}
    candidate_is_in_truth = False
    for candidate in candidates:
        result = get_shape_no_shape_features(candidate, resampled_content)
        if result['features'] == None:
            continue
        if not feature_names:
            feature_names = result['feature_names']
        features.append(result['features'][0])
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    candidate_is_in_truth = True
                    if shape_name == 'line':
                        shape_name = 'no_shape'
                    else:
                        shape_name = 'shape'
                    labels.append(label_mapping[shape_name])
        if not candidate_is_in_truth:      
            labels.append(label_mapping['no_shape'])
        candidate_is_in_truth = False
    return features, labels
                    
                   
file_paths = []
files = ['./__datasets__/FC_1.0/no_text/FC_Train.txt', './__datasets__/FC_1.0/no_text/FC_Validation.txt', './__datasets__/FA_1.1/no_text/FA_Train.txt', './__datasets__/FA_1.1/no_text/FA_Validation.txt', './__datasets__/PN_1.0/PN_Test.txt']
all_features = []
all_labels = []

for name_file_path in files:
        with open(name_file_path) as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                if line.endswith('.inkml'):
                    file_paths.append(os.path.dirname(name_file_path) + '/' + line)
for i, path in enumerate(file_paths):
    print(f"Processing file {i + 1}/{len(file_paths)}: {path}")
    features, labels = prepare_data(path)
    all_features.extend(features)
    all_labels.extend(labels)
print('all features', all_features)
pearson_correlation(all_labels, all_features)
    
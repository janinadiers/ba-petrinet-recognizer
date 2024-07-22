from classifier.shape_classifier.template_matching import use as template_matching
from classifier.shape_classifier.linear_svm import train as linear_svm
from classifier.shape_classifier.rbf_svm import train as rbf_svm
from classifier.shape_classifier.one_class_rectangle_svm import train as one_class_svm_rectangle
from classifier.shape_classifier.one_class_circle_svm import train as one_class_svm_circle
from rejector.shape_rejector.hellinger_and_correlation import use as hellinger_plus_correlation
from rejector.shape_rejector.linear_svm import train as linear_svm_rejector
from rejector.shape_rejector.rbf_svm import train as rbf_svm_rejector
import argparse 
import os
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth, parse_ratio_from_inkml_file
from grouper.shape_grouper.optimized_grouper import group as grouper
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features, get_hellinger_correlation_features
from helper.normalizer import resample_strokes, convert_coordinates

CLASSIFIERS = {
    'template_matching' : template_matching,
    'linear_svm' : linear_svm,
    'rbf_svm' : rbf_svm,
    'one_class_svm_rectangle' : one_class_svm_rectangle,
    'one_class_svm_circle' : one_class_svm_circle
}

REJECTORS = {
    'hellinger_plus_correlation' : hellinger_plus_correlation,
    'linear_svm' : linear_svm_rejector,
    'rbf_svm' : rbf_svm_rejector
    
}



parser = argparse.ArgumentParser(description='Petrinet recognizer 0.1.')

parser.add_argument('--classifier', dest='classifier', type=str, nargs='?', action='store',
                    help='select a classifier you would like to train: linear_svm')
parser.add_argument('--rejector', dest='rejector', type=str, nargs='?', action='store',
                    help='select a rejector you would like to train: hellinger_plus_correlation')

feature_names = None

def prepare_classifier_data(path):
    print('prepare_classifier_data')
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
                        features.append(result['features'])
                        labels.append(label_mapping['circle'])
                    elif shape_name == 'rectangle':
                        result = get_circle_rectangle_features(candidate,resampled_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                        features.append(result['features'])
                        labels.append(label_mapping['rectangle'])
       
        
    return features, labels

def prepare_rejector_data(path):
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
        features.append(result['features'])
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

def prepare_one_class_classifier_data(path):
    print('prepare_one__class_classifier_data')
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
    
    for candidate in candidates:
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    if shape_name == 'rectangle':
                        result = get_circle_rectangle_features(candidate, resampled_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                                   
                        features.append(result['features'])

                    # print(shape_name)
                    # print('---------------------------')
                    # get_hellinger_correlation_features(candidate, resampled_content)
                    # print('---------------------------')
    
    return features
    
    
def prepare_one_class_rejector_data(path):
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
    for candidate in candidates:
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    result = get_shape_no_shape_features(candidate, resampled_content)
                    if not feature_names:
                        feature_names = result['feature_names']     
                    features.append(result['features'])
    return features
                    
                   
args = parser.parse_args()
file_paths = []
files = ['./__datasets__/FC_1.0/no_text/FC_Train.txt', './__datasets__/FC_1.0/no_text/FC_Validation.txt', './__datasets__/FA_1.1/no_text/FA_Train.txt', './__datasets__/FA_1.1/no_text/FA_Validation.txt']
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
    if args.classifier:
        if args.classifier == 'one_class_svm_rectangle':
            features = prepare_one_class_classifier_data(path)
            all_features.extend(features)
        elif args.classifier == 'one_class_svm_circle':
            features = prepare_one_class_classifier_data(path)
            all_features.extend(features)
        else:
            features, labels = prepare_classifier_data(path)
            all_features.extend(features)
            all_labels.extend(labels)
    if args.rejector:
        if args.rejector == 'one_class_svm':
            features = prepare_one_class_rejector_data(path)
            all_features.extend(features)
        else:
            features, labels = prepare_rejector_data(path)
            all_features.extend(features)
            all_labels.extend(labels)

if args.classifier:
    if args.classifier not in CLASSIFIERS:
        print('Invalid classifier. Exiting...')
        exit()
    elif args.classifier == 'one_class_svm_rectangle':
        print('one_class_svm_rectangle')
        classifier = CLASSIFIERS[args.classifier]
        classifier(all_features, feature_names)
    elif args.classifier == 'one_class_svm_circle':
        classifier = CLASSIFIERS[args.classifier]
        classifier(all_features, feature_names)
    else:
        print('classifier selected', args.classifier)
        classifier = CLASSIFIERS[args.classifier]
        classifier(all_features, all_labels, feature_names)
        

if args.rejector:
    if args.rejector not in REJECTORS:
        print('Invalid rejector. Exiting...')
        exit()   
    elif args.rejector == 'one_class_svm':
        rejector = REJECTORS[args.rejector]
        rejector(all_features, feature_names)
    else:
        print('rejector selected', args.rejector)
        rejector = REJECTORS[args.rejector]
        # print(all_features, all_labels, feature_names)
        rejector(all_features, all_labels, feature_names)
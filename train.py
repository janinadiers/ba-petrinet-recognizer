from classifier.shape_classifier.template_matching import use as template_matching
from classifier.shape_classifier.linear_svm import train as linear_svm
from classifier.shape_classifier.rbf_svm import train as rbf_svm
from rejector.hellinger_plus_correlation import is_valid_shape as hellinger_plus_correlation
from rejector.linear_svm import train as linear_svm_rejector
from rejector.rbf_svm import train as rbf_svm_rejector
import argparse 
import os
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth
from grouper.shape_grouper.optimized_grouper import group as grouper
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features
from helper.normalizer import normalize, remove_junk_strokes

CLASSIFIERS = {
    'template_matching' : template_matching,
    'linear_svm' : linear_svm,
    'rbf_svm' : rbf_svm
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
    global feature_names
    content = parse_strokes_from_inkml_file(path)
    content = remove_junk_strokes(content)
    candidates = grouper(content) 
    normalized_content = normalize(content)

    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'circle': 0, 'rectangle': 1}
    for candidate in candidates:
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    if shape_name == 'ellipse' or shape_name == 'circle':
                        result = get_circle_rectangle_features(candidate, normalized_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                        features.append(result['features'])
                        labels.append(label_mapping['circle'])
                    elif shape_name == 'rectangle':
                        result = get_circle_rectangle_features(candidate, normalized_content)
                        if not feature_names:
                            feature_names = result['feature_names']
                        features.append(result['features'])
                        labels.append(label_mapping['rectangle'])
       
        
    return features, labels

def prepare_rejector_data(path):
    global feature_names
    content = parse_strokes_from_inkml_file(path)
    content = remove_junk_strokes(content)
    candidates = grouper(content) 
    normalized_content = normalize(content)
    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'shape': 0, 'no_shape': 1}
    candidate_is_in_truth = False
    for candidate in candidates:
        result = get_shape_no_shape_features(candidate, normalized_content)
        if not feature_names:
            feature_names = result['feature_names']
        print(result['features'])

        features.append(result['features'])
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    candidate_is_in_truth = True
                    if shape_name == 'circle':
                        shape_name = 'shape'
                    elif shape_name == 'rectangle':
                        shape_name = 'shape'
                    elif shape_name == 'ellipse':
                        shape_name = 'shape'
                    else:
                        shape_name = 'no_shape'
                    labels.append(label_mapping[shape_name])
        if not candidate_is_in_truth:      
            labels.append(label_mapping['no_shape'])
        candidate_is_in_truth = False
    return features, labels
    
    
args = parser.parse_args()
file_paths = []
files = ['./__datasets__/FC_1.0/no_text/FC_Train.txt']
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
        features, labels = prepare_classifier_data(path)
    if args.rejector:
        features, labels = prepare_rejector_data(path)
    all_features.extend(features)
    all_labels.extend(labels)

if args.classifier:
    
    if args.classifier not in CLASSIFIERS:
        print('Invalid classifier. Exiting...')
        exit()
    else:
        print('classifier selected', args.classifier)
        classifier = CLASSIFIERS[args.classifier]
        classifier(all_features, all_labels, feature_names)
        

if args.rejector:
    print('rejector selected', args.rejector)
    if args.rejector not in REJECTORS:
        print('Invalid rejector. Exiting...')
        exit()
    else:
        rejector = REJECTORS[args.rejector]
        rejector(all_features, all_labels, feature_names)
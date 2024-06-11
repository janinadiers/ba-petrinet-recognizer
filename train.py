from classifier.shape_classifier.template_matching import use as template_matching
from classifier.shape_classifier.linear_svm import train as linear_svm
from classifier.shape_classifier.radial_svm import train as radial_svm
from rejector.hellinger_plus_correlation import is_valid_shape as hellinger_plus_correlation
from rejector.linear_svm import train as linear_rejector_svm
from rejector.radial_svm import train as radial_rejector_svm
import argparse 
import os
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth
from grouper.shape_grouper.optimized_grouper import group as grouper
from helper.features import get_feature_vector
from helper.normalizer import normalize

CLASSIFIERS = {
    'template_matching' : template_matching,
    'linear_svm' : linear_svm,
    'radial_svm' : radial_svm
}

REJECTORS = {
    'hellinger_plus_correlation' : hellinger_plus_correlation,
    'linear_svm' : linear_rejector_svm,
    'radial_svm' : radial_rejector_svm
}



parser = argparse.ArgumentParser(description='Petrinet recognizer 0.1.')

parser.add_argument('--classifier', dest='classifier', type=str, nargs='?', action='store', default='linear_svm',
                    help='select a classifier you would like to train: linear_svm')
parser.add_argument('--rejector', dest='rejector', type=str, nargs='?', action='store', default='hellinger_plus_correlation',
                    help='select a rejector you would like to train: hellinger_plus_correlation')

feature_names = None

def prepare_classifier_data(path):
    content = parse_strokes_from_inkml_file(path)
    candidates = grouper(content) 
    normalized_content = normalize(content)

    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'circle': 0, 'rectangle': 1,'no shape': 2}
    candidate_is_in_truth = False
    for candidate in candidates:
        result = get_feature_vector(candidate, normalized_content)
        if not feature_names:
            feature_names = result['feature_names']
        features.append(result['features'])
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    candidate_is_in_truth = True
                    if shape_name == 'ellipse':
                        shape_name = 'circle'
                    elif shape_name != 'rectangle' and shape_name != 'circle':
                        shape_name = 'no shape'
                    labels.append(label_mapping[shape_name])
        if not candidate_is_in_truth:      
            labels.append(label_mapping['no shape'])
        candidate_is_in_truth = False
    return features, labels

def prepare_rejector_data(path):
    content = parse_strokes_from_inkml_file(path)
    candidates = grouper(content) 
    normalized_content = normalize(content)

    truth = parse_ground_truth(path)
    features = []
    labels = []
    label_mapping = {'shape': 0, 'no_shape': 1}
    candidate_is_in_truth = False
    for candidate in candidates:
        features.append(get_feature_vector(candidate, normalized_content))
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
                        shape_name = 'no shape'
                    labels.append(label_mapping[shape_name])
        if not candidate_is_in_truth:      
            labels.append(label_mapping['no shape'])
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
    features, labels = prepare_classifier_data(path)
    all_features.extend(features)
    all_labels.extend(labels)

if args.classifier:
    if args.classifier not in CLASSIFIERS:
        print('Invalid classifier. Exiting...')
        exit()
    else:
        classifier = CLASSIFIERS[args.classifier]
        classifier(all_features, all_labels, feature_names)
        

# if args.rejector:
#     if args.rejector not in REJECTORS:
#         print('Invalid rejector. Exiting...')
#         exit()
#     else:
#         rejector = REJECTORS[args.rejector]
#         rejector.train()
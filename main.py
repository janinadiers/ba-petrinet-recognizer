import argparse
from glob import glob  
from grouper.shape_grouper.thesis_grouper import group as thesis_grouper
from grouper.shape_grouper.optimized_grouper import group as optimized_grouper
from recognizer.random_mock import recognize as random_mock
from recognizer.perfect_mock import recognize as perfect_mock
from recognizer.shape_recognizer import recognize as shape_recognizer
from classifier.shape_classifier.template_matching import use as template_matching
from classifier.shape_classifier.linear_svm import use as linear_svm
from classifier.shape_classifier.rbf_svm import use as rbf_svm
from classifier.shape_classifier.one_class_rectangle_svm import use as one_class_rectangle_svm
from classifier.shape_classifier.classifier_with_thresholds import use as classifier_with_thresholds
from rejector.shape_rejector.hellinger_plus_correlation import use as hellinger_plus_correlation
from rejector.shape_rejector.linear_svm import use as linear_svm_rejector
from rejector.shape_rejector.rbf_svm import use as rbf_svm_rejector
from rejector.shape_rejector.rejector_with_threshold import use as rejector_with_threshold
from rejector.shape_rejector.one_class_svm import use as one_class_svm
from helper.EvaluationWrapper import EvaluationWrapper
from helper.parsers import parse_strokes_from_inkml_file
from helper.normalizer import resample_strokes
from helper.normalizer import convert_coordinates
import os
from helper.print_progress_bar import printProgressBar
import datetime
from helper.utils import get_strokes_from_candidate
import numpy as np
import json


GROUPERS = {
    'thesis_grouper' : thesis_grouper,
    'optimized_grouper' : optimized_grouper
}

RECOGNIZERS = {
    'random_mock' : random_mock,
    'perfect_mock' : perfect_mock,
    'shape_recognizer' : shape_recognizer
   
}

CLASSIFIERS = {
    'template_matching' : template_matching,
    'linear_svm' : linear_svm,
    'rbf_svm' : rbf_svm,
    'one_class_rectangle_svm' : one_class_rectangle_svm,
    'classifier_with_thresholds' : classifier_with_thresholds
}

REJECTORS = {
    'hellinger_plus_correlation' : hellinger_plus_correlation,
    'linear_svm' : linear_svm_rejector,
    'rbf_svm' : rbf_svm_rejector,
    'rejector_with_threshold' : rejector_with_threshold,
    'one_class_svm' : one_class_svm
}
    

def _toGlobalPath(path: str):
    return glob(path, recursive=True)

parser = argparse.ArgumentParser(description='Petrinet recognizer 0.1.')

parser.add_argument('--files', dest='files', nargs='+',
                    help='glob to textfile(s) containing inkml file names', default=['./__datasets__/FA_1.1/no_text/FA_Train.txt'])
parser.add_argument('--inkml', dest='inkml', type=_toGlobalPath, nargs='?', action='store', default='',
                    help='glob to inkml file(s)')
parser.add_argument('--grouper', dest='grouper', type=str, nargs='?', action='store', default='optimized_grouper',
                    help='select a grouping algorithm, thesis_grouper or optimized_grouper')
parser.add_argument('--recognizer', dest='recognizer', type=str, nargs='?', action='store', default='shape_recognizer',
                    help='select a recognizer, random_mock_recognizer, perfect_mock_recognizer or shape_recognizer')
parser.add_argument('--classifier', dest='classifier', type=str, nargs='?', action='store', default='linear_svm',
                    help='select a classifier, template_matching or linear_svm')
parser.add_argument('--rejector', dest='rejector', type=str, nargs='?', action='store', default='rejector_with_threshold',
                    help='select a rejector, like hellinger_plus_correlation')
parser.add_argument('--other_ratio', dest='other_ratio', type=str, nargs='?', action='store',
                    help='scales input to another dimension')
parser.add_argument('--production', dest='production', type=bool, nargs='?', action='store', default=False,
                    help='determines if we run with evaluation logic or not')
parser.add_argument('--save', dest='save', type=str, nargs='?', action='store', default='n',
                    help='determines if we save the results to a file or not')


args = parser.parse_args()


def validate_args(args):
    if args.grouper not in GROUPERS:
        print('Invalid grouper. Exiting...')
        exit()
    if args.recognizer not in RECOGNIZERS:
        print('Invalid recognizer. Exiting...')
        exit()
    if args.classifier not in CLASSIFIERS:
        print('Invalid classifier. Exiting...')
        exit()
    if args.rejector not in REJECTORS:
        print('Invalid rejector. Exiting...')
        exit()
    if args.production and args.save == 'y':
        print('Invalid combination of arguments. Cannot save results in production mode. Exiting...')
        exit()
    
validate_args(args)

evaluationWrapper = None if args.production else EvaluationWrapper(RECOGNIZERS[args.recognizer])

recognizer = RECOGNIZERS[args.recognizer] if args.production else evaluationWrapper.recognize
grouper = GROUPERS[args.grouper]
shape_no_shape_features = None
rectangle_features = None
circle_features = None

file_paths = []
if args.inkml:
    file_paths = args.inkml
elif args.files:
    for name_file_path in args.files:
        with open(name_file_path) as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                if line.endswith('.inkml'):
                    file_paths.append(os.path.dirname(name_file_path) + '/' + line)
else:
    print('No files specified. Exiting...')
    exit()

items = list(range(0, len(file_paths)))
l = len(items)
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)   
resampled_content = None
content = None

for i, path in enumerate(file_paths):
    # print('Processing file:', path)
    evaluationWrapper.setCurrentFilePath(path) if not args.production else None
    content = parse_strokes_from_inkml_file(path)
    
    if args.other_ratio:
        ratio = args.other_ratio.split('/')
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        candidates = grouper(converted_strokes)
        resampled_content = resample_strokes(converted_strokes)
    else:
        candidates = grouper(content)
        resampled_content = resample_strokes(content)
    results = []
    recognized_strokes = []
    print('Length Produzierte candidates:', len(candidates))
    for candidate in candidates:
        # check if no values from the candidate are in recognized_strokes
        if not any(recognized_stroke in candidate for recognized_stroke in recognized_strokes):
        # if True:
            # print(args.recognizer, args.classifier, args.rejector)
            recognizer_result, shape_no_shape_features, rectangle_features = recognizer(REJECTORS[args.rejector], CLASSIFIERS[args.classifier], candidate, resampled_content)
            if not shape_no_shape_features:
                shape_no_shape_features = shape_no_shape_features
            if not rectangle_features:
                rectangle_features = rectangle_features
            results.append(recognizer_result)
            if 'valid' in recognizer_result:
                recognized_strokes.extend(candidate)
    
    # printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# print('result: ', results)
        
if not args.production:
    evaluationWrapper.set_total()
    evaluationWrapper.set_accuracy()
    print(evaluationWrapper)
    

if args.save == 'y':
    print('Saving results to file...')
    file_name = 'evaluation_results/results' + str(datetime.datetime.now()) +'.csv'
    evaluationWrapper.matrix.to_csv(file_name)
    with open(file_name, 'a') as f:
        f.write('# dataset: ' + str(args.files) + '\n')
        f.write('# grouper: ' + str(args.grouper) + '\n')
        f.write('# classifier: ' + str(args.classifier) + '\n')
        f.write('# rejector: ' + str(args.rejector) + '\n')
        f.write('# shape no shape features: '+ ''.join(shape_no_shape_features) +'\n')
        f.write('# circle rectangle features: '+ ''.join(rectangle_features) +'\n')

if args.production:
    file_name = args.inkml[0].split('/')[-1].split('.')[0]
    with open(f'inkml_results/{file_name}.json', 'a') as f:
        f.write('[')
    id_counter = 0
    for result in results:
        if 'valid' in result:
            shape_name = next(iter(result['valid']))
            candidates = result['valid'][shape_name]
            strokes_of_candidate= get_strokes_from_candidate(candidates, content)
            
            min_x = np.inf
            min_y = np.inf
            max_x = 0
            max_y = 0
            width = 0
            height = 0
            conversion_factor = 1000
            for stroke in strokes_of_candidate:
                for point in stroke:
                    if point['x'] < min_x:
                        min_x = point['x']
                    if point['y'] < min_y:
                        min_y = point['y']
                    if point['x'] > max_x:
                        max_x = point['x']
                    if point['y'] > max_y:
                        max_y = point['y']
            width = max_x - min_x
            height = max_y - min_y
            if shape_name == 'rectangle':
                shape_id = 't' + str(id_counter)
            elif shape_name == 'circle':
                shape_id = 'p' + str(id_counter)
            # line still has to be implemented 
            # x and y values are being adapted to the canvas size of the petri net editors from I love petri nets
            result_obj = {'shape_name': shape_name,'min_x': min_x, 'min_y': min_y, 'max_x': max_x, 'max_y': max_y, 'width': width, 'height': height, 'shape_id': shape_id}
          
            with open(f'inkml_results/{file_name}.json', 'a') as f:
                json.dump(result_obj, f, indent=4)
                if id_counter < len(results) - 1:
                    f.write(',\n')
        id_counter += 1
    with open(f'inkml_results/{file_name}.json', 'a') as f:
        f.write(']')
    
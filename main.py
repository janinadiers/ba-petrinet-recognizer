import argparse
from glob import glob  
from grouper.shape_grouper.thesis_grouper import group as thesis_grouper
from grouper.shape_grouper.optimized_grouper import group as optimized_grouper
from grouper.connection_grouper.grouper import group as connection_grouper
from recognizer.random_mock import recognize as random_mock
from recognizer.perfect_mock import recognize as perfect_mock
from recognizer.shape_recognizer import recognize as shape_recognizer
from classifier.shape_classifier.template_matching import use as template_matching
from classifier.shape_classifier.linear_svm import use as linear_svm
from classifier.shape_classifier.rbf_svm import use as rbf_svm
from classifier.shape_classifier.one_class_rectangle_svm import use as one_class_rectangle_svm
from classifier.shape_classifier.classifier_with_threshold import use as classifier_with_threshold
from classifier.shape_classifier.perfect_mock import use as perfect_mock_classifier
from rejector.shape_rejector.threshold_and_ellipse import use as threshold_and_ellipse
from rejector.shape_rejector.hellinger_and_correlation import use as hellinger_plus_correlation
from rejector.shape_rejector.linear_svm import use as linear_svm_rejector
from rejector.shape_rejector.rbf_svm import use as rbf_svm_rejector
from rejector.shape_rejector.rejector_with_threshold import use as rejector_with_threshold
from rejector.shape_rejector.one_class_svm import use as one_class_svm
from rejector.shape_rejector.perfect_mock import use as perfect_mock_rejector
from helper.EvaluationWrapper import EvaluationWrapper
from helper.parsers import parse_strokes_from_inkml_file, parse_ground_truth, parse_ratio_from_inkml_file
from helper.normalizer import resample_strokes
from helper.normalizer import convert_coordinates
from helper.utils import get_unrecognized_strokes, get_position_values, plot_strokes_without_scala
from scripts.determine_best_closed_shape_threshold import get_threshold, next_threshold
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
    'classifier_with_threshold' : classifier_with_threshold,
    'perfect_mock_classifier' : perfect_mock_classifier
}

REJECTORS = {
    'threshold_and_ellipse' : threshold_and_ellipse,
    'linear_svm' : linear_svm_rejector,
    'rbf_svm' : rbf_svm_rejector,
    'rejector_with_threshold' : rejector_with_threshold,
    'one_class_svm' : one_class_svm,
    'hellinger_plus_correlation' : hellinger_plus_correlation,
    'perfect_mock_rejector' : perfect_mock_rejector
}
    

def _toGlobalPath(path: str):
    return glob(path, recursive=True)

parser = argparse.ArgumentParser(description='Petrinet recognizer 1.0.')
#parser.add_argument('--files', dest='files', nargs='+',
                   #help='glob to textfile(s) containing inkml file names', default=['./__datasets__/FA_1.1/no_text/FA_Train.txt', './__datasets__/FA_1.1/no_text/FA_Validation.txt'])
#parser.add_argument('--files', dest='files', nargs='+',
                    #help='glob to textfile(s) containing inkml file names', default=['./__datasets__/FC_1.0/no_text/no_junk/FC_Train.txt', './__datasets__/FC_1.0/no_text/no_junk/FC_Validation.txt'])
parser.add_argument('--files', dest='files', nargs='+',
                    help='glob to textfile(s) containing inkml file names', default=['./__datasets__/PN_1.0/PN_Test.txt'])
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
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)   
resampled_content = None
content = None

# while get_threshold() < 1:
    
evaluationWrapper = None if args.production else EvaluationWrapper(RECOGNIZERS[args.recognizer], connection_grouper)
recognizer = RECOGNIZERS[args.recognizer] if args.production else evaluationWrapper.recognize
connection_localizer = connection_grouper if args.production else evaluationWrapper.group_connections
grouper = GROUPERS[args.grouper]
shape_no_shape_features = None
rectangle_features = None
circle_features = None
files_wo_es_nicht_geklappt_hat = []

# next_threshold()
# print('WHILE Lopp: Threshold:', get_threshold())
for i, path in enumerate(file_paths):
    print('Processing file: ', path, i , 'of', len(file_paths))
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    

    evaluationWrapper.setCurrentFilePath(path) if not args.production else None
    content = parse_strokes_from_inkml_file(path)
    if args.other_ratio:
        ratio = args.other_ratio.split('/')
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        candidates = grouper(resampled_content)
        
    else:
        if 'FC' in path:
            ratio = [59414,49756]
            converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
            resampled_content = resample_strokes(converted_strokes)
            candidates = grouper(resampled_content)
        elif 'FA' in path:
            ratio = [48484,26442]
            converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
            resampled_content = resample_strokes(converted_strokes)
            candidates = grouper(resampled_content)
        elif 'PN' in path:
            ratio = parse_ratio_from_inkml_file(path)
            converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
            resampled_content = resample_strokes(converted_strokes)
            candidates = grouper(resampled_content)
    
    if not args.production:
        evaluationWrapper.set_amount_of_invalid_candidates(candidates)
        
    results = []
    recognized_strokes = []
    unrecognized_strokes = []
    candidates_already_checked = []
    for i,candidate in enumerate(candidates):
        # check if no values from the candidate are in recognized_strokes
        if not any(recognized_stroke in candidate for recognized_stroke in recognized_strokes):
            recognizer_result, shape_no_shape_features, rectangle_features = recognizer({'use': REJECTORS[args.rejector], 'name':args.rejector},  {'use': CLASSIFIERS[args.classifier], 'name': args.classifier}, candidate, resampled_content)
            candidates_already_checked.append(candidate)
            if not shape_no_shape_features:
                shape_no_shape_features = shape_no_shape_features
            if not rectangle_features:
                rectangle_features = rectangle_features
            if 'valid' in recognizer_result:
                recognized_strokes.extend(candidate)
                results.append(recognizer_result)
    unrecognized_strokes = get_unrecognized_strokes(recognized_strokes, resampled_content)
    evaluationWrapper.save_time() if not args.production else None
    shape_strokes = []
    
    # truth = parse_ground_truth(path)
    # for dictionary in truth:
    #     for shape_name, trace_ids in dictionary.items():
            
    #         # Normalize candidates by sorting and converting to tuples
    #         normalized_candidates = set(tuple(sorted(candidate)) for candidate in candidates)


    #         # Normalize trace_ids by sorting and converting to a tuple
    #         normalized_trace_ids = tuple(sorted(trace_ids))

    #         # Check if normalized_trace_ids is in normalized_candidates
    #         if 'rectangle' == shape_name and normalized_trace_ids not in normalized_candidates:
    #             print('Rectangle not found', normalized_trace_ids, path)
    #             files_wo_es_nicht_geklappt_hat.append(path)
                
                
    #             exit()
    for i, shape in enumerate(results):
        shape_name = list(shape['valid'].keys())[0]
        if shape_name == 'circle':
            shape_strokes.append({'shape_name': shape_name , 'shape_id': 'p' + str(i), 'shape_candidates': shape['valid'][next(iter(shape['valid']))], 'shape_strokes': get_strokes_from_candidate(shape['valid'][next(iter(shape['valid']))], resampled_content)})
        elif shape_name == 'rectangle':
            shape_strokes.append({'shape_name': shape_name , 'shape_id': 't' + str(i), 'shape_candidates': shape['valid'][next(iter(shape['valid']))], 'shape_strokes': get_strokes_from_candidate(shape['valid'][next(iter(shape['valid']))], resampled_content)})

            
    edges = connection_localizer(shape_strokes, unrecognized_strokes)
   
    results.extend(edges)


if not args.production:
    evaluationWrapper.set_total()
    evaluationWrapper.set_accuracy()
    print(evaluationWrapper)
    print()
    print(evaluationWrapper.get_connection_evaluation())
    

if args.save == 'y':
    print('Saving results to file...')
    file_name1 = 'evaluation_results/results' + str(datetime.datetime.now()) +'.csv'
    file_name2 = 'evaluation_results/connection_results' + str(datetime.datetime.now()) +'.csv'
    evaluationWrapper.matrix.to_csv(file_name1)
    evaluationWrapper.matrix2.to_csv(file_name2)
    with open(file_name1, 'a') as f:
        f.write('# dataset: ' + str(args.files) + '\n')
        f.write('# grouper: ' + str(args.grouper) + '\n')
        f.write('# classifier: ' + str(args.classifier) + '\n')
        f.write('# rejector: ' + str(args.rejector) + '\n')
        f.write('# shape no shape features: '+ ''.join(shape_no_shape_features) +'\n')
        f.write('# circle rectangle features: '+ ''.join(rectangle_features) +'\n')
        f.write('# rejector threshold: '+ str(get_threshold()) +'\n')
    with open(file_name2, 'a') as f:
        f.write('# dataset: ' + str(args.files) + '\n')
        f.write('# grouper: ' + str(args.grouper) + '\n')
        f.write('# classifier: ' + str(args.classifier) + '\n')
        f.write('# rejector: ' + str(args.rejector) + '\n')
        f.write('# shape no shape features: '+ ''.join(shape_no_shape_features) +'\n')
        f.write('# circle rectangle features: '+ ''.join(rectangle_features) +'\n')
        f.write('# rejector threshold: '+ str(get_threshold()) +'\n')

    

if args.production:
    file_name = args.inkml[0].split('/')[-1].split('.')[0]
    with open(f'inkml_results/{file_name}.json', 'a') as f:
        f.write('[')
    id_counter = 0
    for result in results:
        shape_name = next(iter(result['valid']))
        candidates = result['valid'][shape_name]
        if not shape_name == 'line':
            strokes_of_candidate= get_strokes_from_candidate(candidates, content)
        else:
            strokes_of_source_candidate = get_strokes_from_candidate(result['valid']['line']['source'], content)
            strokes_of_target_candidate = get_strokes_from_candidate(result['valid']['line']['target'], content)
          
        if shape_name == 'rectangle':
            shape_id = 't' + str(id_counter)
        elif shape_name == 'circle':
            shape_id = 'p' + str(id_counter)
        elif shape_name == 'line':
            shape_id = 'l' + str(id_counter)
       
        # x and y values are being adapted to the canvas size of the petri net editors from I love petri nets
        if shape_name == 'line':
            source_min_x, source_min_y, source_max_x, source_max_y, source_width, source_height = get_position_values(strokes_of_source_candidate)
            target_min_x, target_min_y, target_max_x, target_max_y, target_width, target_height = get_position_values(strokes_of_target_candidate)
            height_factor_source = 80 / (source_min_y + source_max_y)
            height_factor_target = 80 / (target_min_y + target_max_y)
            line_candidate = [resampled_content.index(result['valid']['line']['stroke'])]
            result_obj = {'shape_name': shape_name, 'source_min_x': source_min_x, 'source_min_y': source_min_y, 'source_max_x': source_max_x, 'source_max_y': source_max_y, 'target_min_x': target_min_x , 'target_min_y': target_min_y, 'target_max_x': target_max_x, 'target_max_y': target_max_y, 'shape_id': shape_id, 'target_id': result['valid']['line']['target_id'], 'source_id': result['valid']['line']['source_id'], 'candidate': line_candidate}
        else:
            min_x, min_y, max_x, max_y, width, height = get_position_values(strokes_of_candidate)
            result_obj = {'shape_name': shape_name,'min_x': min_x, 'min_y': min_y, 'max_x': max_x, 'max_y': max_y, 'width': width, 'height': height, 'shape_id': shape_id, 'candidates': candidates}
        with open(f'inkml_results/{file_name}.json', 'a') as f:
            json.dump(result_obj, f, indent=4)
            if id_counter < len(results) - 1:
                f.write(',\n')
        id_counter += 1
            
        
    
    with open(f'inkml_results/{file_name}.json', 'a') as f:
        f.write(']')
        
    
import argparse
from glob import glob  
from grouper.thesis_grouper import group as thesis_grouper
from grouper.optimized_grouper import group as optimized_grouper
from recognizer.random_mock_recognizer import is_a_shape as random_mock_recognizer
from recognizer.perfect_mock_recognizer import is_a_shape as perfect_mock_recognizer
from recognizer.template_matching_recognizer import is_a_shape as template_matching_recognizer
from helper.EvaluationWrapper import EvaluationWrapper
from helper.parsers import parse_strokes_from_inkml_file
from helper.normalizer import normalize
import os
from helper.print_progress_bar import printProgressBar
import datetime


GROUPERS = {
    'thesis_grouper' : thesis_grouper,
    'optimized_grouper' : optimized_grouper
}

RECOGNIZERS = {
    'random_mock_recognizer' : random_mock_recognizer,
    'perfect_mock_recognizer' : perfect_mock_recognizer,
    'template_matching_recognizer' : template_matching_recognizer
}
    

def _toGlobalPath(path: str):
    return glob(path, recursive=True)

parser = argparse.ArgumentParser(description='Petrinet recognizer 0.1.')

parser.add_argument('--files', dest='files', type=_toGlobalPath, nargs='?',action='store',
                    help='glob to textfile(s) containing inkml file names', default='./__datasets__/FA_1.1/no_text/FA_Train.txt')
parser.add_argument('--inkml', dest='inkml', type=_toGlobalPath, nargs='?', action='store', default='',
                    help='glob to inkml file(s)')
parser.add_argument('--grouper', dest='grouper', type=str, nargs='?', action='store', default='optimized_grouper',
                    help='select a grouping algorithm, thesis_grouper or optimized_grouper')
parser.add_argument('--recognizer', dest='recognizer', type=str, nargs='?', action='store', default='template_matching_recognizer',
                    help='select a recognition algorithm, random_mock_recognizer, perfect_mock_recognizer or template_matching_recognizer')
parser.add_argument('--production', dest='production', type=bool, nargs='?', action='store', default=False,
                    help='determines if we run with evaluation logic or not')
parser.add_argument('--save', dest='save', type=str, nargs='?', action='store', default='n',
                    help='determines if we save the results to a file or not')
parser.add_argument('--params', dest='params', type=str, nargs='?', action='store', default='50,6,110, 54')

args = parser.parse_args()

evaluationWrapper = None if args.production else EvaluationWrapper(RECOGNIZERS[args.recognizer])
recognizer = RECOGNIZERS[args.recognizer] if args.production else evaluationWrapper.is_a_shape
grouper = GROUPERS[args.grouper]

if args.params:
    # set params if any
    evaluationWrapper.set_params(*args.params.split(','))

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
    
for i, path in enumerate(file_paths):
   
    evaluationWrapper.setCurrentFilePath(path) if not args.production else None
    content = parse_strokes_from_inkml_file(path)
    
    candidates = grouper(content)
    normalized_content = normalize(content)
    results = []
    for candidate in candidates:
        results.append(recognizer(candidate, normalized_content))
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
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
        f.write('# recognizer: ' + str(args.recognizer) + '\n')
        f.write('# stroke_min: ' + str(evaluationWrapper.stroke_min) + '\n')
        f.write('# diagonal_to_stroke_length: ' + str(evaluationWrapper.diagonal_to_stroke_length) + '\n')
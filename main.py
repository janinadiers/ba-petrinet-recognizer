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
                    help='glob to textfile(s) containing inkml file names', default='./__datasets__/FA_1.1/no_text/FA_Test.txt')
parser.add_argument('--inkml', dest='inkml', type=_toGlobalPath, nargs='?', action='store', default='',
                    help='glob to inkml file(s)')
parser.add_argument('--grouper', dest='grouper', type=str, nargs='?', action='store', default='optimized_grouper',
                    help='select a grouping algorithm, thesis_grouper or optimized_grouper')
parser.add_argument('--recognizer', dest='recognizer', type=str, nargs='?', action='store', default='template_matching_recognizer',
                    help='select a recognition algorithm, random_mock_recognizer, perfect_mock_recognizer or template_matching_recognizer')
parser.add_argument('--production', dest='production', type=bool, nargs='?', action='store', default=False,
                    help='determines if we run with evaluation logic or not')


args = parser.parse_args()

evaluationWrapper = None if args.production else EvaluationWrapper(RECOGNIZERS[args.recognizer])
recognizer = RECOGNIZERS[args.recognizer] if args.production else evaluationWrapper.is_a_shape
grouper = GROUPERS[args.grouper]

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
    
    
for path in file_paths:
    evaluationWrapper.setCurrentFilePath(path) if not args.production else None
    content = parse_strokes_from_inkml_file(path)
    candidates = grouper(content)
    normalized_content = normalize(content)
    
    results = []
    for candidate in candidates:
        results.append(recognizer(candidate, normalized_content))
if not args.production:
    print(evaluationWrapper)



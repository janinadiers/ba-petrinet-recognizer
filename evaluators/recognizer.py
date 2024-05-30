
import os
from optimized_grouper import group as group_optimized
from grouper import group
from parsers import parse_ground_truth, parse_strokes_from_inkml_file, exclude_text_strokes
import time
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix
from distance_calculators.distance_with_bounding_box import initialize_adjacency_matrix as initialize_adjacency_matrix2
from distance_calculators.distance_with_average_of_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix3
# from recognizer.perfect_mock_recognizer import is_a_shape
from recognizer.random_recognizer import is_a_shape as random_is_a_shape
from recognizer.recognizer import is_a_shape
from normalizer import normalize
from collections import Counter




def get_amount_valid_shapes(expected_shapes:list[dict]) -> int:
    amount = 0
    for shape in expected_shapes:
        shape_name = next(iter(shape))
        
        if (shape_name == 'circle' or shape_name == 'rectangle'):
            amount += 1
    return amount

def dict_to_hashable(d):
    # Converts each dictionary to a hashable tuple.
    # Sort lists that are values of the dictionary to handle unordered comparisons.
    return tuple((key, tuple(sorted(value)) if isinstance(value, list) else value)
                 for key, value in sorted(d.items()))


def get_amount_correctly_recognized_shapes(recognized_shapes: list[dict], expected_shapes: list[dict]) -> int:
    # Convert lists of dictionaries to hashable tuples using the helper function.
    rec_shapes_tuples = [dict_to_hashable(shape) for shape in recognized_shapes]
    exp_shapes_tuples = [dict_to_hashable(shape) for shape in expected_shapes]

    # Create Counters for both lists to handle duplicate shapes with counts.
    rec_shapes_counter = Counter(rec_shapes_tuples)
    exp_shapes_counter = Counter(exp_shapes_tuples)

    # Intersection of counters to get the minimum count of identical items.
    common_shapes = rec_shapes_counter & exp_shapes_counter
    total_recognized = sum(common_shapes.values())

    return total_recognized
    
def get_average_run_time(runtimes:list) -> time:
    sum = 0
    for runtime in runtimes:
        sum += runtime
    return sum / len(runtimes)


def normalize_all_strokes(strokes:list[dict]) -> list[dict]:
    normalized_strokes = []
    for stroke in strokes:
        stroke_points = next(iter(stroke.values()))
        normalized_points = normalize(stroke_points)
        # Add the normalized points to the stroke
        stroke[next(iter(stroke))] = normalized_points
        # add the stroke to the list of normalized strokes
        normalized_strokes.append(stroke)
    # return the list of normalized strokes
    return normalized_strokes

def get_filenames(modus:str, dataset_type:str) -> list[str]:
    filenames = []
    if modus == 'ALL' and dataset_type == 'BOTH':
        filenames.append('FC_Test.txt')
        filenames.append('FA_Test.txt')
        filenames.append('FC_Train.txt')
        filenames.append('FA_Train.txt')
        filenames.append('FC_Validation.txt')
        filenames.append('FA_Validation.txt')
    if modus == 'TEST' and dataset_type == 'FA':
        filenames.append('FA_Test.txt')
    elif modus == 'TEST' and dataset_type == 'FC':
        filenames.append('FC_Test.txt')
    elif modus == 'TRAIN' and dataset_type == 'FA':
        filenames.append('FA_Train.txt')
    elif modus == 'TRAIN' and dataset_type == 'FC':
        filenames.append('FC_Train.txt')
    elif modus == 'V' and dataset_type == 'FA':
        filenames.append('FA_Validation.txt')
    elif modus == 'V' and dataset_type == 'FC':
        filenames.append('FC_Validation.txt')
    elif modus == 'ALL' and dataset_type == 'FA':
        filenames.append('FA_Test.txt')
        filenames.append('FA_Train.txt')
        filenames.append('FA_Validation.txt')
    elif modus == 'ALL' and dataset_type == 'FC':
        filenames.append('FC_Test.txt')
        filenames.append('FC_Train.txt')
        filenames.append('FC_Validation.txt')
    elif modus == 'TRAIN' and dataset_type == 'BOTH':
        filenames.append('FC_Train.txt')
        filenames.append('FA_Train.txt')
    elif modus == 'TEST' and dataset_type == 'BOTH':
        filenames.append('FC_Test.txt')
        filenames.append('FA_Test.txt')
    elif modus == 'V' and dataset_type == 'BOTH':
        filenames.append('FC_Validation.txt')
        filenames.append('FA_Validation.txt')
    elif modus == 'development' and dataset_type == 'BOTH':
        filenames.append('FA_Train.txt')
        filenames.append('FC_Train.txt')
        filenames.append('FA_Validation.txt')
        filenames.append('FC_Validation.txt')
    elif modus == 'development' and dataset_type == 'FA':
        filenames.append('FA_Train.txt')
        filenames.append('FA_Validation.txt')   
    elif modus == 'development' and dataset_type == 'FC':
        filenames.append('FC_Train.txt')
        filenames.append('FC_Validation.txt')
    elif modus == 'evaluation' and dataset_type == 'BOTH':
        filenames.append('FA_Test.txt')
        filenames.append('FC_Test.txt')
    elif modus == 'evaluation' and dataset_type == 'FA':
        filenames.append('FA_Test.txt')
    elif modus == 'evaluation' and dataset_type == 'FC':
        filenames.append('FC_Test.txt')
    return filenames

def file_path_endswith(file_path:str, filenames:str) -> bool:
    for filename in filenames:
        if file_path.endswith(filename):
            return True
    return False
    

def evaluate_recognizer(paths:list, modus:str='ALL', dataset_type:str = 'BOTH') -> None:
    amount_valid_shapes:int = 0
    amount_correctly_recognized_shapes:int = 0
    amount_recognizer_calls:int = 0
    stroke_amount:int = 0
    filenames = get_filenames(modus, dataset_type)
    

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path_endswith(file_path, filenames):
                    runtimes = []
                    with open(file_path) as f:
                        content = f.readlines()
                        print('diagrams: ', len(content))
                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file:str = os.path.dirname(file_path) + '/' + line.strip()
                        
                        test_file_without_text = exclude_text_strokes(test_file)
                        expected_shapes:list[dict] = parse_ground_truth(test_file_without_text)
                        # expected_shapes:list[dict] = parse_ground_truth(test_file)
                        strokes:list[dict] = parse_strokes_from_inkml_file(test_file_without_text)
                        # strokes:list[dict] = parse_strokes_from_inkml_file(test_file)  
                        stroke_amount += len(strokes)                      
                        start_time = time.time()  # Startzeit speichern
                        grouped_strokes:dict = group_optimized(strokes, is_a_shape, initialize_adjacency_matrix, expected_shapes)
                        end_time = time.time()  # Endzeit speichern
                        elapsed_time = end_time - start_time  # Differenz berechnen
                        runtimes.append(elapsed_time)
                        amount_recognizer_calls += grouped_strokes['recognizer calls']
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print(expected_shapes)
                        amount_valid_shapes += get_amount_valid_shapes(expected_shapes)
                        amount_correctly_recognized_shapes += get_amount_correctly_recognized_shapes(grouped_strokes['recognized shapes'], expected_shapes)
                        print(test_file)
                        print(amount_correctly_recognized_shapes, ' / ', amount_valid_shapes, 'richtig erkannt')
                    # print('Aufrufe des recognizers: ', amount_recognizer_calls)
                    print('average run time: ', get_average_run_time(runtimes))
  
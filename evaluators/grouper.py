
import os
from grouper import group
from parsers import parse_ground_truth, parse_strokes_from_inkml_file, exclude_text_strokes
import time
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix
from distance_calculators.distance_with_bounding_box import initialize_adjacency_matrix as initialize_adjacency_matrix2
from distance_calculators.distance_with_average_of_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix3
from recognizer.perfect_mock_recognizer import is_a_shape, get_count
from normalizer import normalize


def get_amount_valid_shapes(expected_shapes:list[dict]) -> int:
    amount = 0
    for shape in expected_shapes:
        shape_name = next(iter(shape))
        if (shape_name == 'circle' or shape_name == 'rectangle'):
            amount += 1
    return amount

def get_amount_correctly_recognized_shapes(recognized_shapes:list[dict], expected_shapes:list[dict]) -> int:
    amount = 0
    for shape1 in recognized_shapes:
        for shape2 in expected_shapes:
            if(shape1 == shape2):
                amount += 1
    return amount

    
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
        # filenames.append('FC_Validation.txt')
        # filenames.append('FA_Validation.txt')
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
        # filenames.append('FA_Validation.txt')
    elif modus == 'ALL' and dataset_type == 'FC':
        filenames.append('FC_Test.txt')
        filenames.append('FC_Train.txt')
        # filenames.append('FC_Validation.txt')
    elif modus == 'TRAIN' and dataset_type == 'BOTH':
        filenames.append('FC_Train.txt')
        filenames.append('FA_Train.txt')
    elif modus == 'TEST' and dataset_type == 'BOTH':
        filenames.append('FC_Test.txt')
        filenames.append('FA_Test.txt')
    elif modus == 'V' and dataset_type == 'BOTH':
        filenames.append('FC_Validation.txt')
        filenames.append('FA_Validation.txt')
    return filenames

def file_path_endswith(file_path:str, filenames:str) -> bool:
    for filename in filenames:
        if file_path.endswith(filename):
            return True
    return False
    

def evaluate_grouper(paths:list, modus:str='ALL', dataset_type:str = 'BOTH') -> None:
    amount_valid_shapes:int = 0
    amount_correctly_recognized_shapes:int = 0
    amount_counter:int = 0
    
    filenames = get_filenames(modus, dataset_type)
    
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path_endswith(file_path, filenames):
                    runtimes = []
                    with open(file_path) as f:
                        content = f.readlines()
                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file:str = os.path.dirname(file_path) + '/' + line.strip()
                        # test_file_without_text = exclude_text_strokes(test_file)
                        # expected_shapes:list[dict] = parse_ground_truth(test_file_without_text)
                        expected_shapes:list[dict] = parse_ground_truth(test_file)
                        # strokes:list[dict] = parse_strokes_from_inkml_file(test_file_without_text)
                        strokes:list[dict] = parse_strokes_from_inkml_file(test_file)
                        start_time = time.time()  # Startzeit speichern
                        grouped_strokes:dict = group(strokes, is_a_shape, initialize_adjacency_matrix, expected_shapes)
                        end_time = time.time()  # Endzeit speichern
                        elapsed_time = end_time - start_time  # Differenz berechnen
                        runtimes.append(elapsed_time)
                        amount_counter += grouped_strokes['counter']
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print('recognizer count: ', get_count())
                        amount_valid_shapes += get_amount_valid_shapes(expected_shapes)
                        amount_correctly_recognized_shapes += get_amount_correctly_recognized_shapes(grouped_strokes['recognized shapes'], expected_shapes)
                        print(amount_correctly_recognized_shapes, ' / ', amount_valid_shapes, 'richtig erkannt')
                    print('Aufrufe des recognizers ohne memoization: ', amount_counter)
                    print('average run time: ', get_average_run_time(runtimes))
  
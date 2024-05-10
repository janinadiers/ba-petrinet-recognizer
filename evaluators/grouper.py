
import os
from grouper import group, get_average_time_for_initialization
from parsers import parse_ground_truth, parse_strokes_from_inkml_file
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
    

def evaluate_grouper(path:str, modus:str='ALL', dataset_type:str = 'BOTH') -> None:
    amount_valid_shapes:int = 0
    amount_correctly_recognized_shapes:int = 0
    if dataset_type == 'FA' or dataset_type == 'FC':
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if(file_path.endswith('FC_Test.txt')):
                    with open(file_path) as f:
                        content = f.readlines()

                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file:str = os.path.dirname(file_path) + '/' + line.strip()
                        print(test_file)
                        expected_shapes:list[dict] = parse_ground_truth(test_file)
                        strokes:list[dict] = parse_strokes_from_inkml_file(test_file)
                        strokes = normalize_all_strokes(strokes)
                        start_time = time.time()  # Startzeit speichern
                        grouped_strokes:dict = group(strokes, is_a_shape, initialize_adjacency_matrix3, expected_shapes)
                        end_time = time.time()  # Endzeit speichern
                        elapsed_time = end_time - start_time  # Differenz berechnen
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print('recognizer count: ', get_count())
                        amount_valid_shapes += get_amount_valid_shapes(expected_shapes)
                        amount_correctly_recognized_shapes += get_amount_correctly_recognized_shapes(grouped_strokes['recognized shapes'], expected_shapes)
                        print(amount_correctly_recognized_shapes, ' / ', amount_valid_shapes, 'richtig erkannt')
                    print('average time for initialization: ', get_average_time_for_initialization() / len(content))
  

import os
from optimized_grouper import group as group_optimized
from grouper import group
from parsers import parse_ground_truth, parse_strokes_from_inkml_file, exclude_text_strokes
import time
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix
from distance_calculators.distance_with_bounding_box import initialize_adjacency_matrix as initialize_adjacency_matrix2
from distance_calculators.distance_with_average_of_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix3
from recognizer.random_recognizer import is_a_shape as random_is_a_shape
from recognizer.recognizer import is_a_shape
from normalizer import normalize
from Recognition_Result import RecognitionResult


def add_shapes_to_recognition_result(recognition_result, test_file_without_text) -> None:
    expected_shapes:list[dict] = parse_ground_truth(test_file_without_text)
    recognition_result.valid_shapes = []
    recognition_result.shapes = []
    for shape in expected_shapes:
        shape_name = next(iter(shape))
        if (shape_name == 'circle' or shape_name == 'rectangle'):
            recognition_result.add_valid_shape(shape)
        
        recognition_result.add_shape(shape)

def normalize_all_strokes(strokes:list[dict]) -> list[dict]:
    for i in range(len(strokes)):
        strokes[i] = normalize(strokes[i])
    return strokes
    

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
    
    filenames = get_filenames(modus, dataset_type)
    recognition_result = RecognitionResult()

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path_endswith(file_path, filenames):
                    with open(file_path) as f:
                        content = f.readlines()
                        print('diagrams: ', len(content))
                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file:str = os.path.dirname(file_path) + '/' + line.strip()
                        test_file_without_text = exclude_text_strokes(test_file)
                        add_shapes_to_recognition_result(recognition_result, test_file_without_text)
                        strokes:list[dict] = parse_strokes_from_inkml_file(test_file_without_text) 
                        strokes = normalize_all_strokes(strokes)
                        start_time = time.time()
                        group_optimized(strokes, is_a_shape, initialize_adjacency_matrix, recognition_result)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        recognition_result.runtimes.append(elapsed_time)
                        print(recognition_result.get_shapes())
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print(recognition_result.get_amount_correctly_recognized_shapes(), ' / ', recognition_result.get_amount_valid_shapes(), 'richtig erkannt')
                        print(recognition_result.get_amount_correctly_rejected_shape_candidates(), '/', recognition_result.get_amount_invalid_shape_candidates(), 'richtig abgelehnt')
                    
                    print('Aufrufe des recognizers: ', recognition_result.get_recognizer_calls())
                    print('Kreis mit Rechteck verwechselt: ', recognition_result.get_amount_circle_confusion()['rectangle'])
                    print('Kreis mit Ellipse verwechselt: ', recognition_result.get_amount_circle_confusion()['ellipse'])
                    print('Kreis mit Linie verwechselt: ', recognition_result.get_amount_circle_confusion()['line'])
                    print('Kreis mit Diamant verwechselt: ', recognition_result.get_amount_circle_confusion()['diamond'])
                    print('Kreis mit Parallelogramm verwechselt: ', recognition_result.get_amount_circle_confusion()['parallelogram'])
                    print('Kreis mit Kreis im Kreis verwechselt: ', recognition_result.get_amount_circle_confusion()['circle_in_circle'])
                    print('Rechteck mit Kreis verwechselt: ', recognition_result.get_amount_rectangle_confusion()['circle'])
                    print('Rechteck mit Ellipse verwechselt: ', recognition_result.get_amount_rectangle_confusion()['ellipse'])
                    print('Rechteck mit Linie verwechselt: ', recognition_result.get_amount_rectangle_confusion()['line'])
                    print('Rechteck mit Diamant verwechselt: ', recognition_result.get_amount_rectangle_confusion()['diamond'])
                    print('Rechteck mit Parallelogramm verwechselt: ', recognition_result.get_amount_rectangle_confusion()['parallelogram'])
                    print('Rechteck mit Kreis im Kreis verwechselt: ', recognition_result.get_amount_rectangle_confusion()['circle_in_circle'])
                    print('average run time: ', recognition_result.get_average_run_time())
  
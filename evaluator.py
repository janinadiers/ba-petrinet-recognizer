import sys
import os
from grouper import group, get_average_time_for_initialization
from parsers import parse_ground_truth, parse_traces_from_inkml_file
import time
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix as initialize_adjacency_matrix
from distance_calculators.distance_with_bounding_box import initialize_adjacency_matrix as initialize_adjacency_matrix2
from recognizer.perfectMockRecognizer import is_a_shape, get_count


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


def evaluate_grouper(path:str, dataset_type:str = 'Both') -> None:
    amount_valid_shapes:int = 0
    amount_correctly_recognized_shapes:int = 0
    if dataset_type == 'FA' or dataset_type == 'FC':
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if(file_path.endswith('FA_Test.txt')):
                    with open(file_path) as f:
                        content = f.readlines()

                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file:str = os.path.dirname(file_path) + '/' + line.strip()
                        expected_shapes:list[dict] = parse_ground_truth(test_file)
                        traces:list[dict] = parse_traces_from_inkml_file(test_file)
                        start_time = time.time()  # Startzeit speichern
                        grouped_traces:dict = group(traces, is_a_shape, initialize_adjacency_matrix2, expected_shapes)
                        end_time = time.time()  # Endzeit speichern
                        elapsed_time = end_time - start_time  # Differenz berechnen
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print('recognizer count: ', get_count())
                        amount_valid_shapes += get_amount_valid_shapes(expected_shapes)
                        amount_correctly_recognized_shapes += get_amount_correctly_recognized_shapes(grouped_traces['recognized shapes'], expected_shapes)
                        print(amount_correctly_recognized_shapes, ' / ', amount_valid_shapes, 'richtig erkannt')
                        print('average time for initialization: ', get_average_time_for_initialization(), len(content))
                    print('average time for initialization: ', get_average_time_for_initialization() / len(content))
  
                       
        
                                                  

# get input from command line: --fa or --fc or both

if len(sys.argv) < 2:
    path = ["datasets/FC_1.0", "../../../datasets/FA_1.1"] 
elif(sys.argv[1] == '--fa'):
    path = "datasets/FA_1.1"
    evaluate_grouper(path, 'FA')
elif(sys.argv[1] == '--fc'):
    path = "datasets/FC_1.0"

    



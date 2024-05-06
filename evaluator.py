import sys
import os
from parser import parse_traces_from_inkml_file
from parser import parse_ground_truth
from parser import parse_shape_types_with_amount_of_occurence
from grouper import group
from helpers import count_common_elements, count_different_elements
from helpers import trace_ids_are_unique, get_shape_names, count_shape, count_correctly_recognized_shape_name
from collections import Counter
from prettytable import PrettyTable
import time
from distance_calculators.distance_between_all_points import DistanceBetweenAllPoints
from distance_calculators.distance_with_bounding_box import DistanceWithBoundingBox
from recognizer.PerfectMockRecognizer import PerfectMockRecognizer



def check_soundness(grouped_traces):
    # Jeder Form sollte mind. eine traceId zugeordnet sein
    for shape in grouped_traces:
        if not len(shape[next(iter(shape))]) > 0:
            raise ValueError('expected shape list contains shape without trace ID!')
    
    # Keine traceId doppelt, sowohl in expected als auch in actual
    if not trace_ids_are_unique(grouped_traces):
        raise ValueError('expected shape list or actual shape list contains duplicate trace ID!')
    else:
        return True

def amount_of_diamonds_accidentaly_recognized_as_circle(recognized_circle, expected_shapes):
    amount = 0
    for shape in expexted_shapes:
        if 'diamond' in shape and recognized_circle in shape.values():
            amount += 1
    return amount

def amount_of_line_accidentaly_recognized_as_circle(recognized_circle, expected_shapes):
    amount = 0
    for shape in expexted_shapes:
        if 'line' in shape and recognized_circle in shape.values():
            print('line recognized as circle: ', shape)
            amount += 1
    return amount


                





def start_shape_recognition(traces, expected_shapes):
    search_space = [] + traces
    recognized_shapes = []
   
    for trace in search_space:
        shape_candidate = trace
        grouped_traces = group_strokes(shape_candidate)
        # print('grouped traces: ', grouped_traces)
        result = is_a_shape(grouped_traces)
        if 'valid' in result:
            recognized_shapes.append(result['valid'])
            search_space.remove(shape_candidate)
        else:
            search_space.remove(shape_candidate)
    return recognized_shapes       

def evaluate_recognizer(path, dataset_type = 'Both'):
    circle_amount = 0
    rectangle_amount = 0
    circle_in_circle_amount = 0
    line_amount = 0
    parallelogram_amount = 0
    diamond_amount = 0
    ellipse_amount = 0
    text_amount = 0
    circle_as_circle = 0
    rectangle_as_rectangle = 0
    circle_as_diamond = 0
    circle_as_line = 0
    circle_as_ellipse = 0
    circle_as_parallelogram = 0
    circle_as_text = 0
    circle_as_circle_in_circle = 0
    circle_as_rectangle = 0
    rectangle_as_circle = 0
    rectangle_as_diamond = 0
    rectangle_as_line = 0
    rectangle_as_ellipse = 0
    rectangle_as_parallelogram = 0
    rectangle_as_text = 0
    rectangle_as_circle_in_circle = 0
    
    
    
    if dataset_type == 'FA' or dataset_type == 'FC':
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # get all test inkml files
                if(file_path.endswith('_fake_Test.txt')):
                    with open(file_path) as f:
                        content = f.readlines()
                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        
                        test_file = os.path.dirname(file_path) + '/' + line.strip()
                        expected_shapes = parse_ground_truth(test_file)
                        print('expected shapes: ', expected_shapes)
                        circle_amount += count_shape(expected_shapes, 'circle')
                        
                        rectangle_amount += count_shape(expected_shapes, 'rectangle')
                        circle_in_circle_amount += count_shape(expected_shapes, 'circle in circle')
                        line_amount += count_shape(expected_shapes, 'line')
                        parallelogram_amount += count_shape(expected_shapes, 'parallelogram')
                        diamond_amount += count_shape(expected_shapes, 'diamond')
                        ellipse_amount += count_shape(expected_shapes, 'ellipse')
                        text_amount += count_shape(expected_shapes, 'text')
                        traces = parse_traces_from_inkml_file(test_file)
                        recognized_shapes = start_shape_recognition(traces, expected_shapes)
                        print('recognized shapes: ', recognized_shapes)
                        test(recognized_shapes, expected_shapes)
                        circle_as_circle += count_correctly_recognized_shape_name(recognized_shapes, expected_shapes, 'circle')
                        rectangle_as_rectangle += count_correctly_recognized_shape_name(recognized_shapes, expected_shapes, 'rectangle')

                        # check if the traces are sound: no duplicate trace ids and each shape has at least one trace id
                        check_soundness(recognized_shapes)
                        check_soundness(expected_shapes)
       
        column_headers = ['Circle', 'Rectangle', '-']
        rows = []
        for shape_name in get_shape_names(expected_shapes):
            row = [shape_name]
            for column in column_headers:
                if(column == 'Circle') and (shape_name == 'circle'):
                    row.append(str(circle_as_circle) + ' / ' + str(circle_amount))
                elif(column == 'Rectangle') and (shape_name == 'rectangle'):
                    row.append(str(rectangle_as_rectangle) + ' / ' + str(rectangle_amount))
                elif shape_name == 'circle in circle':
                    row.append('0 / '+ str(circle_in_circle_amount) )
                elif shape_name == 'line':
                    row.append('0 / ' + str(line_amount) )
                elif shape_name == 'parallelogram':
                    row.append('0 / ' + str(parallelogram_amount ))
                elif shape_name == 'diamond':
                    row.append('0 / ' + str(diamond_amount ))
                elif shape_name == 'ellipse':
                    row.append('0 / ' + str(ellipse_amount ))
                elif shape_name == 'text':
                    row.append('0 / ' + str(text_amount ))
                else:
                    row.append('0 / 0')
            rows.append(row)
        
        # Create a table
        table = PrettyTable()
        table.field_names = [" "] + column_headers  # Add an empty space for the row headers

        # Add rows to the table
        for row in rows:
            table.add_row(row)
        
        print(table)
        
    elif dataset_type == 'Both':
        pass      

def get_amount_valid_shapes(expected_shapes):
    amount = 0
    for shape in expected_shapes:
        if (next(iter(shape)) == 'circle' or next(iter(shape)) == 'rectangle'):
            amount += 1
    return amount

def get_amount_correctly_recognized_shapes(recognized_shapes, expected_shapes):
    amount = 0
    for shape1 in recognized_shapes:
        for shape2 in expected_shapes:
            if(shape1 == shape2):
                amount += 1
    return amount


def evaluate_grouper(path, dataset_type = 'Both'):
    amount_valid_shapes = 0
    amount_correctly_recognized_shapes = 0
    
    if dataset_type == 'FA' or dataset_type == 'FC':
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # get all test inkml files
                if(file_path.endswith('FA_Test.txt')):
                    with open(file_path) as f:
                        content = f.readlines()
                    for line in content:
                        line = line.strip()
                        if not line.endswith('.inkml'):
                            continue
                        test_file = os.path.dirname(file_path) + '/' + line.strip()
                        expected_shapes = parse_ground_truth(test_file)
                        print('expected shapes: ', expected_shapes)
                        traces = parse_traces_from_inkml_file(test_file)
                        start_time = time.time()  # Startzeit speichern
                        perfect_mock_recognizer = PerfectMockRecognizer(expected_shapes)
                        grouped_traces = group(traces, perfect_mock_recognizer, DistanceWithBoundingBox())
                        end_time = time.time()  # Endzeit speichern
                        elapsed_time = end_time - start_time  # Differenz berechnen
                        print(f"Laufzeit: {elapsed_time} Sekunden")
                        print('recognizer count: ', perfect_mock_recognizer.get_count())
                        amount_valid_shapes += get_amount_valid_shapes(expected_shapes)
                        amount_correctly_recognized_shapes += get_amount_correctly_recognized_shapes(grouped_traces['recognized shapes'], expected_shapes)
                        print(amount_correctly_recognized_shapes, ' / ', amount_valid_shapes, 'richtig erkannt')
                       
                       
        
                                                  

# get input from command line: --fa or --fc or both

if len(sys.argv) < 2:
    path = ["../../../datasets/FC_1.0", "../../../datasets/FA_1.1"] 
    evaluate_recognizer(path)
elif(sys.argv[1] == '--fa'):
    path = "../../../datasets/FA_1.1"
    # evaluate_recognizer(path, 'FA')
    evaluate_grouper(path, 'FA')
elif(sys.argv[1] == '--fc'):
    path = "../../../datasets/FC_1.0"
    evaluate_recognizer(path, 'FC')

    



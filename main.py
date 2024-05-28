import sys
from grouper import group
from optimized_grouper import group as group_optimized
from parsers import parse_ground_truth, parse_strokes_from_inkml_file, exclude_text_strokes
from recognizer.perfect_mock_recognizer import is_a_shape
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix

# get input from command line with the path to the inkml file

if len(sys.argv) == 2:
    path = sys.argv[1]
    test_file_without_text = exclude_text_strokes(path)
    expected_shapes:list[dict] = parse_ground_truth(test_file_without_text)
    strokes:list[dict] = parse_strokes_from_inkml_file(test_file_without_text)
    grouped_strokes:dict = group_optimized(strokes, is_a_shape, initialize_adjacency_matrix, expected_shapes)


   
    

    

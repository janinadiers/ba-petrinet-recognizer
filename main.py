import sys
from grouper import group
from optimized_grouper import group as group_optimized
from parsers import parse_ground_truth, parse_strokes_from_inkml_file, exclude_text_strokes
from recognizer.perfect_mock_recognizer import is_a_shape
from distance_calculators.distance_between_all_points import initialize_adjacency_matrix
from normalizer import normalize
from export_strokes_to_inkml import export_strokes_to_inkml

# get input from command line with the path to the inkml file

if len(sys.argv) == 2:
    path = sys.argv[1]
    test_file_without_text = exclude_text_strokes(path)
    expected_shapes:list[dict] = parse_ground_truth(test_file_without_text)
    strokes:list[dict] = parse_strokes_from_inkml_file(test_file_without_text)
    # zunächst möchte ich gerne die normalisierung testen und die normalisierten Striche in einem neuen inkml file speichern
    
    for i in range(len(strokes)):
        strokes[i] = normalize(strokes[i])
        
        # print('nachher: ',len(stroke))

    export_strokes_to_inkml(strokes, 'normalized_strokes.inkml')
    # export_points_to_inkml(normalized_strokes, 'normalized_strokes.inkml')
    # save the normalized strokes in a new inkml file
    
    # grouped_strokes:dict = group_optimized(strokes, is_a_shape, initialize_adjacency_matrix, expected_shapes)
    


   
    

    

import unittest
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance, initialize_adjacency_matrix_with_distance, get_max_dist, median
import numpy as np
from helper.parsers import parse_strokes_from_inkml_file
from helper.normalizer import resample_strokes


class TestDistanceBetweenAllPointsMethods(unittest.TestCase):

    def test_get_min_distance(self):
        stroke1 = [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]
        stroke2 = [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]
        stroke3 = [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]
        stroke4 = [{'x': 0, 'y': 4, 't': 0}, {'x': 3, 'y': 8, 't': 1}, {'x': 6, 'y': 12, 't': 2}]
        
        
        # float("{:.2f}".format to make sure the result has only 2 decimal places
        self.assertEqual( float("{:.2f}".format(get_min_distance(stroke1, stroke2))), 0)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke3, stroke4))), 7.21)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke1, stroke3))), 5.0)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke2, stroke4))), 2.83)
        
    def test_get_min_distance2(self):
        strokes = parse_strokes_from_inkml_file('./__datasets__/FC_1.0/no_text/no_junk/writer015_fc_012b.inkml')
        resampled_strokes = resample_strokes(strokes)
        stroke15 = resampled_strokes[15]
        stroke16 = resampled_strokes[16]
        stroke17 = resampled_strokes[17]
        distance1 = get_min_distance(stroke15, stroke16)
        distance2 = get_min_distance(stroke15, stroke17)
        distance3 = get_min_distance(stroke16, stroke17)
        print('distance1', distance1)
        print('distance2', distance2)
        print('distance3', distance3)
        

        
        
    def test_median(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(median(lst), 3)
        lst = [1, 2, 3, 4, 5, 6]
        self.assertEqual(median(lst), 3.5)
        
    
    def test_initialize_adjacency_matrix(self):
        strokes = [[{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}], 
                   [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}],
                   [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}],
                   [{'x': 3000, 'y': 4000, 't': 0}, {'x': 3400, 'y': 8000, 't': 1}, {'x': 6000, 'y': 1200, 't': 2}]]
        matrix = initialize_adjacency_matrix_with_distance(strokes)
        expected_matrix = np.zeros((4, 4), dtype=int)
        expected_matrix[0, 0] = 0
        expected_matrix[0, 1] = get_min_distance(strokes[0], strokes[1]) if get_min_distance(strokes[0], strokes[1]) <= 600 else 0
        expected_matrix[0, 2] = get_min_distance(strokes[0], strokes[2]) if get_min_distance(strokes[0], strokes[2]) <= 600 else 0
        expected_matrix[0, 3] = get_min_distance(strokes[0], strokes[3]) if get_min_distance(strokes[0], strokes[3]) <= 600 else 0
        expected_matrix[1, 0] = get_min_distance(strokes[1], strokes[0]) if get_min_distance(strokes[1], strokes[0]) <= 600 else 0
        expected_matrix[1, 1] = 0
        expected_matrix[1, 2] = get_min_distance(strokes[1], strokes[2]) if get_min_distance(strokes[1], strokes[2]) <= 600 else 0
        expected_matrix[1, 3] = get_min_distance(strokes[1], strokes[3]) if get_min_distance(strokes[1], strokes[3]) <= 600 else 0
        expected_matrix[2, 0] = get_min_distance(strokes[2], strokes[0]) if get_min_distance(strokes[2], strokes[0]) <= 600 else 0
        expected_matrix[2, 1] = get_min_distance(strokes[2], strokes[1]) if get_min_distance(strokes[2], strokes[1]) <= 600 else 0
        expected_matrix[2, 2] = 0
        expected_matrix[2, 3] = get_min_distance(strokes[2], strokes[3]) if get_min_distance(strokes[2], strokes[3]) <= 600 else 0
        expected_matrix[3, 0] = get_min_distance(strokes[3], strokes[0]) if get_min_distance(strokes[3], strokes[0]) <= 600 else 0
        expected_matrix[3, 1] = get_min_distance(strokes[3], strokes[1]) if get_min_distance(strokes[3], strokes[1]) <= 600 else 0
        expected_matrix[3, 2] = get_min_distance(strokes[3], strokes[2]) if get_min_distance(strokes[3], strokes[2]) <= 600 else 0
        expected_matrix[3, 3] = 0

        np.testing.assert_array_equal(expected_matrix, matrix)
    
        
    
   

if __name__ == '__main__':
    unittest.main()
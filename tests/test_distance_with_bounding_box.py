import unittest
from distance_calculators.distance_with_bounding_box import get_distance, get_bounding_box_center, initialize_adjacency_matrix
import numpy as np

class TestDistanceWithBoundingBoxMethods(unittest.TestCase):

    def test_distance(self):
        stroke1 = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}
        # bounding box center of stroke1 is (3, 4)
        stroke2 = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]}
        # bounding box center of stroke2 is (4, 5)
        stroke3 = {'1': [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]}
        # bounding box center of stroke3 is (13, 4)
        stroke4 = {'1': [{'x': 0, 'y': 4, 't': 0}, {'x': 3, 'y': 8, 't': 1}, {'x': 6, 'y': 12, 't': 2}]}
        # bounding box center of stroke4 is (3, 8)
        
        # float("{:.2f}".format to make sure the result has only 2 decimal places
        self.assertEqual( float("{:.2f}".format(get_distance(stroke1, stroke2))), 1.41)
        self.assertEqual(float("{:.2f}".format(get_distance(stroke3, stroke4))), 10.77)
    
    def test_get_bounding_box_center(self):
        stroke = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}
        self.assertEqual(get_bounding_box_center(stroke), (3, 4))
    
    def test_initialize_adjacency_matrix(self):
        strokes = [{'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}, 
                   {'2': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]},
                   {'3': [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]},
                   {'4': [{'x': 3000, 'y': 4000, 't': 0}, {'x': 3400, 'y': 8000, 't': 1}, {'x': 6000, 'y': 1200, 't': 2}]}]
        matrix = initialize_adjacency_matrix(strokes)
        expected_matrix = np.zeros((4, 4), dtype=int)
        expected_matrix[0, 0] = 0
        expected_matrix[0, 1] = 1
        expected_matrix[0, 2] = 1
        expected_matrix[0, 3] = 0
        expected_matrix[1, 0] = 0
        expected_matrix[1, 1] = 0
        expected_matrix[1, 2] = 1
        expected_matrix[1, 3] = 0
        expected_matrix[2, 0] = 0
        expected_matrix[2, 1] = 0
        expected_matrix[2, 2] = 0
        expected_matrix[2, 3] = 0
        expected_matrix[3, 0] = 0
        expected_matrix[3, 1] = 0
        expected_matrix[3, 2] = 0
        expected_matrix[3, 3] = 0

        np.testing.assert_array_equal(expected_matrix, matrix)
    
        
    
   

if __name__ == '__main__':
    unittest.main()
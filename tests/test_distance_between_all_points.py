import unittest
from distance_calculators.distance_between_all_points import get_min_distance, initialize_adjacency_matrix, get_max_dist, median, average_distance_between_all_neighbouring_strokes
import numpy as np
import math


class TestDistanceBetweenAllPointsMethods(unittest.TestCase):

    def test_get_min_distance(self):
        stroke1 = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}
        stroke2 = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]}
        stroke3 = {'1': [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]}
        stroke4 = {'1': [{'x': 0, 'y': 4, 't': 0}, {'x': 3, 'y': 8, 't': 1}, {'x': 6, 'y': 12, 't': 2}]}
        
        
        # float("{:.2f}".format to make sure the result has only 2 decimal places
        self.assertEqual( float("{:.2f}".format(get_min_distance(stroke1, stroke2))), 0)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke3, stroke4))), 7.21)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke1, stroke3))), 5.0)
        self.assertEqual(float("{:.2f}".format(get_min_distance(stroke2, stroke4))), 2.83)
        
    
    def test_median(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(median(lst), 3)
        lst = [1, 2, 3, 4, 5, 6]
        self.assertEqual(median(lst), 3.5)
        
    
    def test_get_max_dist(self):
        strokes = [{'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}, 
                   {'2': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]},
                   {'3': [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]},
                   {'4': [{'x': 0, 'y': 4, 't': 0}, {'x': 3, 'y': 8, 't': 1}, {'x': 6, 'y': 12, 't': 2}]}]
        boundingBox1 = {'width': 6, 'height': 8}
        boundingBox2 = {'width': 8, 'height': 10}
        boundingBox3 = {'width': 14, 'height': 8}
        boundingBox4 = {'width': 6, 'height': 8}
        diagonal1 = math.sqrt(boundingBox1['width']**2 + boundingBox1['height']**2)
        diagonal2 = math.sqrt(boundingBox2['width']**2 + boundingBox2['height']**2)
        diagonal3 = math.sqrt(boundingBox3['width']**2 + boundingBox3['height']**2)
        diagonal4 = math.sqrt(boundingBox4['width']**2 + boundingBox4['height']**2)
        median_diagonal = median([diagonal1, diagonal2, diagonal3, diagonal4])
        self.assertEqual(float("{:.2f}".format(get_max_dist(strokes))), float("{:.2f}".format(median_diagonal)))
    
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
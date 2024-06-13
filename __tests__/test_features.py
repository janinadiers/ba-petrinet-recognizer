import unittest
from helper.features import get_shape_no_shape_features, get_circle_rectangle_features
import math


class TestFeatureMethods(unittest.TestCase):

    def test_get_shape_no_shape_features(self):
        rect = [[{'x': 485, 'y': 223}, {'x': 484, 'y': 260}, {'x': 486, 'y': 287}, {'x': 522, 'y': 289}, {'x': 542, 'y': 273}, {'x': 543, 'y': 237}, {'x': 516, 'y': 226}, {'x': 487, 'y': 224}]]
        circle = [[{'x': 573, 'y': 224}, {'x': 536, 'y': 227}, {'x': 514, 'y': 254}, {'x': 535, 'y': 281}, {'x': 572, 'y': 279}, {'x': 593, 'y': 253}, {'x': 574, 'y': 226}, {'x': 567, 'y': 224}]]
        line = [[{'x': 329, 'y': 258}, {'x': 368, 'y': 258}, {'x': 407, 'y': 258}, {'x': 446, 'y': 258}, {'x': 485, 'y': 258}, {'x': 511, 'y': 258}]]
        # rect_convex_hull_perimeter_to_area_ratio = int(10/6)
        # rect_total_stroke_length_to_diagonal_length = int(10/math.sqrt(13))
        # circle_convex_hull_perimeter_to_area_ratio = int(2/circle_radius)
        # circle_total_stroke_length_to_diagonal_length = int(math.pi / math.sqrt(2))
        rect_features = get_shape_no_shape_features([0], rect)
        circle_features = get_shape_no_shape_features([0], circle)
        line_features = get_shape_no_shape_features([0], line)
        rect_features['features'] = [int(x) for x in rect_features['features']]
        circle_features['features'] = [int(x) for x in circle_features['features']]
        line_features['features'] = [int(x) for x in line_features['features']]
        print(rect_features['features'], circle_features['features'], line_features['features'])
        # self.assertEqual(rect_features['features'], [rect_convex_hull_perimeter_to_area_ratio, rect_total_stroke_length_to_diagonal_length])
        # self.assertEqual(circle_features['features'], [circle_convex_hull_perimeter_to_area_ratio, circle_total_stroke_length_to_diagonal_length])
        # self.assertTrue(rect_features['features'][0] < circle_features['features'][0])
       
    # def test_get_circle_rectangle_features(self):
    #     rect = [[{'x': 3, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4},{'x': 2, 'y': 4}, {'x': 3, 'y': 4}, {'x': 3, 'y': 3}, {'x': 3, 'y': 2}, {'x': 3, 'y': 1}]]
    #     circle = [[{'x': 5.0, 'y': 2.0},{'x': 4.618033988749895, 'y': 3.1755705045849463},{'x': 3.618033988749895, 'y': 3.9021130325903073},{'x': 2.381966011250105, 'y': 3.9021130325903073},{'x': 1.381966011250105, 'y': 3.1755705045849467},{'x': 1.0, 'y': 2.0},{'x': 1.381966011250105, 'y': 0.8244294954150534},{'x': 2.381966011250105, 'y': 0.09788696740969294},{'x': 3.6180339887498945, 'y': 0.09788696740969282},{'x': 4.618033988749895, 'y': 0.824429495415053}]]
    #     rect_amount_cluster = 4
    #     circle_amount_cluster = 0
    #     total_stroke_length_difference_to_total_stroke_length_of_circle = 0
    #     rect_features = get_circle_rectangle_features([0], rect)
    #     print('----------------------------')
    #     circle_features = get_circle_rectangle_features([0], circle)
    #     print(rect_features['features'], rect_features['features'])
        
       
if __name__ == '__main__':
    unittest.main()
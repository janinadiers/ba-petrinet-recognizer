import unittest
from helper.features import get_shape_no_shape_features, get_circle_rectangle_features
from helper.parsers import parse_strokes_from_inkml_file
from helper.normalizer import normalize_strokes, remove_junk_strokes
from helper.utils import combine_strokes
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length
class TestFeatureMethods(unittest.TestCase):

    def test_get_shape_no_shape_features(self):
        rect_file = './inkml_requests/rectangle.inkml'
        circle_file = './inkml_requests/circle.inkml'
        ellipse_file = './inkml_requests/ellipse.inkml'
        line_file = './inkml_requests/line.inkml'
        
        rect_strokes = parse_strokes_from_inkml_file(rect_file)
        rect_strokes = remove_junk_strokes(rect_strokes)
        rect_strokes = normalize_strokes(rect_strokes)
        rect_stroke = combine_strokes([0], rect_strokes)
        # visualize_points(rect_stroke)
               
        circle_strokes = parse_strokes_from_inkml_file(circle_file)
        circle_strokes = remove_junk_strokes(circle_strokes)
        circle_strokes = normalize_strokes(circle_strokes)
        circle_stroke = combine_strokes([0], circle_strokes)
        circle_bounding_box = get_bounding_box(circle_stroke)
        # visualize_points(circle_stroke)
        
        ellipse_strokes = parse_strokes_from_inkml_file(ellipse_file)
        ellipse_strokes = remove_junk_strokes(ellipse_strokes)
        ellipse_strokes = normalize_strokes(ellipse_strokes)
        ellipse_stroke = combine_strokes([0], ellipse_strokes)
        ellipse_bounding_box = get_bounding_box(ellipse_stroke)
        # visualize_points(ellipse_stroke)
        
        line_strokes = parse_strokes_from_inkml_file(line_file)
        line_strokes = remove_junk_strokes(line_strokes)
        line_strokes = normalize_strokes(line_strokes)
        line_stroke = combine_strokes([0,1], line_strokes)
        line_bounding_box = get_bounding_box(line_stroke)
        # visualize_points(line_stroke)
        
        # Feature 0: Convex Hull Perimeter to Area Ratio, Feature 1: Total Stroke Length to Diagonal Length, Feature 2: aspect ratio, Feature 3: number_of_convex_hull_vertices, Feature 4: centroid_distance_variability
        rect_features = get_shape_no_shape_features([0], rect_strokes)
        circle_features = get_shape_no_shape_features([0], circle_strokes)
        ellipse_features = get_shape_no_shape_features([0], ellipse_strokes)
        line_features = get_shape_no_shape_features([0,1], line_strokes)
          
        print(rect_features['features'][0], circle_features['features'][0], ellipse_features['features'][0], line_features['features'][0])
        
        
       
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

# Visualisierung für manuelle Überprüfung (optional)
def visualize_points(points):
    coords = np.array([[p['x'], p['y']] for p in points])
    bounding_box = get_bounding_box(points)
    total_stroke_length = calculate_total_stroke_length(points)
    print('Total Stroke Length:', total_stroke_length)
    print('Bounding Box:', bounding_box)
    plt.plot(coords[:, 0], coords[:, 1], 'o')
    hull = ConvexHull(coords)
    # visualize convex hull
    for simplex in hull.simplices:
        plt.plot(coords[simplex, 0], coords[simplex, 1], 'k-')
    plt.show()
        
       
if __name__ == '__main__':
    unittest.main()
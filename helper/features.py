
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length
from helper.corner_detection import detect_corners
import numpy as np
import copy
from helper.utils import combine_strokes, get_perfect_mock_shape, order_strokes
from helper.export_strokes_to_inkml import export_strokes_to_inkml
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# compactness ratio: 
# Circles: For a perfect circle, the ratio of area to perimeter (compactness) is maximized, because circles have the highest area for a given perimeter compared to other shapes. This makes the compactness ratio close to that of a circle.
# Rectangles and Other Polygons: Shapes like rectangles, especially elongated ones, have a lower compactness ratio compared to circles. This is because they have more perimeter for the same area compared to a circle.
def compute_convex_hull_perimeter_to_area_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    if len(points) < 3:
        return 0  # Not enough points to form a convex hull

    hull = ConvexHull(_points)
    hull_area = hull.volume  # For 2D, volume is the area
    hull_perimeter = hull.area  # For 2D, area is the perimeter

    if hull_area == 0:
        return 0 

    return hull_perimeter / hull_area



def compute_convex_hull_area_to_perimeter_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    if len(_points) < 3:
        return 0  # Not enough points to form a convex hull

    hull = ConvexHull(_points)
    hull_area = hull.volume  # For 2D, volume is the area
    hull_perimeter = hull.area  # For 2D, area is the perimeter

    if hull_perimeter == 0:
        return 0 

    return hull_area / hull_perimeter


def compute_total_stroke_length_to_diagonal_length(stroke):
    _stroke = copy.deepcopy(stroke)
    return calculate_total_stroke_length(_stroke) / calculate_diagonal_length(get_bounding_box(_stroke))


def calculate_average_min_distance_to_template_shape(ideal_shape, candidate):
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_shape_arr = np.array([[point['x'], point['y']] for point in ideal_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in candidate])
    
    # Calculate pairwise distances between all points in ideal_shape and candidate
    # np.newaxis increases the dimension where applied, making the array broadcasting possible
    distances = np.sqrt(((ideal_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    # Find the minimum distance for each point in ideal_shape to any point in candidate
    min_distances = np.min(distances, axis=1)
    
    # Calculate the average of these minimum distances
    average_min_distance = np.mean(min_distances)
    
    # statt dem mean könnte ich auch mal IDM probieren
    
    return average_min_distance

def calculate_x_cluster_distribution(points):
    x_coords = [stroke['x'] for stroke in points] 
    sorted_x_coords = sorted(x_coords)
    max_x = max(sorted_x_coords)
    min_x = min(sorted_x_coords)
    number_of_x_values = len(sorted_x_coords)
    twenty_percent = int(number_of_x_values * 0.2)
    eighty_percent = int(number_of_x_values * 0.8)
    twenty_percent_x = sorted_x_coords[twenty_percent]
    eighty_percent_x = sorted_x_coords[eighty_percent]
    span = max_x - min_x
    if span == 0:
        return 1, 0
    span_traveled_twenty_percent = (twenty_percent_x - min_x) / span
    span_traveled_eighty_percent = (eighty_percent_x - min_x) / span
    return span_traveled_twenty_percent, span_traveled_eighty_percent

def calculate_y_cluster_distribution(points):
    y_coords = [stroke['y'] for stroke in points] 
    sorted_y_coords = sorted(y_coords)
    max_y = max(sorted_y_coords)
    min_y = min(sorted_y_coords)
    number_of_y_values = len(sorted_y_coords)
    twenty_percent = int(number_of_y_values * 0.2)
    eighty_percent = int(number_of_y_values * 0.8)
    twenty_percent_y = sorted_y_coords[twenty_percent]
    eighty_percent_y = sorted_y_coords[eighty_percent]
    span = max_y - min_y
    if span == 0:
        return 1, 0
    span_traveled_twenty_percent = (twenty_percent_y - min_y) / span
    span_traveled_eighty_percent = (eighty_percent_y - min_y) / span
    return span_traveled_twenty_percent, span_traveled_eighty_percent

        
def get_feature_vector(candidate:list[int], strokes:list[list[dict]])->list[int]:
    """ Extract feature vector from stroke """
    ordered_strokes = order_strokes(strokes)
    stroke = combine_strokes(candidate, ordered_strokes)
  
    x_cluster_twenty_percent = calculate_x_cluster_distribution(stroke)[0]
    x_cluster_eighty_percent = calculate_x_cluster_distribution(stroke)[1]
    y_cluster_twenty_percent = calculate_y_cluster_distribution(stroke)[0]
    y_cluster_eighty_percent = calculate_y_cluster_distribution(stroke)[1]
    amount_cluster = 0
    if x_cluster_twenty_percent < 0.1:
        amount_cluster+=1
    if x_cluster_eighty_percent > 0.9:
        amount_cluster+=1
    if y_cluster_twenty_percent < 0.1:
        amount_cluster+=1
    if y_cluster_eighty_percent > 0.9:
        amount_cluster+=1
    
 
    features = []
    try:
        convex_hull_perimeter_to_area_ratio = compute_convex_hull_perimeter_to_area_ratio(stroke)
        convex_hull_area_to_perimeter_ratio = compute_convex_hull_area_to_perimeter_ratio(stroke)
    except:
        convex_hull_perimeter_to_area_ratio = 0
        convex_hull_area_to_perimeter_ratio = 0
    # total_stroke_length_to_diagonal_length = compute_total_stroke_length_to_diagonal_length(stroke)

    perfect_mock_shape = get_perfect_mock_shape(stroke)
    average_distance_circle = calculate_average_min_distance_to_template_shape(perfect_mock_shape['circle'], stroke)
    average_distance_rect = calculate_average_min_distance_to_template_shape(perfect_mock_shape['rectangle'], stroke)
    # width_to_height_ratio = get_bounding_box(stroke)[4] / get_bounding_box(stroke)[5]
    # height_to_width_ratio = get_bounding_box(stroke)[5] / get_bounding_box(stroke)[4]
    
    

    # features.extend([convex_hull_area_to_perimeter_ratio, convex_hull_perimeter_to_area_ratio])
    features.extend([amount_cluster, average_distance_circle, average_distance_rect, convex_hull_area_to_perimeter_ratio, convex_hull_perimeter_to_area_ratio])
    return {'feature_names': ['amount_cluster', 'average_distance_circle', 'average_distance_rect', 'convex_hull_area_to_perimeter_ratio', 'convex_hull_perimeter_to_area_ratio'], 'features': features}
    

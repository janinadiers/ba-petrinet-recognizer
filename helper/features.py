
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length
import numpy as np
import copy
from helper.utils import combine_strokes, get_perfect_mock_shape, order_strokes



def total_stroke_length_of_circle(radius):
    return 2 * np.pi * radius
# compactness ratio: 
# Circles: For a perfect circle, the ratio of area to perimeter (compactness) is maximized, because circles have the highest area for a given perimeter compared to other shapes. This makes the compactness ratio close to that of a circle.
# Rectangles and Other Polygons: Shapes like rectangles, especially elongated ones, have a lower compactness ratio compared to circles. This is because they have more perimeter for the same area compared to a circle.
def compute_convex_hull_perimeter_to_area_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    try:
        hull = ConvexHull(_points)
        hull_area = hull.volume  # For 2D, volume is the area
        hull_perimeter = hull.area  # For 2D, area is the perimeter
        return hull_perimeter / hull_area
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
        
    
def compute_convex_hull_area_to_perimeter_ratio(points):
    print('compute_convex_hull_area_to_perimeter_ratio')
    _points = [(point['x'], point['y']) for point in points]
    
    try:
        hull = ConvexHull(_points)
        hull_area = hull.volume  # For 2D, volume is the area
        hull_perimeter = hull.area  # For 2D, area is the perimeter
        return hull_area / hull_perimeter
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
  

    
def compute_total_stroke_length_to_diagonal_length(stroke):
    _stroke = copy.deepcopy(stroke)
    diagonal_length = calculate_diagonal_length(get_bounding_box(_stroke))
    total_stroke_length = calculate_total_stroke_length(_stroke)
    
    return total_stroke_length / diagonal_length


def calculate_average_min_distance_to_template_shape(candidate):
    ideal_circle_shape = get_perfect_mock_shape(candidate)['circle']
    ideal_rect_shape = get_perfect_mock_shape(candidate)['rectangle']
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_circle_shape_arr = np.array([[point['x'], point['y']] for point in ideal_circle_shape])
    ideal_rect_shape_arr = np.array([[point['x'], point['y']] for point in ideal_rect_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in candidate])
    bounding_box = get_bounding_box(candidate)
    
    diagonal_of_bounding_box = calculate_diagonal_length(bounding_box)
    # Calculate pairwise distances between all points in ideal_shape and candidate
    # np.newaxis increases the dimension where applied, making the array broadcasting possible
    distances_to_ideal_circle_shape = np.sqrt(((ideal_circle_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    distances_to_ideal_rect_shape = np.sqrt(((ideal_rect_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    # Find the minimum distance for each point in ideal_shape to any point in candidate
    min_distances_to_ideal_circle_shape = np.min(distances_to_ideal_circle_shape, axis=1)
    min_distances_to_ideal_rect_shape = np.min(distances_to_ideal_rect_shape, axis=1)
   
    # Calculate the average of these minimum distances
    average_min_distance_ideal_circle = np.mean(min_distances_to_ideal_circle_shape)
    average_min_distance_ideal_rect = np.mean(min_distances_to_ideal_rect_shape)
   
    return average_min_distance_ideal_circle, average_min_distance_ideal_rect
   
   
def calculate_x_cluster_distribution(points):
    x_coords = [stroke['x'] for stroke in points] 
    sorted_x_coords = sorted(x_coords)
    max_x = max(sorted_x_coords)
    min_x = min(sorted_x_coords)
    number_of_x_values = len(sorted_x_coords)
    print('number_of_x_values', number_of_x_values)
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

def get_cluster_amount(stroke):
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
    return amount_cluster


def get_shape_no_shape_features(candidate, strokes):
    """ Extract feature vector from stroke """
    ordered_strokes = order_strokes(strokes)
    stroke = combine_strokes(candidate, ordered_strokes)
    print('stroke', stroke)
    try:
        convex_hull_perimeter_to_area_ratio = compute_convex_hull_perimeter_to_area_ratio(stroke)
        print('try', convex_hull_perimeter_to_area_ratio)
    except:
        print('except')
        convex_hull_perimeter_to_area_ratio = 0
        
    total_stroke_length_to_diagonal_length = compute_total_stroke_length_to_diagonal_length(stroke)

        
    return {'feature_names': ['convex_hull_perimeter_to_area_ratio', 'total_stroke_length_to_diagonal_length'], 'features': [convex_hull_perimeter_to_area_ratio, total_stroke_length_to_diagonal_length]}


def get_circle_rectangle_features(candidate, strokes):
    """ Extract feature vector from stroke """
    
    ordered_strokes = order_strokes(strokes)
    stroke = combine_strokes(candidate, ordered_strokes)
    print('stroke', stroke)
    amount_cluster = get_cluster_amount(stroke)
    total_stroke_length = calculate_total_stroke_length(stroke)
    radius = get_bounding_box(stroke)[4] / 2
    total_stroke_length_difference_to_total_stroke_length_of_circle = total_stroke_length_of_circle(radius) - total_stroke_length
    
    return {'feature_names': ['amount_cluster'], 'features': [amount_cluster]}


# def get_feature_vector(candidate:list[int], strokes:list[list[dict]])->list[int]:
#     """ Extract feature vector from stroke """
#     ordered_strokes = order_strokes(strokes)
#     stroke = combine_strokes(candidate, ordered_strokes)
    
#     # check if bounding box is zero
#     if get_bounding_box(stroke)[4] == 0 or get_bounding_box(stroke)[5] == 0:
#         return {'feature_names': ['amount_cluster', 'average_distance_circle', 'average_distance_rect', 'convex_hull_area_to_perimeter_ratio', 'convex_hull_perimeter_to_area_ratio'], 'features': [0, 0, 0, 0, 0]}
    
    
    
 
   
#     # total_stroke_length_to_diagonal_length = compute_total_stroke_length_to_diagonal_length(stroke)

    
#     average_distance_circle = calculate_average_min_distance_to_template_shape(stroke)[0]
#     average_distance_rect = calculate_average_min_distance_to_template_shape(stroke)[1]
#     # width_to_height_ratio = get_bounding_box(stroke)[4] / get_bounding_box(stroke)[5]
#     # height_to_width_ratio = get_bounding_box(stroke)[5] / get_bounding_box(stroke)[4]
    
#     amount_cluster = get_cluster_amount(stroke)

#     # features.extend([convex_hull_area_to_perimeter_ratio, convex_hull_perimeter_to_area_ratio])
#     features.extend([amount_cluster, average_distance_circle, average_distance_rect, convex_hull_area_to_perimeter_ratio, convex_hull_perimeter_to_area_ratio])
#     return {'feature_names': ['amount_cluster', 'average_distance_circle', 'average_distance_rect', 'convex_hull_area_to_perimeter_ratio', 'convex_hull_perimeter_to_area_ratio'], 'features': features}
    

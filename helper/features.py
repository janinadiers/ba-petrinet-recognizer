
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length
import numpy as np
import copy
from helper.utils import combine_strokes, get_perfect_mock_shape, order_strokes, distance
from shapely.geometry import Polygon, LineString
from scipy.spatial.distance import directed_hausdorff
from skimage.measure import EllipseModel



    
def get_hausdorff_distance(stroke):
    points = np.array([(point['x'], point['y']) for point in stroke])
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    d1 = directed_hausdorff(points, hull_points)[0]
    d2 = directed_hausdorff(hull_points, points)[0]
    return max(d1, d2)

def get_aspect_ratio(stroke):
    bounding_box = get_bounding_box(stroke)
    width = bounding_box[4]
    height = bounding_box[5]
    return width / height

def find_closest_point(points):
    # Initialize the minimum distance and closest point
    min_distance = float('inf')
    closest_point = None
    bounding_box = get_bounding_box(points)
    center = {'x': bounding_box[0] + bounding_box[4] / 2, 'y': bounding_box[2] + bounding_box[5] / 2}
    # Iterate over all points to find the closest one
    for point in points:
        eucl_distance = distance(point, center)
        if eucl_distance < min_distance:
            min_distance = eucl_distance
            closest_point = point
    return min_distance

def get_bounding_box_perimeter_to_total_stroke_length_ratio(stroke):
    bounding_box = get_bounding_box(stroke)
    width = bounding_box[4]
    height = bounding_box[5]
    bounding_box_perimeter = 2 * width + 2 * height
    total_stroke_length = calculate_total_stroke_length(stroke)
    return bounding_box_perimeter / total_stroke_length
    

def calculate_solidity(stroke):
    # Flatten the list of strokes into a list of points
    points = np.array([(point['x'], point['y']) for point in stroke])
    
    # Create a Polygon from the points
    polygon = Polygon(points)
    
    # Calculate the area of the shape
    shape_area = polygon.area
    
    # Compute the convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    
    # Create a Polygon from the hull points
    hull_polygon = Polygon(hull_points)
    
    # Calculate the area of the convex hull
    hull_area = hull_polygon.area
    
    # Calculate solidity
    solidity = shape_area / hull_area if hull_area != 0 else 0
    return solidity

def get_number_of_convex_hull_vertices(stroke):
    _stroke = copy.deepcopy(stroke)
    points = [(point['x'], point['y']) for point in _stroke]
    try:
        hull = ConvexHull(points)
        return len(hull.vertices)
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
    
def get_circularity(stroke):
    
    _points = [(point['x'], point['y']) for point in stroke]
    # Create a Polygon from the points
    polygon = Polygon(_points)

    # Calculate area and perimeter
    area = polygon.area
    perimeter = polygon.length

    # Calculate circularity
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    return circularity

def get_convexity(strokes):
    # Flatten the list of strokes into a list of points
    points = np.array([(point['x'], point['y']) for stroke in strokes for point in stroke])
    
    # Create a LineString from the points to calculate the perimeter
    linestring = LineString(points)
    shape_perimeter = linestring.length
    
    # Compute the convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    
    # Create a Polygon from the hull points to calculate the convex hull perimeter
    hull_polygon = Polygon(hull_points)
    hull_perimeter = hull_polygon.length
    
    # Calculate convexity
    convexity = hull_perimeter / shape_perimeter
    
    return convexity

def compute_convex_hull(points):
    hull = ConvexHull(points)
    return hull

def calculate_concavity(stroke):
    points = np.array([(point['x'], point['y']) for point in stroke])
    polygon = Polygon(points)
    hull = compute_convex_hull(points)
    hull_polygon = Polygon(points[hull.vertices])
    
    shape_area = polygon.area
    hull_area = hull_polygon.area
    
    concavity_area = hull_area - shape_area
    concavity_index = concavity_area / hull_area if hull_area != 0 else 0
    
    return concavity_index

    
def get_centroid_distance_variability(points):
    _points = [(point['x'], point['y']) for point in points]
    try:
        hull = ConvexHull(_points)
        hull_points = hull.points[hull.vertices]
        centroid = np.mean(hull_points, axis=0)
        distances = []
        for point in hull_points:
            distances.append(distance({'x': centroid[0], 'y': centroid[1]}, {'x': point[0], 'y': point[1]}))

        return np.var(distances)
    except Exception as e:
        raise Exception("Convex hull could not be computed.")

def is_closed_shape(strokes):
    _strokes = copy.deepcopy(strokes)
    edge_points = []
    for stroke in _strokes:
        edge_points.append(stroke[0])
        edge_points.append(stroke[-1])
    min_distances = []
    for point1 in edge_points:
        distances = []
        for point2 in edge_points:
            if point1 == point2:
                continue
            distances.append(distance(point1, point2))
        min_distances.append(min(distances))
        
    # return np.mean(min_distances)
    return max(min_distances)

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

def stroke_has_only_duplicates(stroke):
    for i in range(len(stroke) - 1):
        if stroke[i] != stroke[i + 1]:
            return False
    return True

def get_strokes_from_candidate(candidate, strokes):
    _strokes = []
    for index in candidate:
        _strokes.append(strokes[index])
    return _strokes

def get_shape_no_shape_features(candidate, strokes):
    """ Extract feature vector from stroke """
    stroke = combine_strokes(candidate, strokes)
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    bounding_box = get_bounding_box(stroke)
    if (len(stroke) < 5 or has_only_duplicates or bounding_box[4] < 1 or bounding_box[5] < 1):
        print('returning')
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    
    convex_hull_perimeter_to_area_ratio = compute_convex_hull_perimeter_to_area_ratio(stroke)
    total_stroke_length_to_diagonal_length = compute_total_stroke_length_to_diagonal_length(stroke)
    aspect_ratio = get_aspect_ratio(stroke)
    number_of_convex_hull_vertices = get_number_of_convex_hull_vertices(stroke)
    centroid_distance_variability = get_centroid_distance_variability(stroke)
    average_min_distance_ideal_circle, average_min_distance_ideal_rect = calculate_average_min_distance_to_template_shape(stroke)
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    # print('strokes_of_candidate', strokes_of_candidate)
    closed_shape = is_closed_shape(strokes_of_candidate)
    # circularity = get_circularity(strokes_of_candidate)
    convexity = get_convexity(strokes_of_candidate)
    concavity = calculate_concavity(stroke)
    aspect_ratio = get_aspect_ratio(stroke)
    bounding_box_perimeter_to_total_stroke_length = get_bounding_box_perimeter_to_total_stroke_length_ratio(stroke)
    closest_point_from_center = find_closest_point(stroke)
    solidity = calculate_solidity(stroke)
    hausdorff_distance = get_hausdorff_distance(stroke)
 
    # ordered_strokes = order_strokes(strokes_of_candidate)
    # ordered_and_combined_strokes = []
    # for stroke in ordered_strokes:
    #     ordered_and_combined_strokes.extend(stroke)
    # distance_between_start_and_end_point = get_start_and_end_point_distance(ordered_and_combined_strokes)
    return {'feature_names': ['closed_shape'], 'features': [closed_shape]}
   


def get_circle_rectangle_features(candidate, strokes):
    """ Extract feature vector from stroke """
    
    ordered_strokes = order_strokes(strokes)
    stroke = combine_strokes(candidate, ordered_strokes)
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    if (len(stroke) < 5 or has_only_duplicates):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    amount_cluster = get_cluster_amount(stroke)
    total_stroke_length = calculate_total_stroke_length(stroke)
    radius = get_bounding_box(stroke)[4] / 2
    total_stroke_length_difference_to_total_stroke_length_of_circle = total_stroke_length_of_circle(radius) - total_stroke_length
    number_of_convex_hull_vertices = get_number_of_convex_hull_vertices(stroke)
    centroid_distance_variability = get_centroid_distance_variability(stroke)
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
   
    circularity = get_circularity(stroke)
    return {'feature_names': ['number_of_convex_hull_vertices', 'amount_cluster'], 'features': [number_of_convex_hull_vertices, amount_cluster]}


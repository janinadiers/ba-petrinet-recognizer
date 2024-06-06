
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length
import numpy as np
# compactness ratio: 
# Circles: For a perfect circle, the ratio of area to perimeter (compactness) is maximized, because circles have the highest area for a given perimeter compared to other shapes. This makes the compactness ratio close to that of a circle.
# Rectangles and Other Polygons: Shapes like rectangles, especially elongated ones, have a lower compactness ratio compared to circles. This is because they have more perimeter for the same area compared to a circle.
def compute_convex_hull_perimeter_to_area_ratio(points):
    points = [(point['x'], point['y']) for point in points]
    if len(points) < 3:
        return 0  # Not enough points to form a convex hull

    hull = ConvexHull(points)
    hull_area = hull.volume  # For 2D, volume is the area
    hull_perimeter = hull.area  # For 2D, area is the perimeter

    if hull_area == 0:
        return 0 

    return hull_perimeter / hull_area



def compute_convex_hull_area_to_perimeter_ratio(points):
    points = [(point['x'], point['y']) for point in points]
    if len(points) < 3:
        return 0  # Not enough points to form a convex hull

    hull = ConvexHull(points)
    hull_area = hull.volume  # For 2D, volume is the area
    hull_perimeter = hull.area  # For 2D, area is the perimeter

    if hull_perimeter == 0:
        return 0 

    return hull_area / hull_perimeter


def compute_total_stroke_length_to_diagonal_length(stroke):
    return calculate_total_stroke_length(stroke) / calculate_diagonal_length(get_bounding_box(stroke))


def get_stroke_amount(strokes):
    return len(strokes)

def get_points_amount(strokes):
    return sum([len(stroke) for stroke in strokes])

def calculate_average_min_distance(ideal_shape, candidate):
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
    
    return average_min_distance
    

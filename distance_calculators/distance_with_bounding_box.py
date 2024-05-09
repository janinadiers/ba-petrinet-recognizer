import math
import numpy as np



def get_bounding_box_center(stroke: dict) -> tuple:
    points:list = []
    for key, val in stroke.items():
        points = val
    min_x:int = min(int(point['x']) for point in points)
    max_x:int = max(int(point['x']) for point in points)
    min_y:int = min(int(point['y']) for point in points)
    max_y:int = max(int(point['y']) for point in points)
    center_point:tuple = (min_x + max_x) / 2, (min_y + max_y) / 2
    return center_point


def get_distance(stroke1:dict, stroke2:dict) -> float:
    """Calculate the distance between two strokes based on their bounding box centers."""
    center1:tuple = get_bounding_box_center(stroke1)
    center2:tuple = get_bounding_box_center(stroke2)
    return math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
def initialize_adjacency_matrix(strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_strokes:int = len(strokes)
    matrix:np.ndarray = np.zeros((num_strokes, num_strokes), dtype=object)
    MAX_DIST:int=2306
    # Iterate over all pairs of strokes and determine if they are neighbors
    for i in range(num_strokes):
        for j in range(i + 1, num_strokes):
            distance:float = get_distance(strokes[i], strokes[j])
            # If distance is less than or equal to threshold, mark them as neighbors
            if distance <= MAX_DIST:
                matrix[i, j] = (1, round(distance))   
    return matrix
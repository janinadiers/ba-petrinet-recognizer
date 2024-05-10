import math
import numpy as np

def get_average_point(normalized_stroke: dict) -> tuple:
    points:list = []
    for key, val in normalized_stroke.items():
        points = val
    return (average(list(int(point['x']) for point in points)), average(list(int(point['y']) for point in points)))
   

def average(lst:list[int]): 
    return sum(lst) / len(lst) 

def get_distance(normalized_stroke1:dict, normalized_stroke2:dict) -> float:
    """Calculate the distance between two strokes based on their average points."""
    average_x:tuple = get_average_point(normalized_stroke1)
    average_y:tuple = get_average_point(normalized_stroke2)
    return math.sqrt((average_x[0] - average_y[0])**2 + (average_x[1] - average_y[1])**2)


def initialize_adjacency_matrix(normalized_strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_normalized_strokes:int = len(normalized_strokes)
    matrix:np.ndarray = np.zeros((num_normalized_strokes, num_normalized_strokes), dtype=int)
    MAX_DIST:int=2238
    # Iterate over all pairs of normalized_strokes and determine if they are neighbors
    for i in range(num_normalized_strokes):
        for j in range(i + 1, num_normalized_strokes):
            distance:float = get_distance(normalized_strokes[i], normalized_strokes[j])
            # If distance is less than or equal to threshold, mark them as neighbors
            if distance <= MAX_DIST:
                matrix[i, j] = 1
        
    return matrix
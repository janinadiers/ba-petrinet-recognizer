import math
import numpy as np
  
    
def get_min_distance(stroke1:dict, stroke2:dict) -> float:
    """Calculate the minimum Euclidean distance between all point pairs of two strokes."""
    min_distance:float = float('inf')
    points_stroke1:list[dict] = next(iter(stroke1.values()))
    points_stroke2:list[dict] = next(iter(stroke2.values()))
    
    for point1 in points_stroke1:
        for point2 in points_stroke2:
            distance:float = euclidean_distance(point1, point2)
            if distance < min_distance:
                min_distance = distance
    return min_distance

def euclidean_distance(point1: dict, point2:dict) -> float:
    
    """Calculate the Euclidean distance between two points."""
    point1X:int = int(point1['x'])
    point1Y:int = int(point1['y'])
    point2X:int = int(point2['x'])
    point2Y:int = int(point2['y'])
    return math.sqrt((point1X - point2X)**2 + (point1Y - point2Y)**2)
    
    
def initialize_adjacency_matrix(strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_strokes:int = len(strokes)
    matrix:np.ndarray = np.zeros((num_strokes, num_strokes), dtype=int)
    MAX_DIST:int=300
    # Iterate over all pairs of strokes and determine if they are neighbors
    for i in range(num_strokes):
        for j in range(i + 1, num_strokes):
            distance:float = get_min_distance(strokes[i], strokes[j])
            # If distance is less than or equal to threshold, mark them as neighbors
            if distance <= MAX_DIST:
                matrix[i, j] = 1
        
    return matrix
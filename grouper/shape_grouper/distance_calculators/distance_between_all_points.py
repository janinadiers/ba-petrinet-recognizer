import math
import numpy as np
import numpy as np
from scipy.spatial import distance

def convert_dict_to_nparray(points):
    return np.array([[point['x'], point['y']] for point in points])

    
def get_min_distance(stroke1:dict, stroke2:dict) -> float:
#     
    """Calculate the minimum Euclidean distance between all point pairs of two strokes."""
    # min_distance:float = float('inf')
    # points_stroke1:list[dict] = next(iter(stroke1.values()))
    # points_stroke2:list[dict] = next(iter(stroke2.values()))
    s1 = convert_dict_to_nparray(stroke1)
    s2 = convert_dict_to_nparray(stroke2)
    
    return distance.cdist(s1,s2).min(axis=1).min()

def euclidean_distance(point1: dict, point2:dict) -> float:
    
    """Calculate the Euclidean distance between two points."""
    point1X:int = int(point1['x'])
    point1Y:int = int(point1['y'])
    point2X:int = int(point2['x'])
    point2Y:int = int(point2['y'])
    return math.sqrt((point1X - point2X)**2 + (point1Y - point2Y)**2)

def median(lst:list[int]):
    lst.sort()
    n = len(lst)
    if n % 2 == 0:
        return (lst[n//2 - 1] + lst[n//2]) / 2
    return lst[n//2]

def get_max_dist(normalized_strokes:dict) -> float:
    '''Returns the median of the length of bounding box diagonals of all strokes'''
    diagonals = []
    # print('normalized_strokes', normalized_strokes)
    for stroke in normalized_strokes:
        points = next(iter(stroke.values()))
        x = [point['x'] for point in points]
        y = [point['y'] for point in points]
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        # Der Satz des Pythagoras wird verwendet, um die Länge der Diagonalen zu berechnen
        diagonals.append(math.sqrt((xmax - xmin)**2 + (ymax - ymin)**2))
    return median(diagonals)
    
    
def initialize_adjacency_matrix_with_distance(strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_strokes:int = len(strokes)
    matrix:np.ndarray = np.zeros((num_strokes, num_strokes), dtype=float)
    max_dist:int= 800
    # Iterate over all pairs of strokes and determine if they are neighbors
    for i in range(num_strokes):
        for j in range(i + 1, num_strokes):
            
            distance:float = get_min_distance(strokes[i], strokes[j])
            # If distance is less than or equal to threshold, mark them as neighbors
            if distance <= max_dist:
                matrix[i, j] = distance
                matrix[j, i] = distance
                
    return matrix


def initialize_adjacency_matrix(strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_strokes:int = len(strokes)
    matrix:np.ndarray = np.zeros((num_strokes, num_strokes), dtype=float)
    # 800 scheint eine gute Größe zwischen Accuracy und erzeugten Kandidaten zu sein
    max_dist:int= 800
    # Iterate over all pairs of strokes and determine if they are neighbors
    for i in range(num_strokes):
        matrix[i, i] = 1
        for j in range(i + 1, num_strokes):
            
            distance:float = get_min_distance(strokes[i], strokes[j])
            # If distance is less than or equal to threshold, mark them as neighbors
            if distance <= max_dist:
                matrix[i, j] = 1
                matrix[j, i] = 1
                
    return matrix
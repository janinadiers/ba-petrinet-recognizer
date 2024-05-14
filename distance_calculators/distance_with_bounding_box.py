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
        diagonals.append(math.sqrt((xmax - xmin)**2 + (ymax - ymin)**2))
    return median(diagonals)
        
def initialize_adjacency_matrix(strokes:list[dict]) -> np.ndarray:
    """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
    num_strokes:int = len(strokes)
    matrix:np.ndarray = np.zeros((num_strokes, num_strokes), dtype=int)
    max_dist:int= get_max_dist(strokes) * 0.35
    # Iterate over all pairs of strokes and determine if they are neighbors
    for i in range(num_strokes):
        for j in range(i + 1, num_strokes):
            distance:float = get_distance(strokes[i], strokes[j])
            if distance <= max_dist:
                matrix[i, j] = 1
        
    return matrix
import numpy as np
from grouper.shape_grouper.optimized_grouper import group



def group(shapes:list, unrecognized_strokes) -> list[dict]:
    edge_candidates = group(unrecognized_strokes)
    
    for candidate in edge_candidates:
        first_stroke = shapes[candidate[0]]
        last_stroke = shapes[candidate[-1]]
        # check if the first stroke is near a shape
        # check if the last stroke is near a shape
        # set candidate as potential edge and calculate bounding box at the start and end of the edge
        # to determine the direction of the edge
    
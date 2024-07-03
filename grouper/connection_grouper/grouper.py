import numpy as np
from grouper.shape_grouper.optimized_grouper import group
from helper.utils import distance
import copy
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance


def stroke_is_near_shape(stroke, shapes) -> bool:
    max_dist = 800
    for shape in shapes:
        for shape_stroke in shape:
            if get_min_distance([stroke[0]], shape_stroke) < max_dist or get_min_distance([stroke[-1]], shape_stroke) < max_dist:
                return True, shape
    return False, shape

def get_connected_shape(stroke, shapes) -> dict:
    for shape in shapes:
        if stroke_is_near_shape(stroke, shape):
            return shape
        
def find_nearest_neighbouring_stroke(last_stroke, unrecognized_strokes) -> list[dict]:
    strokes_with_distances =[]
    stroke_with_minimum_distance = None
    for stroke in unrecognized_strokes:
        if distance(last_stroke[-1], stroke[0]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[0])})
        if distance(last_stroke[-1], stroke[-1]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[-1])})
    # find stroke with minimum distance
    for stroke_with_distance in strokes_with_distances:
        if stroke_with_minimum_distance == None:
            stroke_with_minimum_distance = stroke_with_distance
        elif stroke_with_distance['distance'] < stroke_with_minimum_distance['distance']:
            stroke_with_minimum_distance = stroke_with_distance
    
    return stroke_with_minimum_distance['stroke']
    
        
def unrecognized_stroke_in_bounding_box(unrecognized_strokes, bounding_box) -> bool:
    # check if the stroke is in the bounding box
    # return True if it is in the bounding box, False otherwise
    for stroke in unrecognized_strokes:
        if bounding_box['x'] < stroke['x'] < bounding_box['x'] + bounding_box['width'] and bounding_box['y'] < stroke['y'] < bounding_box['y'] + bounding_box['height']:
            return True
    
def create_edge(line_strokes) -> dict:
    # find direction and create edge
    center1 = line_strokes[0][0]
    center2 = line_strokes[-1][-1]
    bounding_box_1 = {'x': center1['x'] -25, 'y': center1['y'] -25, 'width': 50, 'height': 50}
    bounding_box_2 = {'x': center2['x'] -25, 'y': center2['y'] -25, 'width': 50, 'height': 50}
    if unrecognized_stroke_in_bounding_box(line_strokes, bounding_box_1):
        return {'valid': {'line': line_strokes, 'arrow head': center1}}
    elif unrecognized_stroke_in_bounding_box(line_strokes, bounding_box_2):
        return {'valid': {'line': line_strokes, 'arrow head': center2}}

def group(shapes:list, unrecognized_strokes) -> list[dict]:
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)
    new_edge = [_unrecognized_strokes[0]]
    counter = 0
    while len(_unrecognized_strokes) > 0 and counter < len(_unrecognized_strokes) - 1:
        
        first_stroke_is_near_shape, shape1 = stroke_is_near_shape(new_edge[0], shapes)
        last_stroke_is_near_shape, shape2 = stroke_is_near_shape(new_edge[-1], shapes)
        
        if (first_stroke_is_near_shape and last_stroke_is_near_shape) and (shape1 != shape2):
            edge = create_edge(new_edge)
            valid_edges.append(edge)
            for stroke in new_edge:
                _unrecognized_strokes.remove(stroke)
            new_edge.append(_unrecognized_strokes[0])
        elif first_stroke_is_near_shape:
           nearest_neighbour = find_nearest_neighbouring_stroke(new_edge[-1], _unrecognized_strokes)
           new_edge.append(nearest_neighbour)

        else:
            counter += 1
            new_edge = [_unrecognized_strokes[counter]]
            
    return valid_edges
               
                
            
    
import numpy as np
from grouper.shape_grouper.optimized_grouper import group
from helper.utils import distance
import copy
from helper.utils import plot_strokes_without_scala
from helper.normalizer import scale, translate_to_origin
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance2


def stroke_is_near_shape(stroke, shapes) -> bool:
    max_dist = 800
    shape = None
    shape_strokes = []
    strokes_for_plotting = [stroke]
    for shape in shapes:
        shape_name = next(iter(shape))
        shape_strokes.extend([shape_stroke for shape_stroke in shape[shape_name]])
        strokes_for_plotting.extend(shape_strokes)
        # plot_strokes_without_scala(strokes_for_plotting) 
        for shape_stroke in shape[shape_name]:
            min_distance1, closest_point1 = get_min_distance2([stroke[0]], shape_stroke)
            min_distance2, closest_point2 = get_min_distance2([stroke[-1]], shape_stroke)
        
            if min_distance1 < max_dist:
                return True, shape, closest_point1
            if min_distance2 < max_dist:
                return True, shape, closest_point2
         
                 

    return False, shape, None
        
def find_nearest_neighbouring_stroke(last_stroke, unrecognized_strokes, shapes) -> list[dict]:
    strokes_with_distances =[]
    stroke_with_minimum_distance = None
    for stroke in unrecognized_strokes:
      
        if stroke == last_stroke:
            continue
        
        shape_strokes = []
        strokes_for_plotting = [last_stroke]
        for shape in shapes:
            shape_name = next(iter(shape))
            shape_strokes.extend([shape_stroke for shape_stroke in shape[shape_name]])
            strokes_for_plotting.extend(shape_strokes)
        # plot_strokes_without_scala(strokes_for_plotting, stroke)
        
        if distance(last_stroke[-1], stroke[0]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[0])})
        if distance(last_stroke[-1], stroke[-1]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[-1])})
        if distance(last_stroke[0], stroke[0]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[0], stroke[0])})
        if distance(last_stroke[0], stroke[-1]) < 800:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[0], stroke[-1])})
    # find stroke with minimum distance
    # print('strokes_with_distances', strokes_with_distances)
    for stroke_with_distance in strokes_with_distances:
        if stroke_with_minimum_distance == None:
            stroke_with_minimum_distance = stroke_with_distance
        elif stroke_with_distance['distance'] < stroke_with_minimum_distance['distance']:
            stroke_with_minimum_distance = stroke_with_distance
   
    return stroke_with_minimum_distance['stroke']
    
        
def unrecognized_stroke_in_bounding_box(unrecognized_stroke, bounding_box) -> bool:
    # check if the stroke is in the bounding box
    # return True if it is in the bounding box, False otherwise
    
    for point in unrecognized_stroke:
        if bounding_box['x'] < point['x'] < bounding_box['x'] + bounding_box['width'] and bounding_box['y'] < point['y'] < bounding_box['y'] + bounding_box['height']:
            return True
        
def get_amount_of_points_in_bounding_box(stroke, bounding_box) -> int:
    # return the amount of points in the bounding box
    amount_of_points = 0
    for point in stroke:
        if bounding_box['x'] < point['x'] < bounding_box['x'] + bounding_box['width'] and bounding_box['y'] < point['y'] < bounding_box['y'] + bounding_box['height']:
            amount_of_points += 1
    return amount_of_points
    
def create_edge(line_strokes, closest_point1, closest_point2, shape1, shape2, unrecognized_strokes) -> dict:
    # find direction and create edge
    _line_strokes = copy.deepcopy(line_strokes)
    strokes_to_plot = copy.deepcopy(line_strokes)
    shape_strokes1 = []
    shape_strokes2 = []
    shape_name1 = next(iter(shape1))
    shape_strokes1.extend([shape_stroke for shape_stroke in shape1[shape_name1]])
    
    shape_name2 = next(iter(shape2))
    shape_strokes2.extend([shape_stroke for shape_stroke in shape2[shape_name2]])
    
    strokes_to_plot.extend(shape_strokes1)
    strokes_to_plot.extend(shape_strokes2)
    
    closest_point1 = {'x': closest_point1[0], 'y': closest_point1[1]}
    closest_point2 = {'x': closest_point2[0], 'y': closest_point2[1]}
   
    bounding_box_1 = {'x': closest_point1['x'] -600, 'y': closest_point1['y'] -600, 'width': 1200, 'height': 1200}
    bounding_box_2 = {'x': closest_point2['x'] -600, 'y': closest_point2['y'] -600, 'width': 1200, 'height': 1200}
    # plot_strokes_without_scala(strokes_to_plot, [closest_point1, closest_point2, {'x': bounding_box_1['x'], 'y': bounding_box_1['y']},{'x': bounding_box_1['x'] + bounding_box_1['width'], 'y': bounding_box_1['y'] + bounding_box_1['height']},{'x': bounding_box_1['x'] + bounding_box_1['width'], 'y': bounding_box_1['y']}, {'x': bounding_box_1['x'], 'y': bounding_box_1['y'] + bounding_box_1['height']}, {'x': bounding_box_2['x'], 'y': bounding_box_2['y']},{'x': bounding_box_2['x'] + bounding_box_2['width'], 'y': bounding_box_2['y'] + bounding_box_2['height']},{'x': bounding_box_2['x'] + bounding_box_2['width'], 'y': bounding_box_2['y']}, {'x': bounding_box_2['x'], 'y': bounding_box_2['y'] + bounding_box_2['height']}])
    density1 = 0
    density2 = 0
    for stroke in unrecognized_strokes:
        if unrecognized_stroke_in_bounding_box(stroke, bounding_box_1):
            density1 += get_amount_of_points_in_bounding_box(stroke, bounding_box_1)
        if unrecognized_stroke_in_bounding_box(stroke, bounding_box_2):
            density2 += get_amount_of_points_in_bounding_box(stroke, bounding_box_2)
    if density1 > density2:

        return {'valid': {'line': _line_strokes, 'arrow head': closest_point1}}
    else:

        return {'valid': {'line': _line_strokes, 'arrow head': closest_point2}}
   

def group(shapes:list, unrecognized_strokes) -> list[dict]:
    
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)
    new_edge = [_unrecognized_strokes[0]]
    counter = 0
    while len(_unrecognized_strokes) > 0 and counter < len(_unrecognized_strokes) - 1:
        first_stroke_is_near_shape, shape1, closest_point1 = stroke_is_near_shape(new_edge[0], shapes)
        # get shapes without shape1
        shapes_without_shape1 = [shape for shape in shapes if shape != shape1]
        last_stroke_is_near_shape, shape2, closest_point2 = stroke_is_near_shape(new_edge[-1], shapes_without_shape1)
        if (first_stroke_is_near_shape and last_stroke_is_near_shape) and (shape1 != shape2):
            edge = create_edge(new_edge, closest_point1, closest_point2, shape1, shape2, _unrecognized_strokes)
            valid_edges.append(edge)
            for stroke in new_edge:
                _unrecognized_strokes.remove(stroke)
                
            if len(_unrecognized_strokes) > 0:
                new_edge = [_unrecognized_strokes[0]]
                
        elif first_stroke_is_near_shape:
            nearest_neighbour = find_nearest_neighbouring_stroke(new_edge[-1], _unrecognized_strokes, shapes)
            new_edge.extend(nearest_neighbour)

        else:
            counter += 1
            new_edge = [_unrecognized_strokes[counter]]
            
    return valid_edges
               
                
            
    
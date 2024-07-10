import numpy as np
from grouper.shape_grouper.optimized_grouper import group
from helper.utils import distance
import copy
from helper.utils import plot_strokes_without_scala
from helper.normalizer import scale, translate_to_origin
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance2


def get_closest_point(stroke, shape_strokes) -> dict:
    min_distance = None
    closest_point = None
    for shape_stroke in shape_strokes:
        for point in shape_stroke:
            for stroke_point in stroke:
                if min_distance == None:
                    min_distance = distance(point, stroke_point)
                    closest_point = [point['x'], point['y']]
                elif distance(point, stroke_point) < min_distance:
                    min_distance = distance(point, stroke_point)
                    closest_point = [point['x'], point['y']]
    return closest_point

def stroke_is_near_shape(stroke, shapes) -> bool:
    # max_dist = 800
    max_dist = 1000
    shape = None
   
    for shape in shapes:
        # plot_strokes_without_scala(shape['shape_strokes'], stroke) 
        # min_distances = []
        for shape_stroke in shape['shape_strokes']:
            # print('stroke', stroke)
            min_distance1, closest_point1 = get_min_distance2([stroke[0]], shape_stroke)
            min_distance2, closest_point2 = get_min_distance2([stroke[-1]],shape_stroke)
            if min_distance1 < max_dist:
                return True, shape, closest_point1
            if min_distance2 < max_dist:
                return True, shape, closest_point2
    return False, shape, None
        
def find_nearest_neighbouring_stroke(last_stroke, unrecognized_strokes, shapes, new_edge) -> list[dict]:
    strokes_with_distances =[]
    stroke_with_minimum_distance = None
    # max_dist = 800
    max_dist = 1000
    for stroke in unrecognized_strokes:
        if stroke in new_edge:
            continue
        
        strokes_for_plotting = [last_stroke]
        for shape in shapes:
            strokes_for_plotting.extend(shape['shape_strokes'])
       
        print(distance(last_stroke[-1], stroke[0]), distance(last_stroke[-1], stroke[-1]), distance(last_stroke[0], stroke[0]), distance(last_stroke[0], stroke[-1]))
        
        if distance(last_stroke[-1], stroke[0]) < max_dist:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[0])})
        if distance(last_stroke[-1], stroke[-1]) < max_dist:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[-1], stroke[-1])})
        if distance(last_stroke[0], stroke[0]) < max_dist:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[0], stroke[0])})
        if distance(last_stroke[0], stroke[-1]) < max_dist:
            strokes_with_distances.append({'stroke': stroke, 'distance': distance(last_stroke[0], stroke[-1])})
    # find stroke with minimum distance
    for stroke_with_distance in strokes_with_distances:
        if stroke_with_minimum_distance == None:
            stroke_with_minimum_distance = stroke_with_distance
        elif stroke_with_distance['distance'] < stroke_with_minimum_distance['distance']:
            stroke_with_minimum_distance = stroke_with_distance
   
    if stroke_with_minimum_distance != None:
        return stroke_with_minimum_distance['stroke']
    return None
    
        
def unrecognized_stroke_in_bounding_box(unrecognized_stroke, bounding_box) -> bool:
    # check if the stroke is in the bounding box
    # return True if it is in the bounding box, False otherwise
    
    for point in unrecognized_stroke:
        if bounding_box['x'] < point['x'] < bounding_box['x'] + bounding_box['width'] and bounding_box['y'] < point['y'] < bounding_box['y'] + bounding_box['height']:
            return True, unrecognized_stroke
        
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
    
    # bounding_box_width = 1200
    # bounding_box_height = 1200
    bounding_box_width = 2000
    bounding_box_height = 2000
   
    strokes_to_plot.extend(shape1['shape_strokes'])
    strokes_to_plot.extend(shape2['shape_strokes'])
    
    closest_point1 = {'x': closest_point1[0], 'y': closest_point1[1]}
    closest_point2 = {'x': closest_point2[0], 'y': closest_point2[1]}
#    600 vorher
    bounding_box_1 = {'x': closest_point1['x'], 'y': closest_point1['y'], 'width': bounding_box_width, 'height': bounding_box_height}
    bounding_box_2 = {'x': closest_point2['x'], 'y': closest_point2['y'], 'width': bounding_box_width, 'height': bounding_box_height}
    # Gute stelle zum plotten
    # plot_strokes_without_scala(strokes_to_plot, [closest_point1, closest_point2, {'x': bounding_box_1['x'], 'y': bounding_box_1['y']},{'x': bounding_box_1['x'] + bounding_box_1['width'], 'y': bounding_box_1['y'] + bounding_box_1['height']},{'x': bounding_box_1['x'] + bounding_box_1['width'], 'y': bounding_box_1['y']}, {'x': bounding_box_1['x'], 'y': bounding_box_1['y'] + bounding_box_1['height']}, {'x': bounding_box_2['x'], 'y': bounding_box_2['y']},{'x': bounding_box_2['x'] + bounding_box_2['width'], 'y': bounding_box_2['y'] + bounding_box_2['height']},{'x': bounding_box_2['x'] + bounding_box_2['width'], 'y': bounding_box_2['y']}, {'x': bounding_box_2['x'], 'y': bounding_box_2['y'] + bounding_box_2['height']}])
    # plot_strokes_without_scala(strokes_to_plot, [closest_point1, closest_point2])

    density1 = 0
    density2 = 0
    for stroke in unrecognized_strokes:
        unrecognized_stroke_in_bounding_box1 = unrecognized_stroke_in_bounding_box(stroke, bounding_box_1)
        unrecognized_stroke_in_bounding_box2 = unrecognized_stroke_in_bounding_box(stroke, bounding_box_2)
        if unrecognized_stroke_in_bounding_box1:
            density1 += get_amount_of_points_in_bounding_box(stroke, bounding_box_1)
        if unrecognized_stroke_in_bounding_box2:
            density2 += get_amount_of_points_in_bounding_box(stroke, bounding_box_2)
    if density1 > density2:
        print('density1 > density2, also shape1 is the arrow head')
        return {'valid': {'line': _line_strokes, 'arrow head': closest_point1}}
    else:
        print('density2 > density1, also shape2 is the arrow head')
        return {'valid': {'line': _line_strokes, 'arrow head': closest_point2}}
   

def group(shapes:list[dict], unrecognized_strokes) -> list[dict]:
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)
    
    new_edge = [_unrecognized_strokes[0]]
    counter = 0
    while len(_unrecognized_strokes) > 0 and counter < len(_unrecognized_strokes) - 1:
        
        print('while')
        
        first_stroke_is_near_shape, shape1, closest_point1 = stroke_is_near_shape(new_edge[0], shapes)
        # get shapes without shape1
        shape_strokes = []
        for shape in shapes:
            shape_strokes.extend(shape['shape_strokes'])
        # plot_strokes_without_scala(shape_strokes + new_edge)     
        shapes_without_shape1 = [shape for shape in shapes if shape != shape1]
        # print(new_edge)
        # print('unrecognized_strokes', len(_unrecognized_strokes), len(new_edge))
        last_stroke_is_near_shape, shape2, closest_point2 = stroke_is_near_shape(new_edge[-1], shapes_without_shape1)
        print('first_stroke_is_near_shape', first_stroke_is_near_shape, 'last_stroke_is_near_shape', last_stroke_is_near_shape)
        plot_strokes_without_scala(shape1['shape_strokes'] + new_edge)
        plot_strokes_without_scala(shape2['shape_strokes'] + new_edge)
        
        if (first_stroke_is_near_shape and last_stroke_is_near_shape) and (shape1 != shape2):
            print('if')
            shape_strokes = []
            for shape in shapes:
                shape_strokes.extend(shape['shape_strokes'])
            # check if neighbours at the first and last stroke exist and are not already in the edge
            unrecognized_strokes_without_edge_strokes = [stroke for stroke in _unrecognized_strokes if stroke not in new_edge]
            
            nearest_neighbour1 = find_nearest_neighbouring_stroke(new_edge[0], unrecognized_strokes_without_edge_strokes, shapes, new_edge)
            nearest_neighbour2 = find_nearest_neighbouring_stroke(new_edge[-1], unrecognized_strokes_without_edge_strokes, shapes, new_edge)
            
            if nearest_neighbour1 and nearest_neighbour2:
                if nearest_neighbour1 == nearest_neighbour2:
                    new_edge.append(nearest_neighbour1)
                else:
                    new_edge.insert(0, nearest_neighbour1)
                    new_edge.append(nearest_neighbour2)
                
            elif nearest_neighbour1:
                print('nearest_neighbour1')
                new_edge.insert(0, nearest_neighbour1)
            elif nearest_neighbour2:
                print('nearest_neighbour2')
                new_edge.append(nearest_neighbour2)
            # Gute stelle zum plotten 
            plot_strokes_without_scala(shape1['shape_strokes'], new_edge[0])
            plot_strokes_without_scala(shape2['shape_strokes'], new_edge[-1])
            # plot_strokes_without_scala(shape_strokes + new_edge)
            
            closest_point1 = get_closest_point(new_edge[0], shape1['shape_strokes'])
            closest_point2 = get_closest_point(new_edge[-1], shape2['shape_strokes'])
            edge = create_edge(new_edge, closest_point1, closest_point2, shape1, shape2, _unrecognized_strokes)
           
            valid_edges.append(edge)
            for stroke in new_edge:
                if stroke in _unrecognized_strokes:
                    _unrecognized_strokes.remove(stroke)
               
                
            if len(_unrecognized_strokes) > 0:
                new_edge = [_unrecognized_strokes[0]]
            
                
        elif first_stroke_is_near_shape:
            print('elif')
            shape_strokes = [] 
            for shape in shapes:
                shape_strokes.extend(shape['shape_strokes'])
            nearest_neighbour = find_nearest_neighbouring_stroke(new_edge[-1], _unrecognized_strokes, shapes, new_edge)
            
            if nearest_neighbour == None:
                counter += 1
                _unrecognized_strokes.remove(new_edge[-1])
                if counter < len(_unrecognized_strokes):
                    new_edge = [_unrecognized_strokes[counter]]
            else:
                new_edge.append(nearest_neighbour)

        else:
            print('else')
            counter += 1
            if counter < len(_unrecognized_strokes):
                new_edge = [_unrecognized_strokes[counter]]
                 
    return valid_edges
               
                
            
    
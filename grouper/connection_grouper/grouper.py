import copy
from helper.utils import get_bounding_box
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance
import numpy as np


def determine_if_edge_is_part_of_shape(edge, shape):
    min_x, min_y, max_x, max_y, width, height= get_bounding_box(shape['shape_strokes'])
    shape_bounding_box = {'x': min_x, 'y': min_y, 'width': width, 'height': height}
    
    amount_of_points_in_bounding_box = get_amount_of_points_in_bounding_box(edge[0], shape_bounding_box)
    if amount_of_points_in_bounding_box > 3:
        return True
    else:
        return False
    
            
def filter_out_duplicate_edges(edges):
    filtered_edges = []
    shape_pairs = []
    for edge in edges:
        shape_pair = [edge['valid']['line']['source_id'], edge['valid']['line']['target_id']]
        if shape_pair not in shape_pairs:
            filtered_edges.append(edge)
        shape_pairs.append(shape_pair)
    return filtered_edges
   

def determine_shape_at_arrow_head(bounding_box_stroke, shape1, shape2):
    
    minimum_distance1 = np.inf
    minimum_distance2 = np.inf
    for stroke in shape1['shape_strokes']:
        distance1 = get_min_distance(bounding_box_stroke, stroke)
        if distance1 < minimum_distance1:
            minimum_distance1 = distance1
    for stroke in shape2['shape_strokes']:
        distance2 = get_min_distance(bounding_box_stroke, stroke)
        if distance2 < minimum_distance2:
            minimum_distance2 = distance2
    if minimum_distance1 < minimum_distance2:
        return shape1
    else:
        return shape2
    
    
def edge_combines_two_shapes(edge, shapes):
    shape1 = None
    shape2 = None
    
    for shape in shapes:
        combined_shape_strokes = []
        for shape_stroke in shape['shape_strokes']:
            combined_shape_strokes.extend(shape_stroke)
        min_x, min_y, max_x, max_y, width, height= get_bounding_box(combined_shape_strokes)
        if width < height:
            distance_threshold = width
        else:
            distance_threshold = height

        if get_min_distance(edge[0], combined_shape_strokes) < distance_threshold:
            shape1 = shape
        
    if shape1 == None:        
        return False, None, None
    
    for shape in shapes:
        if shape == shape1:
            continue
        combined_shape_strokes = []
        for shape_stroke in shape['shape_strokes']:
            combined_shape_strokes.extend(shape_stroke)
        min_x, min_y, max_x, max_y, width, height= get_bounding_box(combined_shape_strokes)

        if width < height:
            distance_threshold = width 
        else:
            distance_threshold = height 

        if get_min_distance(edge[0],combined_shape_strokes) < distance_threshold:
            shape2 = shape
    if shape1 and shape2:
        return True, shape1, shape2
    else:
        return False, None, None

def unrecognized_stroke_in_bounding_box(stroke, bounding_box) -> bool:
    for point in stroke:
        if point['x'] >= bounding_box['x'] and point['x'] <= bounding_box['x'] + bounding_box['width'] and point['y'] >= bounding_box['y'] and point['y'] <= bounding_box['y'] + bounding_box['height']:
            return True
    return False

def get_amount_of_points_in_bounding_box(stroke, bounding_box) -> int:
    amount_of_points = 0
    for point in stroke:
        if point['x'] >= bounding_box['x'] and point['x'] <= bounding_box['x'] + bounding_box['width'] and point['y'] >= bounding_box['y'] and point['y'] <= bounding_box['y'] + bounding_box['height']:
            amount_of_points += 1
    return amount_of_points
    
def create_edge(edge, shape1, shape2, unrecognized_strokes) -> dict:
    center_bounding_box1 = {'x': edge[0][0]['x'], 'y': edge[0][0]['y'], 'width': 2000, 'height': 1800}
    center_bounding_box2 = {'x': edge[0][-1]['x'], 'y': edge[0][-1]['y'], 'width': 2000, 'height': 1800}
    
    bounding_box1 = {'x': center_bounding_box1['x'] - 1000, 'y': center_bounding_box1['y'] - 1000, 'width': 2000, 'height': 2000}
    bounding_box2 = {'x': center_bounding_box2['x'] - 1000, 'y': center_bounding_box2['y'] - 1000, 'width': 2000, 'height': 2000}
    
    density1 = 0
    density2 = 0

    for stroke in unrecognized_strokes:
        unrecognized_stroke_in_bounding_box1 = unrecognized_stroke_in_bounding_box(stroke, bounding_box1)
        unrecognized_stroke_in_bounding_box2 = unrecognized_stroke_in_bounding_box(stroke, bounding_box2)
        
        if unrecognized_stroke_in_bounding_box1:
            density1 += get_amount_of_points_in_bounding_box(stroke, bounding_box1)
        if unrecognized_stroke_in_bounding_box2:
            density2 += get_amount_of_points_in_bounding_box(stroke, bounding_box2)
    if density1 > density2:
        bounding_box_stroke1 = [edge[0][0]]
        closest_shape_to_arrow_head = determine_shape_at_arrow_head(bounding_box_stroke1, shape1, shape2)
        if closest_shape_to_arrow_head == shape1:
            return {'valid': {'line': {'source': shape2['shape_candidates'], 'source_id': shape2['shape_id'], 'target': shape1['shape_candidates'], 'target_id': shape1['shape_id'], 'stroke': edge[0]}}}
        else:
            return {'valid': {'line': {'source': shape1['shape_candidates'], 'source_id': shape1['shape_id'], 'target': shape2['shape_candidates'], 'target_id': shape2['shape_id'], 'stroke': edge[0]}}}

    else:
        bounding_box_stroke2 = [edge[0][-1]]
        closest_shape_to_arrow_head = determine_shape_at_arrow_head(bounding_box_stroke2, shape1, shape2)
        if closest_shape_to_arrow_head == shape1:
            return {'valid': {'line': {'source': shape2['shape_candidates'], 'source_id': shape2['shape_id'], 'target': shape1['shape_candidates'], 'target_id': shape1['shape_id'], 'stroke': edge[0]}}}
        else:
            return {'valid': {'line': {'source': shape1['shape_candidates'], 'source_id': shape1['shape_id'], 'target': shape2['shape_candidates'], 'target_id': shape2['shape_id'], 'stroke': edge[0]}}}


   

def group(shapes:list[dict], unrecognized_strokes) -> list[dict]:
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)

    for unrecognized_stroke in _unrecognized_strokes:
        edge = [unrecognized_stroke]
        combines_two_shapes, shape1, shape2 = edge_combines_two_shapes(edge, shapes)
        
        if combines_two_shapes:
            
            valid_edge = create_edge(edge, shape1, shape2, _unrecognized_strokes)
            valid_edges.append(valid_edge)
             
    filtered_edges = filter_out_duplicate_edges(valid_edges)          
    return filtered_edges
               
                
            
    
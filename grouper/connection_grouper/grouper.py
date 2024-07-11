import copy
from helper.utils import plot_strokes_without_scala, get_strokes_from_candidate, get_position_values
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance
import numpy as np

def determine_shape_at_arrow_head(bounding_box_stroke, shape1, shape2):
    # check which shape is closer at the bounding box
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
    distance_threshold = 6000
    
    relative_distance_threshold = 0.1
    # Berechne relativen distance Threshold: Dabei ist der Threshold abhängig von der Breite der Shape
    for shape in shapes:
        min_x, min_y, max_x, max_y, width, height= get_position_values(shape['shape_strokes'])
        distance_threshold = width
        if get_min_distance(edge[0], shape['shape_strokes'][0]) < distance_threshold:
            shape1 = shape
    for shape in shapes:
        if shape == shape1:
            continue
        min_x, min_y, max_x, max_y, width, height= get_position_values(shape['shape_strokes'])
        distance_threshold = width
        if get_min_distance(edge[-1], shape['shape_strokes'][0]) < distance_threshold:
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
    
    if edge[0][0]['x'] < edge[0][-1]['x']:
        bounding_box1 = {'x': edge[0][0]['x'], 'y': edge[0][0]['y'] - 900, 'width': 2100, 'height': 2200}
        bounding_box2 = {'x': edge[0][-1]['x'] - 2000, 'y': edge[0][-1]['y'] - 900, 'width': 2100, 'height': 2200}
    else:
        bounding_box1 = {'x': edge[0][0]['x'] - 2000, 'y': edge[0][0]['y'] - 900, 'width': 2100, 'height': 2200}
        bounding_box2 = {'x': edge[0][-1]['x'], 'y': edge[0][-1]['y'] - 900, 'width': 2100, 'height': 2200}
    # Gute stelle zum plotten
    # plot_strokes_without_scala(edge + shape1['shape_strokes'] + shape2['shape_strokes'] + unrecognized_strokes, [{'x': bounding_box1['x'], 'y': bounding_box1['y']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y'] + bounding_box1['height']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y']}, {'x': bounding_box1['x'], 'y': bounding_box1['y'] + bounding_box1['height']}, {'x': bounding_box2['x'], 'y': bounding_box2['y']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y'] + bounding_box2['height']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y']}, {'x': bounding_box2['x'], 'y': bounding_box2['y'] + bounding_box2['height']}])
    # plot_strokes_without_scala(shape1['shape_strokes'] + shape2['shape_strokes'] + unrecognized_strokes, [edge[0][0]])
    # plot_strokes_without_scala(shape1['shape_strokes'] + shape2['shape_strokes'] + unrecognized_strokes, [edge[0][-1]])

    density1 = 0
    density2 = 0
    unrecognized_strokes_without_edge = []
    for stroke in unrecognized_strokes:
        if stroke != edge[0]:
            unrecognized_strokes_without_edge.append(stroke)

    for stroke in unrecognized_strokes_without_edge:
        unrecognized_stroke_in_bounding_box1 = unrecognized_stroke_in_bounding_box(stroke, bounding_box1)
        unrecognized_stroke_in_bounding_box2 = unrecognized_stroke_in_bounding_box(stroke, bounding_box2)
        # plot_strokes_without_scala(edge + shape2['shape_strokes'] + [stroke], [{'x': bounding_box1['x'], 'y': bounding_box1['y']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y'] + bounding_box1['height']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y']}, {'x': bounding_box1['x'], 'y': bounding_box1['y'] + bounding_box1['height']}, {'x': bounding_box2['x'], 'y': bounding_box2['y']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y'] + bounding_box2['height']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y']}, {'x': bounding_box2['x'], 'y': bounding_box2['y'] + bounding_box2['height']}])

        if unrecognized_stroke_in_bounding_box1:
            density1 += get_amount_of_points_in_bounding_box(stroke, bounding_box1)
        if unrecognized_stroke_in_bounding_box2:
            density2 += get_amount_of_points_in_bounding_box(stroke, bounding_box2)
    if density1 > density2:
        # determine shape at arrow head
        bounding_box_stroke1 = [edge[0][0]]
        closest_shape_to_arrow_head = determine_shape_at_arrow_head(bounding_box_stroke1, shape1, shape2)
        if closest_shape_to_arrow_head == shape1:
            print('shape1 is target')
            return {'valid': {'line': {'source': shape2['shape_candidates'], 'source_id': shape2['shape_id'], 'target': shape1['shape_candidates'], 'target_id': shape1['shape_id']}}}
        else:
            print('shape2 is target')
            return {'valid': {'line': {'source': shape1['shape_candidates'], 'source_id': shape1['shape_id'], 'target': shape2['shape_candidates'], 'target_id': shape2['shape_id']}}}

    else:
        bounding_box_stroke2 = [edge[0][-1]]
        closest_shape_to_arrow_head = determine_shape_at_arrow_head(bounding_box_stroke2, shape1, shape2)
        if closest_shape_to_arrow_head == shape1:
            print('shape1 is target')
            return {'valid': {'line': {'source': shape2['shape_candidates'], 'source_id': shape2['shape_id'], 'target': shape1['shape_candidates'], 'target_id': shape1['shape_id']}}}
        else:
            print('shape2 is target')
            return {'valid': {'line': {'source': shape1['shape_candidates'], 'source_id': shape1['shape_id'], 'target': shape2['shape_candidates'], 'target_id': shape2['shape_id']}}}


   

def group(shapes:list[dict], unrecognized_strokes) -> list[dict]:
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)
    
    for unrecognized_stroke in _unrecognized_strokes:
        edge = [unrecognized_stroke]
        combines_two_shapes, shape1, shape2 = edge_combines_two_shapes(edge, shapes)
        
        if combines_two_shapes:
            # create only an edge if both shapes are different classes
            # if shape1['shape_name'] == shape2['shape_name']:
            #     continue
            valid_edge = create_edge(edge, shape1, shape2, _unrecognized_strokes)
            valid_edges.append(valid_edge)
             
                 
    return valid_edges
               
                
            
    
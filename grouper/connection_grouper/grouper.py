import copy
from helper.utils import plot_strokes_without_scala, get_strokes_from_candidate, get_position_values
from grouper.shape_grouper.distance_calculators.distance_between_all_points import get_min_distance

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
 
    bounding_box1 = {'x': edge[0][0]['x'] - 600, 'y': edge[0][0]['y'] - 600, 'width': 1200, 'height': 1200}
    bounding_box2 = {'x': edge[0][-1]['x'] - 600, 'y': edge[0][-1]['y'] - 600, 'width': 1200, 'height': 1200}
    # Gute stelle zum plotten
    # plot_strokes_without_scala(edge + shape1['shape_strokes'] + shape2['shape_strokes'], [{'x': bounding_box1['x'], 'y': bounding_box1['y']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y'] + bounding_box1['height']},{'x': bounding_box1['x'] + bounding_box1['width'], 'y': bounding_box1['y']}, {'x': bounding_box1['x'], 'y': bounding_box1['y'] + bounding_box1['height']}, {'x': bounding_box2['x'], 'y': bounding_box2['y']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y'] + bounding_box2['height']},{'x': bounding_box2['x'] + bounding_box2['width'], 'y': bounding_box2['y']}, {'x': bounding_box2['x'], 'y': bounding_box2['y'] + bounding_box2['height']}])

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
        print('density1 > density2, also shape1 is the arrow head')
        return {'valid': {'line': {'source': shape1['shape_candidates'], 'target': shape2['shape_candidates']}}} 


    else:
        print('density2 > density1, also shape2 is the arrow head')
        return {'valid': {'line': {'source': shape2['shape_candidates'], 'target': shape1['shape_candidates']}}} 


   

def group(shapes:list[dict], unrecognized_strokes) -> list[dict]:
    valid_edges = []
    _unrecognized_strokes = copy.deepcopy(unrecognized_strokes)
    
    for unrecognized_stroke in _unrecognized_strokes:
        edge = [unrecognized_stroke]
        combines_two_shapes, shape1, shape2 = edge_combines_two_shapes(edge, shapes)
        
        if combines_two_shapes:
            print('combines_two_shapes')
            # create only an edge if both shapes are different classes
            if shape1['shape_name'] == shape2['shape_name']:
                continue
            valid_edge = create_edge(edge, shape1, shape2, _unrecognized_strokes)
            valid_edges.append(valid_edge)
             
                 
    return valid_edges
               
                
            
    
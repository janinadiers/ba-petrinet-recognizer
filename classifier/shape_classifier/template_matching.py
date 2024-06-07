from helper.features import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length, calculate_average_min_distance
from helper.utils import calculate_total_stroke_length, calculate_diagonal_length, get_bounding_box, combine_strokes, get_perfect_mock_shape, get_circle_with_points, get_rectangle_with_points
from helper.corner_detection import detect_corners


def use(grouped_ids:list[int], strokes:list[dict], params=None) -> dict:
    
    stroke = combine_strokes(grouped_ids, strokes)
    if params is None:
        params = (50, 6, 54, 120)
    else:
        params = params
        
    if len(stroke) < params[0]:
        return {'invalid': grouped_ids}
    # stroke = remove_outliers(stroke) 
    perfect_mock_shape = get_perfect_mock_shape(stroke)
    perfect_circle = perfect_mock_shape['circle']
    perfect_rect = perfect_mock_shape['rectangle']
    if perfect_mock_shape['bounding_box']['width'] == 0 or perfect_mock_shape['bounding_box']['height'] == 0:
        return {'invalid': grouped_ids}
    if ((perfect_mock_shape['bounding_box']['width'] / perfect_mock_shape['bounding_box']['height']) > params[1]) or ((perfect_mock_shape['bounding_box']['height'] / perfect_mock_shape['bounding_box']['width']) > params[1]):
        return {'invalid': grouped_ids}
    
    density = calculate_total_stroke_length(stroke) / calculate_diagonal_length(get_bounding_box(stroke))
    if  density < 2 or density > 5:
        return {'invalid': grouped_ids}
    
    
    average_distance_circle = calculate_average_min_distance(perfect_circle, stroke)
    average_distance_rect = calculate_average_min_distance(perfect_rect, stroke)
    
    if average_distance_circle <= 500 or average_distance_rect <= 500:
        strokes = [strokes[trace_id] for trace_id in grouped_ids]
        # corners = detect_corners(strokes, params[3], params[2])
        # if corners == 0:
        #     return {'valid': {'circle': grouped_ids}}
        # else:
        #     return {'valid': {'rectangle': grouped_ids}}
        if average_distance_circle < average_distance_rect:
            return {'valid': {'circle': grouped_ids}}
        else:
            return {'valid': {'rectangle': grouped_ids}}
    else:
        return {'invalid': grouped_ids}
  
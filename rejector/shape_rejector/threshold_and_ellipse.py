import numpy as np
from rejector.shape_rejector.rejector_with_threshold import use as use_rejector_with_threshold
from scripts.define_clusters import calculate_ellipse_parameters
from helper.utils import hellinger_distance,  distance, pearsons_correlation
import json


def use(X, candidate):
    print('threshold and ellipse')
    first_result = use_rejector_with_threshold(X, candidate)
    with open(f'rejector/clusters.json', 'r') as f:
        data = json.load(f)

    F1_circle = data['circle']['F1']
    F2_circle = data['circle']['F2']
    circle_S = data['circle']['S']
    F1_rectangle = data['rectangle']['F1']
    F2_rectangle = data['rectangle']['F2']
    rectangle_S = data['rectangle']['S']
    
    distance_to_F1_circle = distance(X, F1_circle)

    distance_to_F2_circle = distance(X, F2_circle)

    distance_to_F1_circle = [abs(X[dim] - F1_circle[dim]) for dim in range(len(F1_circle))]
    distance_to_F2_circle = [abs(X[dim] - F2_circle[dim]) for dim in range(len(F2_circle))]
    
    total_distance_circle = [distance_to_F1_circle[dim] + distance_to_F2_circle[dim] for dim in range(len(distance_to_F1_circle))]
    absolute_sum_circle = np.max(total_distance_circle)
    
    distance_to_F1_rectangle = [abs(X[dim] - F1_rectangle[dim]) for dim in range(len(F1_rectangle))]
    distance_to_F2_rectangle = [abs(X[dim] - F2_rectangle[dim]) for dim in range(len(F2_rectangle))]
    
    total_distance_rectangle = [distance_to_F1_rectangle[dim] + distance_to_F2_rectangle[dim] for dim in range(len(distance_to_F1_rectangle))]
    
    absolute_sum_rectangle = sum(total_distance_rectangle)

            
    print('new_circle_S:', absolute_sum_circle, 'circle_S:', circle_S, 'new_rectangle_S:', absolute_sum_rectangle, 'rectangle_S:', rectangle_S)
    
    if (absolute_sum_circle > circle_S) and (absolute_sum_rectangle >rectangle_S) and ('invalid' in first_result):
        return {'invalid': candidate}
    else:
        return {'valid': candidate}
        
    
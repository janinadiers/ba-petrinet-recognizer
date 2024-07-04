import numpy as np
from helper.utils import distance
import json


def use(X, candidate):
    print('threshold and ellipse')
    # first_result = use_rejector_with_threshold(X, candidate)
    with open(f'rejector/clusters.json', 'r') as f:
        data = json.load(f)
    F1_circle = data['circle']['F1']
    F2_circle = data['circle']['F2']
    circle_S = data['circle']['S']
    rectangle_S = data['rectangle']['S']
    F1_rectangle = data['rectangle']['F1']
    F2_rectangle = data['rectangle']['F2']
    
    
    distance_to_F1_circle = distance(X, F1_circle)
    distance_to_F2_circle = distance(X, F2_circle)
    total_distance_circle = distance_to_F1_circle + distance_to_F2_circle
    
    distance_to_F1_rectangle = distance(X, F1_rectangle)
    distance_to_F2_rectangle = distance(X, F2_rectangle)
    total_distance_rectangle = distance_to_F1_rectangle + distance_to_F2_rectangle
   
            
    print('new_circle_S:', total_distance_circle, 'circle_S:', circle_S, 'new_rectangle_S:', total_distance_rectangle, 'rectangle_S:', rectangle_S)
    
    if (total_distance_circle <= circle_S) or (total_distance_rectangle <=rectangle_S):
        print('VALIDDDDDDDDD')
        return {'valid': candidate}
    else:
        print('INVALIDDDDDDDDDDDDDDDDDDDDDDD')

        return {'invalid': candidate}
        
        
    
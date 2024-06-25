import numpy as np
from rejector.shape_rejector.rejector_with_threshold import use as use_rejector_with_threshold
from scripts.define_clusters import calculate_ellipse_parameters
from helper.utils import hellinger_distance,  distance, pearsons_correlation
import json


def use(X, candidate):
    print('use hellinger and correlation')
    with open(f'rejector/clusters.json', 'r') as f:
        data = json.load(f)
    F1_circle = data['circle']['F1']
    F1_rectangle = data['rectangle']['F1']
    cluster_center_circle = data['circle']['cluster_center']    
    cluster_center_rectangle = data['rectangle']['cluster_center']
    similarity_circle = data['circle']['similarity']
    similarity_rectangle = data['rectangle']['similarity']
    F1_circle_distance_to_center = hellinger_distance(F1_circle, cluster_center_circle)
    F1_rectangle_distance_to_center = hellinger_distance(F1_rectangle, cluster_center_rectangle)
   
    hellinger_distance_circle = hellinger_distance(X, cluster_center_circle)
    pearsons_correlation_circle = pearsons_correlation(X, cluster_center_circle)
    hellinger_distance_rectangle = hellinger_distance(X, cluster_center_rectangle)
    pearsons_correlation_rectangle = pearsons_correlation(X, cluster_center_rectangle)
    
    if hellinger_distance_circle < F1_circle_distance_to_center and hellinger_distance_rectangle < F1_rectangle_distance_to_center and pearsons_correlation_circle > similarity_circle and pearsons_correlation_rectangle > similarity_rectangle:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
    
        
    
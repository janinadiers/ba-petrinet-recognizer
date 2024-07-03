from helper.utils import hellinger_distance,  distance, pearsons_correlation
import json


def use(X, candidate):
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
    print('F1_circle_distance_to_center', X, cluster_center_circle, cluster_center_rectangle)
    hellinger_distance_circle = hellinger_distance(X, cluster_center_circle)
    pearsons_correlation_circle = pearsons_correlation(X, cluster_center_circle)
    hellinger_distance_rectangle = hellinger_distance(X, cluster_center_rectangle)
    pearsons_correlation_rectangle = pearsons_correlation(X, cluster_center_rectangle)
    
    if hellinger_distance_circle < F1_circle_distance_to_center and hellinger_distance_rectangle < F1_rectangle_distance_to_center and pearsons_correlation_circle > similarity_circle and pearsons_correlation_rectangle > similarity_rectangle:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
    
        
    
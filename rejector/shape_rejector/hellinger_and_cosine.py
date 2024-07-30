from helper.utils import hellinger_distance,  distance, pearsons_correlation
import json
from sklearn.metrics.pairwise import cosine_similarity


def use(X, candidate, expected_shapes):
    print('use hellinger and cosine', len(X))
    with open(f'rejector/clusters.json', 'r') as f:
        data = json.load(f)
    circle_center = data['circle']['cluster_center']
    print('circle_center', circle_center)
    furthest_similarity_in_circle_cluster = data['circle']['similarity']
    furthest_distance_in_circle_cluster = data['circle']['distance']
    
    rectangle_center = data['rectangle']['cluster_center']
    furthest_similarity_in_rectangle_cluster = data['rectangle']['similarity']
    furthest_distance_in_rectangle_cluster = data['rectangle']['distance']
    
    print('!!!!!!!!!!!!!!!!!!!!X: ', X, 'circle_center: ', circle_center, 'rectangle_center: ', rectangle_center)
    X_distance_to_circle_center = hellinger_distance(X, circle_center)
    X_cosine_similarity_to_circle_center = cosine_similarity([X], [circle_center])
    X_distance_to_rectangle_center = hellinger_distance(X, rectangle_center)
    X_cosine_similarity_to_rectangle_center = cosine_similarity([X], [rectangle_center])
    
    if (X_distance_to_circle_center <= furthest_distance_in_circle_cluster and X_cosine_similarity_to_circle_center >= furthest_similarity_in_circle_cluster) or (X_distance_to_rectangle_center <= furthest_distance_in_rectangle_cluster and X_cosine_similarity_to_rectangle_center >= furthest_similarity_in_rectangle_cluster):
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
    
        
    
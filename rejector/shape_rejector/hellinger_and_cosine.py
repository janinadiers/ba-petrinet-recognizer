from helper.utils import hellinger_distance,  distance, pearsons_correlation
import json
from sklearn.metrics.pairwise import cosine_similarity



def use(X, candidate, expected_shapes):
    with open(f'rejector/clusters.json', 'r') as f:
        data = json.load(f)
    shape_center = data['shape']['cluster_center']
    furthest_similarity_in_cluster = data['no_shape']['similarity']
    furthest_distance_in_cluster = data['shape']['distance']
    
    
    X_distance_to_shape_center = hellinger_distance(X[0], shape_center)
    X_cosine_similarity_to_shape_center = cosine_similarity([X], [[shape_center]])
    
    
    if X_distance_to_shape_center <= furthest_distance_in_cluster and X_cosine_similarity_to_shape_center >= furthest_similarity_in_cluster:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
    
        
    
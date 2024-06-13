
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features


def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]]):
    feature_vector_circle_rectangle = get_circle_rectangle_features(candidate, strokes)
    feature_vector_shape_no_shape = get_shape_no_shape_features(candidate, strokes)
    print('candiddate', candidate)  
    print('feature_vector_circle_rectangle', feature_vector_circle_rectangle['features'])
    if feature_vector_circle_rectangle['features'] == None:
        return {'invalid': candidate}
    if feature_vector_shape_no_shape['features'] == None:
        return {'invalid': candidate}
    candidate_is_valid_shape = rejector(feature_vector_shape_no_shape['features'], candidate)
    # return classifier(feature_vector_circle_rectangle['features'], candidate)
    if 'valid' in candidate_is_valid_shape:
        # return{'valid': {'circle': candidate}}
        result = classifier(feature_vector_circle_rectangle['features'], candidate)
        return result
    else:
        return {'invalid': candidate}
    
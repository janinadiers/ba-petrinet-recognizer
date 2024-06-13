
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features


def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]]):
    feature_vector_circle_rectangle = get_circle_rectangle_features(candidate, strokes)
    feature_vector_shape_no_shape = get_shape_no_shape_features(candidate, strokes)
    print(feature_vector_circle_rectangle['features'], feature_vector_shape_no_shape['features'])
    
    candidate_is_valid_shape = rejector(feature_vector_shape_no_shape['features'], candidate)
    if candidate_is_valid_shape:
        return{'valid': {'circle': candidate}}
        result = classifier(feature_vector_circle_rectangle['features'], candidate)
        return result
    else:
        return {'invalid': candidate}
    

from helper.features import get_circle_rectangle_features, get_shape_no_shape_features
from helper.utils import get_strokes_from_candidate


def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]]):
    feature_vector_circle_rectangle = get_circle_rectangle_features(candidate, strokes)
    feature_vector_shape_no_shape = get_shape_no_shape_features(candidate, strokes)
    if feature_vector_circle_rectangle['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    if feature_vector_shape_no_shape['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    candidate_is_valid_shape = rejector(feature_vector_shape_no_shape['features'], candidate, get_strokes_from_candidate(candidate, strokes))
    # return classifier(feature_vector_circle_rectangle['features'], candidate)
    if 'valid' in candidate_is_valid_shape:
        # return{'valid': {'circle': candidate}}
        result = classifier(feature_vector_circle_rectangle['features'], candidate)
        if 'valid' in result:
            return result, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
        else:
            return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    else:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    
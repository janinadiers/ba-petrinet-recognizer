
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features, get_hellinger_correlation_features
from rejector.shape_rejector.hellinger_and_correlation import use as hellinger_and_correlation




def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]], expected_shapes = None)-> dict:
    feature_vector_circle_rectangle = get_circle_rectangle_features(candidate, strokes)
    feature_vector_shape_no_shape = get_shape_no_shape_features(candidate, strokes)
    # feature_vector_hellinger_correlation = get_hellinger_correlation_features(candidate, strokes)
    if feature_vector_circle_rectangle['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    if feature_vector_shape_no_shape['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    # if rejector['name'] == 'rejector_with_threshold':
    #     candidate_is_valid_shape = rejector['use'](feature_vector_shape_no_shape['features'], candidate)
    # else:
    candidate_is_valid_shape = rejector['use'](feature_vector_shape_no_shape['features'], candidate, expected_shapes)
    if 'invalid' in candidate_is_valid_shape:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    # hellinger_and_correlation_result = hellinger_and_correlation(feature_vector_hellinger_correlation['features'], candidate)
    # if 'invalid' in hellinger_and_correlation_result:
    #     return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    if classifier['name'] == 'perfect_mock_classifier':
        return classifier['use'](feature_vector_shape_no_shape['features'], candidate, expected_shapes)
    else:
        result = classifier['use'](feature_vector_circle_rectangle['features'], candidate)
    if 'valid' in result:
        return result, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    else:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']

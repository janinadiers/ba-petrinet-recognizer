
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features

def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]], expected_shapes = None)-> dict:
    feature_vector_circle_rectangle = get_circle_rectangle_features(candidate, strokes)
    # feature_vector_circle_rectangle = {'features': [], 'feature_names': []}
    feature_vector_shape_no_shape = get_shape_no_shape_features(candidate, strokes)
    if feature_vector_circle_rectangle['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    
    if feature_vector_shape_no_shape['features'] == None:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    
    candidate_is_valid_shape = rejector['use'](feature_vector_shape_no_shape['features'], candidate, expected_shapes)
    # candidate_is_valid_shape = rejector['use'](feature_vector_circle_rectangle['features'], candidate, expected_shapes)

    if 'invalid' in candidate_is_valid_shape:
        
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    if classifier['name'] == 'perfect_mock_classifier':
        result, x, y =  classifier['use'](feature_vector_shape_no_shape['features'], candidate, expected_shapes)
        if 'valid' in result:
            return result, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']

        else:
            print('invalid by classifier')
            return {'invalid by classifier': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']

    else:
        result = classifier['use'](feature_vector_circle_rectangle['features'], candidate)
    if 'valid' in result:
        return result, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']
    else:
        return {'invalid': candidate}, feature_vector_shape_no_shape['feature_names'], feature_vector_circle_rectangle['feature_names']

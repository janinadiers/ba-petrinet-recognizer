
from helper.features import get_feature_vector

def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]]):
    feature_vector = get_feature_vector(candidate)
    candidate_is_valid_shape = rejector(feature_vector)
    if candidate_is_valid_shape:
        return classifier(feature_vector)
    else:
        return {'invalid': candidate}
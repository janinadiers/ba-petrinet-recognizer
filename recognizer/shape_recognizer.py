
from helper.features import get_feature_vector
from helper.utils import combine_strokes


def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]]):
    feature_vector = get_feature_vector(candidate, strokes)
    # candidate_is_valid_shape = rejector(feature_vector)
    # if candidate_is_valid_shape:
    result = classifier(feature_vector['features'], candidate)
    return result
    # else:
    #     return {'invalid': candidate}
    
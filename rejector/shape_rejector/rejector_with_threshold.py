from scripts.determine_best_closed_shape_threshold import get_threshold

def use(X, candidate, expected_shapes)-> dict:
    
    # print('rejector_with_threshold', path_length_of_candidate * 0.02, X[0])
    # ursprünglich 0.4
    # threshold = get_threshold()
    print('X threshold', X[0])
    if X[0] < 1.0:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
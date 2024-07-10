from scripts.determine_best_closed_shape_threshold import get_threshold

def use(X, candidate)-> dict:
    # points = [point for stroke in strokes_of_candidate for point in stroke]
    # scaled_points = scale(strokes_of_candidate)
    # # print('scaled_points', scaled_points)
    # translated_points = translate_to_origin(scaled_points)  
     
    # path_length_of_candidate = path_length(translated_points[0])
    
    # print('rejector_with_threshold', path_length_of_candidate * 0.02, X[0])
    # ursprünglich 0.4
    # threshold = get_threshold()
    if X[0] < 1:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
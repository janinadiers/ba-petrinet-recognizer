from helper.utils import path_length
from helper.normalizer import scale, translate_to_origin

def use(X, candidate)-> dict:
    # points = [point for stroke in strokes_of_candidate for point in stroke]
    # scaled_points = scale(strokes_of_candidate)
    # # print('scaled_points', scaled_points)
    # translated_points = translate_to_origin(scaled_points)  
     
    # path_length_of_candidate = path_length(translated_points[0])
    
    # print('rejector_with_threshold', path_length_of_candidate * 0.02, X[0])
    if X[0] < 0.4:
        return {'valid': candidate}
    else:
        return {'invalid': candidate}
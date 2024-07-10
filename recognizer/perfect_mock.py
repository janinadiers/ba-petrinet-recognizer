
def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]], expected_shapes) -> dict:
    print('perfect mock!!!')
    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if set(trace_ids) == set(candidate) and (shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse' or shape_name == 'parallelogram' or shape_name == 'diamond'):
                if shape_name == 'ellipse': 
                    return {'valid': {'circle': candidate}}, [], []
                elif shape_name == 'parallelogram':
                    return {'valid': {'rectangle': candidate}}, [], []
                elif shape_name == 'diamond':
                    return {'valid': {'rectangle': candidate}}, [], []
                return {'valid': {shape_name: candidate}}, [], []
            
            
        
    return {'invalid': candidate}, [], []
    
    



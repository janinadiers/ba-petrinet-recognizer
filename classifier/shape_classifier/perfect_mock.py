
def use(X, candidate, expected_shapes) -> dict:
    print('perfect mock!!!')

    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if set(trace_ids) == set(candidate) and (shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse'):
                if shape_name == 'ellipse': 
                    return {'valid': {'circle': candidate}}, [], []
                return {'valid': {shape_name: candidate}}, [], []
            
            
        
    return {'invalid': candidate}, [], []
    
    



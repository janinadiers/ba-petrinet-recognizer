
def use(X, candidate, expected_shapes) -> dict:
    print('perfect mock rejector!!!', len(expected_shapes))

    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            
            if set(trace_ids) == set(candidate) and (shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse'):
                return {'valid': candidate}
              
    return {'invalid': candidate}
    
    



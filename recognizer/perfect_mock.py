
def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]], expected_shapes) -> dict:
    print('perfect mock!!!')
    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if set(trace_ids) == set(candidate) and (shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse'):
                print(shape_name)
                if shape_name == 'ellipse': 
                    print('iffffff')
                    print('-------------------------- >>>>>>>>>>>>>>>>>> valid', shape_name)
                    return {'valid': {'circle': candidate}}, [], []
                # print('-------------------------- >>>>>>>>>>>>>>>>>> valid', shape_name)
                return {'valid': {shape_name: candidate}}, [], []
            
            
        
    return {'invalid': candidate}, [], []
    
    



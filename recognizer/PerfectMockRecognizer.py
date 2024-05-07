# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde


count:int = 0
        
def is_a_shape(grouped_indices:tuple, expected_shapes:list[dict]) -> dict:
    global count
    count += 1
    grouped_indices:list[int] = list(grouped_indices)
    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if trace_ids == grouped_indices and (shape_name == 'circle' or shape_name == 'rectangle'):
                print('-------------------------- >>>>>>>>>>>>>>>>>> valid')
                return {'valid': {shape_name: trace_ids}}
        
    return {'invalid': grouped_indices}
    
def get_count():
    global count
    return count
    



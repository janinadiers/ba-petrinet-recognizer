# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde


count:int = 0
        
def is_a_shape(grouped_ids:list[int], expected_shapes:list[dict]) -> dict:
    global count
    count += 1
    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if set(trace_ids) == set(grouped_ids) and (shape_name == 'circle' or shape_name == 'rectangle'):
                print('-------------------------- >>>>>>>>>>>>>>>>>> valid', shape_name)
                return {'valid': {shape_name: trace_ids}}
        
    return {'invalid': grouped_ids}
    
def get_count():
    global count
    return count
    



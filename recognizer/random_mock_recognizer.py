# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde
import random

        
def is_a_shape(grouped_ids:list[int], expected_shapes:list[dict]) -> dict:
    # randomly decide if group is valid or invalid
    is_valid = random.choice([True, False])
    shape_name = random.choice(['circle', 'rectangle'])
    if is_valid:
        print('-------------------------- >>>>>>>>>>>>>>>>>> valid', shape_name)
        return {'valid': {shape_name: grouped_ids}}
    else:
        print('-------------------------- >>>>>>>>>>>>>>>>>> invalid', shape_name)
        return {'invalid': grouped_ids}
    

    



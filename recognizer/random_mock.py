# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde
import random

        
def recognize(rejector:callable, classifier:callable, candidate:list[int], strokes:list[list[dict]], expected_shapes) -> dict:
    # randomly decide if group is valid or invalid
    is_valid = random.choice([True, False])
    shape_name = random.choice(['circle', 'rectangle'])
    if is_valid:
        print('-------------------------- >>>>>>>>>>>>>>>>>> valid', shape_name)
        return {'valid': {shape_name: candidate}}
    else:
        print('-------------------------- >>>>>>>>>>>>>>>>>> invalid', shape_name)
        return {'invalid': candidate}
    

    



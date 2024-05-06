# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde

class PerfectMockRecognizer:
    count = 0
    def __init__(self, expected_shapes):
        self.expected_shapes = expected_shapes
        
        
    def is_a_shape(self, grouped_indices):
        PerfectMockRecognizer.count += 1
        grouped_indices = list(grouped_indices)
        # print('grouped_indices: ', grouped_indices)
        for dictionary in self.expected_shapes:
            for key, val in dictionary.items():
                if val == grouped_indices and (key == 'circle' or key == 'rectangle'):
                    print('-------------------------- >>>>>>>>>>>>>>>>>> valid')
                    return {'valid': {key: val}}
            
        return {'invalid': grouped_indices}
    
    def get_count(self):
        return PerfectMockRecognizer.count
    



from helper.parsers import parse_ground_truth
import pandas as pd

class EvaluationWrapper:
    def __init__(self, recognize:callable):
        self._recognize = recognize
        self.truth = None
        self.columns = ['circle', 'rectangle','no_shape', 'total', 'accuracy']
        self.rows = ['circle', 'rectangle', 'diamond', 'ellipse', 'parallelogram', 'line', 'double circle', 'no_shape', 'total']
        self.matrix = pd.DataFrame(0, index=self.rows, columns=self.columns)
        self.stroke_min = 50
        self.diagonal_to_stroke_length = 6
        self.upper_bound_angle = 110
        self.lower_bound_angle = 54


    def __str__(self):
        return self.matrix.to_string()

    def setCurrentFilePath(self, file_path):
        self.truth = parse_ground_truth(file_path)
        
    
    def set_total(self):
        for row in self.rows:
            self.matrix.at[row, 'total'] = self.matrix.loc[row].sum()
        for column in self.columns:
            self.matrix.at['total', column] = self.matrix[column].sum()
        self.matrix.at['total', 'total'] = self.matrix['total'].sum()
    
    def set_accuracy(self):
        for row in self.rows:
            if self.matrix.at[row, 'total'] != 0:
                if row == 'circle' or row == 'rectangle':
                    self.matrix.at[row, 'accuracy'] = str(int((self.matrix.at[row, row] / self.matrix.at[row, 'total']) * 100)) + '%'
                elif row != 'total':
                    if row == 'ellipse':
                        amount_ellipse_as_circle = int((self.matrix.at[row, 'circle'] / self.matrix.at[row, 'total']) * 100)
                        amount_ellipse_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_ellipse_as_circle + amount_ellipse_as_no_shape) + '%'
                    elif row == 'parallelogram':
                        amount_parallelogram_as_rectangle = int((self.matrix.at[row, 'rectangle'] / self.matrix.at[row, 'total']) * 100)
                        amount_parallelogram_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_parallelogram_as_rectangle + amount_parallelogram_as_no_shape) + '%'
                    else:
                        self.matrix.at[row, 'accuracy'] = str(int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)) + '%'
            else:
                self.matrix.at[row, 'accuracy'] = '-'  
                
    def get_params(self):
        return int(self.stroke_min), int(self.diagonal_to_stroke_length), int(self.lower_bound_angle), int(self.upper_bound_angle)
        
            
    def set_params(self, stroke_min, diagonal_to_stroke_length, lower_bound_angle, upper_bound_angle):
        print('Setting params:', stroke_min, diagonal_to_stroke_length, lower_bound_angle, upper_bound_angle)
        self.stroke_min = stroke_min
        self.diagonal_to_stroke_length = diagonal_to_stroke_length
        self.upper_bound_angle = upper_bound_angle
        self.lower_bound_angle = lower_bound_angle
        
    def recognize(self, candidate, content):
       
        recognizer_result = self._recognize(candidate, content)
        truth_contains_candidate = False
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):
                    truth_contains_candidate = True
                    if 'valid' in recognizer_result:
                        shape_name_recognizer_result = next(iter(recognizer_result['valid']))
                       
                        self.matrix.at[shape_name, shape_name_recognizer_result] += 1
                    else:
                        self.matrix.at[shape_name, 'no_shape'] += 1
        if not truth_contains_candidate and not 'valid' in recognizer_result:
            self.matrix.at['no_shape', 'no_shape'] += 1
        elif not truth_contains_candidate and 'valid' in recognizer_result:
            shape_name_recognizer_result = next(iter(recognizer_result['valid']))
            self.matrix.at['no_shape', shape_name_recognizer_result] += 1
        
        return recognizer_result
        

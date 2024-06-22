from helper.parsers import parse_ground_truth
import pandas as pd
from helper.utils import combine_strokes
class EvaluationWrapper:
    def __init__(self, recognize:callable):
        self._recognize = recognize
        self.truth = None
        self.columns = ['circle', 'rectangle','no_shape', 'total', 'accuracy']
        self.rows = ['circle', 'rectangle', 'diamond', 'ellipse', 'parallelogram', 'line', 'double circle', 'no_shape', 'total']
        self.matrix = pd.DataFrame(0, index=self.rows, columns=self.columns)


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
                        # amount_ellipse_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_ellipse_as_circle) + '%'
                    elif row == 'parallelogram':
                        amount_parallelogram_as_rectangle = int((self.matrix.at[row, 'rectangle'] / self.matrix.at[row, 'total']) * 100)
                        amount_parallelogram_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_parallelogram_as_rectangle + amount_parallelogram_as_no_shape) + '%'
                    else:
                        self.matrix.at[row, 'accuracy'] = str(int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)) + '%'
            else:
                self.matrix.at[row, 'accuracy'] = '-'  
        
    def recognize(self, rejector, classifier, candidate, strokes):
        recognizer_result = self._recognize(rejector, classifier, candidate, strokes)
        # print('djaksdkas', self.truth)
        truth_contains_candidate = False
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):  
                    truth_contains_candidate = True
                    if 'valid' in recognizer_result[0]:
                       
                        shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
                        if not shape_name == shape_name_recognizer_result:
                            print(f'>>>>>>>>>>>>>>>>>>circle or rectangle confusion! {shape_name}>>>>>>>>>>>>>>>>>>>>>>>>>', shape_name, shape_name_recognizer_result)
                        else:
                            print(f'>>>>>>>>>>>>>>>>>>correct recognition! {shape_name}>>>>>>>>>>>>>>>>>>>>>>>>>', shape_name)
                        self.matrix.at[shape_name, shape_name_recognizer_result] += 1
                    else:
                        if shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse':
                            print('>>>>>>>>>>>>>>>>>>wrong rejection!>>>>>>>>>>>>>>>>>>>>>>>>>', shape_name)
                            
                        self.matrix.at[shape_name, 'no_shape'] += 1
        
        if not truth_contains_candidate and not 'valid' in recognizer_result[0]:
            self.matrix.at['no_shape', 'no_shape'] += 1
        elif not truth_contains_candidate and 'valid' in recognizer_result[0]:
            shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<wrong recognition: no_shape was recognized!>>>>>>>>>>>>>>>>>>>>>', shape_name_recognizer_result)

            self.matrix.at['no_shape', shape_name_recognizer_result] += 1
        
        return recognizer_result
        

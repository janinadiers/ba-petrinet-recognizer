from helper.parsers import parse_ground_truth
import pandas as pd
from helper.utils import plot_strokes, get_strokes_from_candidate
from helper.normalizer import scale, translate_to_origin
import datetime
class EvaluationWrapper:
    def __init__(self, recognize:callable):
        self._recognize = recognize
        self.truth = None
        self.columns = ['circle', 'rectangle','no_shape', 'total', 'truth', 'accuracy']
        self.rows = ['circle', 'rectangle', 'diamond', 'ellipse', 'parallelogram', 'line', 'double circle', 'no_shape', 'total']
        self.matrix = pd.DataFrame(0, index=self.rows, columns=self.columns)
        self._candidates = []
        self.recognizer_calls = 0
        self.start_time = None
        self.times = []
        self.valid_shapes = 0


    def get_amount_of_valid_shapes(self):
        return self.valid_shapes
    
    def calculate_average_time(self):
        total_time = datetime.timedelta(0)
        for time in self.times:
            total_time += time
        return total_time / len(self.times)
    
    def __str__(self):
        print('recognizer calls: ', self.recognizer_calls)
        print('average time: ', self.calculate_average_time())
        return self.matrix.to_string()

    def save_time(self):
        self.times.append(datetime.datetime.now() - self.start_time)

    def setCurrentFilePath(self, file_path):
        self.truth = parse_ground_truth(file_path)
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                self.matrix.at[shape_name, 'truth'] += 1  
        self.start_time = datetime.datetime.now()

    
    def set_total(self):
        for row in self.rows:
            # self.matrix.at[row, 'total'] = self.matrix.loc[row].sum()
            # sum(distance(points[i], points[i+1]) for i in range(len(points) - 1))
            self.matrix.at[row, 'total'] = self.matrix.at[row, 'circle'] + self.matrix.at[row, 'rectangle'] + self.matrix.at[row, 'no_shape']
        for column in self.columns:
            self.matrix.at['total', column] = self.matrix[column].sum()
        self.matrix.at['total', 'total'] = self.matrix['total'].sum()
    
    def set_accuracy(self):
        for row in self.rows:
            if self.matrix.at[row, 'truth'] != 0:
                if row == 'circle' or row == 'rectangle':
                    self.matrix.at[row, 'accuracy'] = str(int((self.matrix.at[row, row] / self.matrix.at[row, 'truth']) * 100)) + '%'
                elif row != 'total':
                    if row == 'ellipse':
                        amount_ellipse_as_circle = int((self.matrix.at[row, 'circle'] / self.matrix.at[row, 'truth']) * 100)
                        # amount_ellipse_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'total']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_ellipse_as_circle) + '%'
                    elif row == 'parallelogram':
                        amount_parallelogram_as_rectangle = int((self.matrix.at[row, 'rectangle'] / self.matrix.at[row, 'truth']) * 100)
                        amount_parallelogram_as_no_shape = int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'truth']) * 100)
                        self.matrix.at[row, 'accuracy'] = str(amount_parallelogram_as_rectangle + amount_parallelogram_as_no_shape) + '%'
                    else:
                        self.matrix.at[row, 'accuracy'] = str(int((self.matrix.at[row, 'no_shape'] / self.matrix.at[row, 'truth']) * 100)) + '%'
            else:
                self.matrix.at[row, 'accuracy'] = '-'  
        
    def recognize(self, rejector, classifier, candidate, strokes):
        self.recognizer_calls += 1
        recognizer_result = self._recognize(rejector, classifier, candidate, strokes, self.truth)
        truth_contains_candidate = False
        
        self._candidates.append(candidate)
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):  
                    self.valid_shapes += 1
                    print('>>>>>>>>>>>>>>>>>>truth contains candidate!>>>>>>>>>>>>>>>>>>>>>>>>>', candidate, shape_name)
                    truth_contains_candidate = True
                    if 'valid' in recognizer_result[0]:
                        shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
                        self.matrix.at[shape_name, shape_name_recognizer_result] += 1
                    else:
                        if shape_name == 'circle' or shape_name == 'rectangle' or shape_name == 'ellipse':
                            print('>>>>>>>>>>>>>>>>>>wrong rejection!>>>>>>>>>>>>>>>>>>>>>>>>>', shape_name)
                            # strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
                            # scaled_strokes = scale(strokes_of_candidate)
                            # translated_strokes = translate_to_origin(scaled_strokes)
                            # plot_strokes([translated_strokes[0]])
                            
                        self.matrix.at[shape_name, 'no_shape'] += 1
        
        if not truth_contains_candidate and not 'valid' in recognizer_result[0]:
            self.matrix.at['no_shape', 'no_shape'] += 1
            self.matrix.at['no_shape', 'truth'] += 1
            
        elif not truth_contains_candidate and 'valid' in recognizer_result[0]:
            shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<wrong recognition: no_shape was recognized!>>>>>>>>>>>>>>>>>>>>>', shape_name_recognizer_result)
            self.matrix.at['no_shape', 'truth'] += 1
            self.matrix.at['no_shape', shape_name_recognizer_result] += 1
            # strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
            # scaled_strokes = scale(strokes_of_candidate)
            # translated_strokes = translate_to_origin(scaled_strokes)
            # plot_strokes([translated_strokes[0]])
       
        return recognizer_result
        

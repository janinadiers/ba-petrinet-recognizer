from helper.parsers import parse_ground_truth, parse_strokes_from_inkml_file, parse_ratio_from_inkml_file
import pandas as pd
from helper.normalizer import convert_coordinates
from helper.normalizer import resample_strokes
import datetime
class EvaluationWrapper:
    def __init__(self, recognize:callable, group_connections:callable):
        self._recognize = recognize
        self._group_connections = group_connections
        self.truth = None
        self.columns = ['circle', 'rectangle','no_shape', 'total', 'truth', 'accuracy']
        self.rows = ['circle', 'rectangle', 'diamond', 'ellipse', 'parallelogram', 'line', 'double circle', 'no_shape', 'total']
        self.rows2 = ['line', 'no_shape']
        self.columns2 = ['line', 'truth', 'accuracy']
        self.matrix = pd.DataFrame(0, index=self.rows, columns=self.columns)
        self.matrix2 = pd.DataFrame(0, index=self.rows2, columns=self.columns2)
        self.recognizer_calls = 0
        self.start_time = None
        self.times = []
        self.valid_shapes = 0
        self.file_path = None
        

    def get_truth_without_lines(self):
        truth_without_lines = []
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if shape_name != 'line':
                    truth_without_lines.append({shape_name: trace_ids})
        return truth_without_lines
    
    def get_lines(self):
        lines = []
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if shape_name == 'line':
                    for trace_id in trace_ids:
                        lines.append([trace_id])
        return lines

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
    
    def get_connection_evaluation(self):
        self.matrix2.at['line', 'accuracy'] = str((self.matrix2['line']['line']) / (self.matrix2.loc['line']['truth']) * 100) + '%'
        return self.matrix2.to_string()
    

    def save_time(self):
        self.times.append(datetime.datetime.now() - self.start_time)

    def setCurrentFilePath(self, file_path):
        self.file_path = file_path
        self.truth = parse_ground_truth(file_path)
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                self.matrix.at[shape_name, 'truth'] += 1  
        
        self.start_time = datetime.datetime.now()
        
    
    def set_amount_of_invalid_candidates(self, candidates: list):
        for candidate in candidates:
            truth_contains_candidate = False
            for dictionary in self.truth:
                for shape_name, trace_ids in dictionary.items():
                    if set(trace_ids) == set(candidate): 
                        truth_contains_candidate = True
            if not truth_contains_candidate:
                self.matrix.at['no_shape', 'truth'] += 1

    
    def set_total(self):
        for row in self.rows:
            # self.matrix.at[row, 'total'] = self.matrix.loc[row].sum()
            # sum(distance(points[i], points[i+1]) for i in range(len(points) - 1))
            self.matrix.at[row, 'total'] = self.matrix.at[row, 'circle'] + self.matrix.at[row, 'rectangle'] + self.matrix.at[row, 'no_shape']
        for column in self.columns:
            self.matrix[column] = pd.to_numeric(self.matrix[column], errors='coerce')
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
                        self.matrix.at[row, 'accuracy'] = str(int(((self.matrix.at[row, 'truth'] - (self.matrix.at[row, 'rectangle'] + self.matrix.at[row, 'circle'])) / self.matrix.at[row, 'truth']) * 100)) + '%'
            else:
                self.matrix.at[row, 'accuracy'] = '-'  
    
    def get_ratio(self):
        if 'FC' in self.file_path:
            ratio = [59414,49756]
        elif 'FA' in self.file_path:
            ratio = [48484,26442]
        elif 'PN' in self.file_path:
            ratio = parse_ratio_from_inkml_file(self.file_path)
        return ratio
            
    
    def group_connections(self, shape_strokes, unrecognized_strokes):
        
        content = parse_strokes_from_inkml_file(self.file_path)
        ratio = self.get_ratio()
        converted_strokes = convert_coordinates(content, float(ratio[0]), float(ratio[1]))
        resampled_content = resample_strokes(converted_strokes)
        
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if shape_name == 'line':
                    self.matrix2.at['line', 'truth'] += 1
        
        edges = self._group_connections(shape_strokes, unrecognized_strokes)
        
        truth_contains_edge = False
        amount_of_lines = 0
        amount_of_edges = len(edges)
        
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if shape_name == 'line':
                    amount_of_lines += 1
        
        for edge in edges:
            print('edge: ', edge['valid']['line'])
            line_index = [resampled_content.index(edge['valid']['line']['stroke'])]
            for dictionary in self.truth:
                for shape_name, trace_ids in dictionary.items():
                    if shape_name == 'line' and set(line_index).issubset(set(trace_ids)):
                        # # get source strokes
                        # source_strokes = get_strokes_from_candidate(edge['valid']['line']['source'], content)
                        # # # get target strokes
                        # target_strokes = get_strokes_from_candidate(edge['valid']['line']['target'], content)
                        # # # plot source strokes
                        # plot_strokes_without_scala(source_strokes + target_strokes, edge['valid']['line']['stroke'])
                        # plot_strokes_without_scala(content)
                        truth_contains_edge = True
                        self.matrix2.at['line', 'line'] += 1   
                        
            if not truth_contains_edge and 'valid' in edge:
                # # zeige mir diesen case
                # # get source strokes
                # source_strokes = get_strokes_from_candidate(edge['valid']['line']['source'], content)
                # # get target strokes
                # target_strokes = get_strokes_from_candidate(edge['valid']['line']['target'], content)
                # # plot source strokes
                # # plot_strokes_without_scala(source_strokes + target_strokes, edge['valid']['line']['stroke'])
                # # plot_strokes_without_scala(content)
                self.matrix2.at['no_shape', 'line'] += 1
        # if amount_of_lines != amount_of_edges:
        #     # # zeige mir diesen case
        #     # # get source strokes
        #     source_strokes = get_strokes_from_candidate(edge['valid']['line']['source'], content)
        #     # # get target strokes
        #     target_strokes = get_strokes_from_candidate(edge['valid']['line']['target'], content)
        #     # # plot source strokes
        #     plot_strokes_without_scala(source_strokes + target_strokes, edge['valid']['line']['stroke'])
        #     # # plot_strokes_without_scala(content)
            

        
        return edges

        
                  
    def recognize(self, rejector, classifier, candidate, strokes):
        self.recognizer_calls += 1
        recognizer_result = self._recognize(rejector, classifier, candidate, strokes, self.truth)
        truth_contains_candidate = False
        for dictionary in self.truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate):  
                    self.valid_shapes += 1
                    truth_contains_candidate = True
                    if 'valid' in recognizer_result[0]:
                        shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
                        # if not shape_name == shape_name_recognizer_result:
                        #     print('shape not correctly recognized', self.file_path, shape_name_recognizer_result, candidate)
                        #     exit()
                        
                        self.matrix.at[shape_name, shape_name_recognizer_result] += 1
                    else:  
                        self.matrix.at[shape_name, 'no_shape'] += 1
        
        if not truth_contains_candidate and not 'valid' in recognizer_result[0]:
            self.matrix.at['no_shape', 'no_shape'] += 1
            
        elif not truth_contains_candidate and 'valid' in recognizer_result[0]:
            shape_name_recognizer_result = next(iter(recognizer_result[0]['valid']))
            self.matrix.at['no_shape', shape_name_recognizer_result] += 1
           
       
        return recognizer_result
        

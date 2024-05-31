from helper.parsers import parse_ground_truth
import numpy as np

class EvaluationWrapper:
    def __init__(self, is_a_shape:callable):
        self._is_a_shape = is_a_shape
        self.truth = None


    def __str__(self):
        return "member of Test"

    def setCurrentFilePath(self, file_path):
        self.truth = parse_ground_truth(file_path)
        self.shape_matrix = np.zeros((len(self.truth), len(self.truth)))

    
    def is_a_shape(self, candidate, content):
        print("is_a_shape")
        recognizer_result = self._is_a_shape(candidate, content)
        # prüfen ob der Kandidat einer shape in self.shapes entspricht
        # candidate_is_shape = False
        # if candidate in self.shapes:
        #     candidate_is_shape = True
        
        return recognizer_result
        

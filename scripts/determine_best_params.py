from helper.EvaluationWrapper import EvaluationWrapper
from recognizer.template_matching_recognizer import is_a_shape as template_matching_recognizer
import os

for i in range(53,90):
    for j in range(95, 110):
        evaluationWrapper = EvaluationWrapper(template_matching_recognizer)
        params = '6' + ',' + '50' + ',' +  str(i) + ',' + str(j)
        
        os.system("python ./main.py --file ./__datasets__/FC_1.0/no_text/FC_Validation.txt --save 'y' --params " + params)
        
        
        
        
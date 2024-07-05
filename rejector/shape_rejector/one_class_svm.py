
from classifier.shape_classifier.one_class_circle_svm import use as use_circle
from classifier.shape_classifier.one_class_rectangle_svm import use as use_rectangle


def use(X, candidate)-> dict:
    
    result_circle = use_circle(X, candidate)
    result_rectangle = use_rectangle(X, candidate)
    
    if 'invalid' in result_circle and 'invalid' in result_rectangle:
        return {'invalid': candidate}
    else:
        return {'valid': candidate}
    

    
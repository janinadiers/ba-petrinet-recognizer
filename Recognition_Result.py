import time

class RecognitionResult:
    def __init__(self):
        self.valid_shapes = []
        self.shapes = []
        self.correctly_rejected = 0
        self.incorrectly_not_rejected = 0
        self.incorrectly_not_recognized = 0
        self.correctly_recognized = 0
        self.runtimes = []
        self.recognizer_calls = 0
        self.confuse_circle_with_rectangle = 0
        self.confuse_rectangle_with_circle = 0
        self.amount_valid_shapes = 0
        self.amount_shape_candidates = 0
        
        self.confuse_circle_with_ellipse = 0
        self.confuse_circle_with_line = 0
        self.confuse_circle_with_diamond = 0
        self.confuse_circle_with_parallelogram = 0
        self.confuse_circle_with_circle_in_circle = 0
        
        self.confuse_rectangle_with_circle_in_circle = 0
        self.confuse_rectangle_with_ellipse = 0
        self.confuse_rectangle_with_line = 0
        self.confuse_rectangle_with_diamond = 0
        self.confuse_rectangle_with_parallelogram = 0
        

    def add_valid_shape(self, shape):
        self.valid_shapes.append(shape)
    
    def add_shape(self, shape):
        self.shapes.append(shape)
    
    def add_correctly_rejected(self):
        self.correctly_rejected += 1
    
    def add_correctly_recognized(self):
        self.correctly_recognized += 1
    
    def add_recognizer_call(self):
        self.recognizer_calls += 1
    
    def add_incorrectly_not_rejected(self):
        self.incorrectly_not_rejected += 1
        
    def get_shapes(self):
        return self.shapes
        
    def get_recognizer_calls(self):
        return self.recognizer_calls
    
    def get_valid_shapes(self):
        return self.valid_shapes
    
    def get_amount_valid_shapes(self):
        return self.amount_valid_shapes

    def get_amount_invalid_shape_candidates(self):
        return self.correctly_rejected + self.incorrectly_not_rejected
    
    def get_amount_correctly_recognized_shapes(self):
        return self.correctly_recognized
    
    def get_amount_correctly_rejected_shape_candidates(self):
        return self.correctly_rejected
    
    def get_amount_incorrectly_not_rejected_shapes(self):
        return self.incorrectly_not_rejected
    
    def get_amount_circle_confusion(self):
        return {'rectangle': self.confuse_circle_with_rectangle,
                'ellipse': self.confuse_circle_with_ellipse,
                'line': self.confuse_circle_with_line,
                'diamond': self.confuse_circle_with_diamond,
                'parallelogram': self.confuse_circle_with_parallelogram,
                'circle_in_circle': self.confuse_circle_with_circle_in_circle}
    
    def get_amount_shape_candidates(self):
        return self.amount_shape_candidates
    
    def get_amount_rectangle_confusion(self):
        return {'circle': self.confuse_rectangle_with_circle,
                'ellipse': self.confuse_rectangle_with_ellipse,
                'line': self.confuse_rectangle_with_line,
                'diamond': self.confuse_rectangle_with_diamond,
                'parallelogram': self.confuse_rectangle_with_parallelogram,
                'circle_in_circle': self.confuse_rectangle_with_circle_in_circle}
    
    
    def get_average_run_time(self) -> time:
        sum = 0
        for runtime in self.runtimes:
            sum += runtime
        return sum / len(self.runtimes)
    

    
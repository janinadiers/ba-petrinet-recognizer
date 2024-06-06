from helper.parsers import parse_ground_truth, parse_strokes_from_inkml_file
import os

class TrainWrapper:
    def __init__(self, files, recognizer):
        self.files = files
        self.truth = None
        self.recognizer = recognizer
        self.strokes = []
        
    def get_all_candidates_with_labels(self):
        file_paths = []
        truth = []
        for name_file_path in self.files:
            with open(name_file_path) as f:
                content = f.readlines()
                for line in content:
                    line = line.strip()
                    if line.endswith('.inkml'):
                        file_paths.append(os.path.dirname(name_file_path) + '/' + line)
        for path in file_paths:
            self.strokes.extend(parse_strokes_from_inkml_file(path))
            truth.append(parse_ground_truth(path))
        self.map_shapes_to_labels(truth)
        values = []
        labels = []
        label_mapping = {'rectangle': 0, 'circle': 1, 'line': 2, 'double circle': 2}
        for item in self.truth:
            for key, value in item.items():
                values.append(value)  # Add values to the list
                labels.append(label_mapping[key])
        return values, labels
            
    
    def map_shapes_to_labels(self, truth):
        
        flattened_truth = [item for sublist in truth for item in sublist]

        for entry in flattened_truth:
            if 'parallelogram' in entry:
                entry['rectangle'] = entry.pop('parallelogram')
            if 'diamond' in entry:
                entry['rectangle'] = entry.pop('diamond')
            if 'ellipse' in entry:
                entry['circle'] = entry.pop('ellipse')
        self.truth = flattened_truth
    
    def train_recognizer(self):
        values, labels = self.get_all_candidates_with_labels()

        print('Training recognizer...')
       
        self.recognizer.train(values, labels, self.strokes)
        

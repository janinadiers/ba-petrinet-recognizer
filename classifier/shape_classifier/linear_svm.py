
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from helper.features import compute_convex_hull_perimeter_to_area_ratio, compute_convex_hull_area_to_perimeter_ratio,compute_total_stroke_length_to_diagonal_length, calculate_average_min_distance
from helper.utils import combine_strokes, get_perfect_mock_shape
import joblib
import datetime
from helper.generate_feature_grids import generate_feature_images
from helper.features import get_feature_vector
from helper.parsers import parse_ground_truth, parse_strokes_from_inkml_file


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
        if 'ellipse' in entry:
            entry['circle'] = entry.pop('ellipse')
    self.truth = flattened_truth
    

def train(candidates, labels, strokes):
    # Bildung der Feature Vectors aus den Candidates
    X = []  # Features

    for candidate in candidates:
        stroke = combine_strokes(candidate, strokes)
        features = get_feature_vector(stroke)
        # add stroke amount and points amount
        features.append(len(candidate))
        features.append(len(stroke))
        X.append(features)
        
    X = np.array(X)
    y = np.array(labels)  # Corresponding labels (0: Rectangle, 1: Circle, 2: no shape)
   
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    
    # Generate a unique filename with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save the model
    joblib_file = f"svm_model_{timestamp}.joblib"
    joblib.dump(clf, joblib_file)


def use(grouped_ids:list[int], strokes:list[dict])-> dict:
    generate_feature_images(grouped_ids, strokes)
    return {'valid': {'rectangle': grouped_ids}}
    # X = []  # Features
    # stroke = combine_strokes(grouped_ids, strokes)
    # if len(stroke) < 10:
    #     return {'invalid': grouped_ids}
    # features = extract_features(stroke)
    # if len(features) == 0:
    #     return {'invalid': grouped_ids}
    # features.append(len(grouped_ids))
    # features.append(len(stroke))
    # X.append(features)
    # X = np.array(X)
    # # get the right model
    # joblib_file = "svm_model_20240606_121740.joblib"
    # # Load the model
    # loaded_clf = joblib.load(joblib_file)
    # predicted_label = loaded_clf.predict(X)
    # if predicted_label == 0:
    #     return {'valid': {'rectangle': grouped_ids}}
    # elif predicted_label == 1:
    #     return {'valid': {'circle': grouped_ids}}
    # else:
    #     return {'invalid': grouped_ids}
    

# # Extract and visualize orientation features for the first candidate
# orientation_features = [compute_orientation_feature([candidates[0]], angle) for angle in [0, 45, 90, 135]]

# # Plot the feature images
# fig, axes = plt.subplots(1, 4, figsize=(12, 3))
# for ax, feature, angle in zip(axes, orientation_features, [0, 45, 90, 135]):
#     ax.imshow(feature, cmap='hot', interpolation='nearest')
#     ax.set_title(f'Orientation {angle}°')
# plt.show()




# # Split dataset into training set and test set
# X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, test_size=0.3,random_state=109) # 70% training and 30% test

# #Create a svm Classifier
# clf = svm.SVC(kernel='linear') # Linear Kernel

# #Train the model using the training sets
# clf.fit(X_train, y_train)

# #Predict the response for test dataset
# y_pred = clf.predict(X_test)

# # Model Accuracy: how often is the classifier correct?
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
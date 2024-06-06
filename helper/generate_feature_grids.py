import numpy as np
import math

# Funktion zur Berechnung der Ähnlichkeit eines Punktes mit einem Referenzwinkel
def compute_orientation_similarity(point, angle):
    radians = math.radians(angle)
    reference_vector = np.array([math.cos(radians), math.sin(radians)])
    vector = np.array([point['x'], point['y']])
    similarity = np.dot(vector, reference_vector) / (np.linalg.norm(vector) * np.linalg.norm(reference_vector))
    similarity = max(0, min(1, similarity))  # Begrenzen auf [0, 1]
    return similarity

# Funktion zur Erstellung eines Orientierungs-Feature-Images
def compute_orientation_feature(stroke, angle):
    feature_image = np.zeros((24, 24))
    for point in stroke:
        similarity = compute_orientation_similarity(point, angle)
        grid_x = min(int(point['x'] // (24 / 24)), 23)
        grid_y = min(int(point['y'] // (24 / 24)), 23)
        feature_image[grid_y, grid_x] = max(feature_image[grid_y, grid_x], similarity)
    return feature_image

# Funktion zur Erstellung eines Endpunkt-Feature-Images
def compute_endpoint_feature(strokes):
    feature_image = np.zeros((24, 24))
    start_point = strokes[0]
    end_point = strokes[-1]
    grid_x_start = min(int(start_point['x'] // (24 / 24)), 23)
    grid_y_start = min(int(start_point['y'] // (24 / 24)), 23)
    grid_x_end = min(int(end_point['x'] // (24 / 24)), 23)
    grid_y_end = min(int(end_point['y'] // (24 / 24)), 23)
    print(grid_x_start, grid_y_start, grid_x_end, grid_y_end)
    feature_image[grid_y_start, grid_x_start] = 1
    feature_image[grid_y_end, grid_x_end] = 1
            
    return feature_image

# Funktion zur Erstellung der Feature-Images für einen Kandidaten
def generate_feature_images(candidate, strokes):
    feature_images = []
    combined_strokes = combine_strokes(candidate, strokes)
    orientations = [0, 45, 90, 135]
    for angle in orientations:
        feature_image = compute_orientation_feature(combined_strokes, angle)
        feature_images.append(feature_image)
    endpoint_image = compute_endpoint_feature(combined_strokes)
    feature_images.append(endpoint_image)
    # print(feature_images)
    return feature_images

# Dummy-Funktion zum Kombinieren der Striche eines Kandidaten
def combine_strokes(candidate, strokes):
    combined = []
    for idx in candidate:
        combined.extend(strokes[idx])
    return combined

# Beispielhafte Verwendung
candidates = [
    [0, 1], [2, 3]
]
strokes = [
    [{'x': 1, 'y': 2}, {'x': 2, 'y': 3}], 
    [{'x': 2, 'y': 4}, {'x': 3, 'y': 5}], 
    [{'x': 3, 'y': 6}, {'x': 4, 'y': 7}], 
    [{'x': 4, 'y': 8}, {'x': 5, 'y': 9}]
]

# Generiere Feature-Images für jeden Kandidaten
# for candidate in candidates:
#     feature_images = generate_feature_images(candidate, strokes)
#     for idx, img in enumerate(feature_images):
#         print(f"Feature Image {idx+1} for candidate {candidate}:\n{img}")

# Vergleich mit Template-Images würde hier folgen (nicht implementiert)


import numpy as np
import copy

def calculate_vector(p1, p2):
    """ Calculate the directional vector from point p1 to p2 """
    return np.array([p2['x'] - p1['x'], p2['y'] - p1['y']])

    
def normalize_vector(v):
    """ Normalize a vector to unit length """
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

def get_first_and_last_segment_of_stroke(stroke, corners):
    first_point = stroke[0]
    first_corner = stroke[corners[0]]
    last_corner = stroke[corners[-1]]
    last_point = stroke[-1]
    first_segment = [first_point, first_corner]
    last_segment = [last_corner, last_point]
    return first_segment, last_segment

def detect_corners_within_stroke(points, upper_bound_angle, lower_bound_angle):
    """ Detect corners in a list of points within a stroke and return indices of corner points """
    vectors = []
    corner_indices = []  # Start by considering the first point as a potential corner

    for i in range(1, len(points)):
       
        v = calculate_vector(points[i-1], points[i])
        vectors.append(normalize_vector(v))

    for i in range(1, len(vectors)):
        angle = angle_between(vectors[i-1], vectors[i])
        if lower_bound_angle <= angle <= upper_bound_angle:
            corner_indices.append(i)  # Append the index of the corner

    # corner_indices.append(len(points) - 1)  # Consider the last point as a potential corner
    return corner_indices

def detect_corners(strokes, upper_bound_angle = 120, lower_bound_angle = 54):
    """ Detect corners across multiple strokes, considering corners within strokes and between strokes """
    total_corners = 0
    detected_corners = []
    segments = []
    vectors = []
    counter = 0
    _strokes = copy.deepcopy(strokes)
    for stroke in _strokes:
        corner_indices = detect_corners_within_stroke(stroke, upper_bound_angle, lower_bound_angle)
        if len(corner_indices) > 0:
            total_corners += len(corner_indices)
            for corner_index in corner_indices:
                detected_corners.append(stroke[corner_index])
            first_segment, last_segment = get_first_and_last_segment_of_stroke(stroke, corner_indices)
            segments.append(first_segment)
            segments.append(last_segment)
            vectors.append(normalize_vector(calculate_vector(first_segment[0], first_segment[1])))
            vectors.append(normalize_vector(calculate_vector(last_segment[0], last_segment[1])))
           
        else:
            vectors.append(normalize_vector(calculate_vector(stroke[0], stroke[-1])))
            segments.append([stroke[0], stroke[-1]])
        counter += 1
    for i in range(1, len(vectors)):
        angle = angle_between(vectors[i-1], vectors[i])
        
        if lower_bound_angle <= angle <= upper_bound_angle:
            # print('detected corner between strokes', segments[i][0], i)
            if not segments[i][0] in detected_corners:
                total_corners += 1
                detected_corners.append(segments[i][0])
    angle = angle_between(vectors[-1], vectors[0])
    if lower_bound_angle <= angle <= upper_bound_angle:
        if not segments[0][0] in detected_corners:
            total_corners += 1
            detected_corners.append(segments[0][0])
    return total_corners # Total corners include intra and inter stroke corners

def angle_between(v1, v2):
    """ Calculate the angle in degrees between vectors 'v1' and 'v2' using dot product and arccos """
    v1_u = normalize_vector(v1)
    v2_u = normalize_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return np.degrees(angle)
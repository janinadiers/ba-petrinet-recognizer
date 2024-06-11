
import numpy as np

def calculate_vector(p1, p2):
    """ Calculate the directional vector from point p1 to p2 """
    return np.array([p2['x'] - p1['x'], p2['y'] - p1['y']])

    
def normalize_vector(v):
    """ Normalize a vector to unit length """
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v


def detect_corners(stroke, lower_bound_angle = 80, upper_bound_angle = 100):
    """ Detect corners in a list of points within a stroke and return indices of corner points """
    vectors = []
    amount_of_corners = 0 
   
    for i in range(1, len(stroke)):
        v = calculate_vector(stroke[i-1], stroke[i])
        vectors.append(v)
    
    for i in range(1, len(vectors)):
        angle = angle_between(vectors[i-1], vectors[i])
        if angle > lower_bound_angle and angle < upper_bound_angle:
            amount_of_corners += 1
    
    angle = angle_between(vectors[-1], vectors[0])
    if angle > lower_bound_angle and angle < upper_bound_angle:
        amount_of_corners += 1
    print(f'Amount of corners: {amount_of_corners}')
    return amount_of_corners

def angle_between(v1, v2):
    """ Calculate the angle in degrees between vectors 'v1' and 'v2' using dot product and arccos """
    v1_u = normalize_vector(v1)
    v2_u = normalize_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return np.degrees(angle)

def find_x_distribution(points):
    x_values = [point['x'] for point in points]
    # get the distribution of x values
    return np.histogram(x_values, bins=10, range=(0, 1000))
    
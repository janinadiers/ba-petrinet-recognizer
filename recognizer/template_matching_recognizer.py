from helper.export_strokes_to_inkml import export_strokes_to_inkml
import numpy as np


def is_a_shape(grouped_ids:list[int], strokes:list[dict], params=None) -> dict:
    
    stroke = combine_strokes(grouped_ids, strokes)
    if params is None:
        params = (50, 6, 54, 120)
    else:
        params = params
        
    if len(stroke) < params[0]:
        return {'invalid': grouped_ids}
    # stroke = remove_outliers(stroke) 
    perfect_mock_shape = get_perfect_mock_shape(stroke)
    perfect_circle = perfect_mock_shape['circle']
    perfect_rect = perfect_mock_shape['rectangle']
    if perfect_mock_shape['bounding_box']['width'] == 0 or perfect_mock_shape['bounding_box']['height'] == 0:
        return {'invalid': grouped_ids}
    if ((perfect_mock_shape['bounding_box']['width'] / perfect_mock_shape['bounding_box']['height']) > params[1]) or ((perfect_mock_shape['bounding_box']['height'] / perfect_mock_shape['bounding_box']['width']) > params[1]):
        return {'invalid': grouped_ids}
    
    density = calculate_total_stroke_length(stroke) / calculate_diagonal_length(get_bounding_box(stroke))
    if  density < 2 or density > 5:
        return {'invalid': grouped_ids}
    
    
    average_distance_circle = calculate_average_min_distance(perfect_circle, stroke)
    average_distance_rect = calculate_average_min_distance(perfect_rect, stroke)
    
    if average_distance_circle <= 500 or average_distance_rect <= 500:
        strokes = [strokes[trace_id] for trace_id in grouped_ids]
        corners = detect_corners(strokes, params[3], params[2])
        if corners == 0:
            return {'valid': {'circle': grouped_ids}}
        else:
            return {'valid': {'rectangle': grouped_ids}}
    else:
        return {'invalid': grouped_ids}
  
    
 
def export_to_inkml(grouped_ids, strokes, perfect_rect, perfect_circle):
    recognized_strokes = [strokes[trace_id] for trace_id in grouped_ids]
    export_strokes_to_inkml([perfect_rect, perfect_circle] + recognized_strokes, str(grouped_ids[0]) + '_perfect_mock_shape.inkml')

def calculate_average_min_distance(ideal_shape, candidate):
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_shape_arr = np.array([[point['x'], point['y']] for point in ideal_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in candidate])
    
    # Calculate pairwise distances between all points in ideal_shape and candidate
    # np.newaxis increases the dimension where applied, making the array broadcasting possible
    distances = np.sqrt(((ideal_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    # Find the minimum distance for each point in ideal_shape to any point in candidate
    min_distances = np.min(distances, axis=1)
    
    # Calculate the average of these minimum distances
    average_min_distance = np.mean(min_distances)
    
    return average_min_distance

def calculate_total_stroke_length(stroke):
    total_length = 0
    for i in range(1, len(stroke)):
        total_length += np.sqrt((stroke[i]['x'] - stroke[i-1]['x'])**2 + (stroke[i]['y'] - stroke[i-1]['y'])**2)
    return total_length

def calculate_diagonal_length(bounding_box):
    min_x, max_x, min_y, max_y = bounding_box
    return np.sqrt((max_x - min_x)**2 + (max_y - min_y)**2)


def calculate_vector(p1, p2):
    """ Calculate the directional vector from point p1 to p2 """
    return np.array([p2['x'] - p1['x'], p2['y'] - p1['y']])

def normalize_vector(v):
    """ Normalize a vector to unit length """
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

def angle_between(v1, v2):
    """ Calculate the angle in degrees between vectors 'v1' and 'v2' using dot product and arccos """
    v1_u = normalize_vector(v1)
    v2_u = normalize_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return np.degrees(angle)

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
    for stroke in strokes:
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


def get_first_and_last_segment_of_stroke(stroke, corners):
    first_point = stroke[0]
    first_corner = stroke[corners[0]]
    last_corner = stroke[corners[-1]]
    last_point = stroke[-1]
    first_segment = [first_point, first_corner]
    last_segment = [last_corner, last_point]
    return first_segment, last_segment

def get_bounding_box(stroke:list[dict]):
    # get the bounding box of the grouped strokes
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for point in stroke:
        
        x = point['x']
        y = point['y']
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    return min_x, max_x, min_y, max_y

def combine_strokes(grouped_ids:list[int], strokes:list[dict]):
    combined_strokes = []  
    for stroke_id in grouped_ids:
        stroke = strokes[stroke_id]
        combined_strokes += stroke
    return combined_strokes
     


def get_perfect_mock_shape(stroke:list[dict]) -> dict:
    
    bounding_box = get_bounding_box(stroke)
    # get the bounding box of the grouped strokes
    min_x, max_x, min_y, max_y = bounding_box
    # create the perfect mock shape
    perfect_mock_shape = []
    # add the top left point
    perfect_mock_shape.append({'x': min_x, 'y': min_y})
    # add the top right point
    perfect_mock_shape.append({'x': max_x, 'y': min_y})
    # add the bottom right point
    perfect_mock_shape.append({'x': max_x, 'y': max_y})
    # add the bottom left point
    perfect_mock_shape.append({'x': min_x, 'y': max_y})
    
    perfect_mock_shape.append({'x': min_x, 'y': min_y})
 
    # resampled_mock_shape = resample(perfect_mock_shape, 32)
    perfect_mock_rect = get_rectangle_with_points(bounding_box, 32)
    # get center of mass
    center_of_mass_x = (min_x + max_x) / 2
    center_of_mass_y = (min_y + max_y) / 2
    
    radius = min((max_x - min_x) / 2, (max_y - min_y) / 2)
    perfect_cyclic_mock_shape = get_circle_with_points(center_of_mass_x, center_of_mass_y, radius, 32)
    

    return {'rectangle': perfect_mock_rect, 'circle': perfect_cyclic_mock_shape, 'bounding_box': {'min_x':min_x, 'min_y': min_y, 'width': max_x - min_x, 'height': max_y - min_y}}
    

def remove_outliers(stroke:list[dict]):
    new_stroke = []

    sorted_points = list(stroke)
    # # Calculate the number of points to retain
    retain_count = round(0.9 * len(stroke))
    remove_count = len(stroke) - retain_count
        
    remove_each_end = int(remove_count / 2)  # Use integer division for slicing
    if remove_each_end == 0:
        return stroke
    # # Sort and slice based on 'x'
    sorted_points.sort(key=lambda point: point['x'])
    sorted_points = sorted_points[remove_each_end:-remove_each_end]
    # # Sort and slice based on 'y'
    sorted_points.sort(key=lambda point: point['y'])
    sorted_points = sorted_points[remove_each_end:-remove_each_end]
    # # Filter the original points list to only include those that remain in sorted_points
    new_stroke.append([point for point in stroke if point in sorted_points])
    if len(new_stroke[0]) == 0:
        pass

    return new_stroke[0]

def get_circle_with_points(cx, cy, radius, num_points):
    
    # Winkelabstand zwischen den Punkten
    angle_step = 2 * np.pi / num_points
    
    # Punkte auf dem Kreis berechnen
    points = [{'x': cx + radius * np.cos(i * angle_step), 'y': cy + radius * np.sin(i * angle_step)} for i in range(num_points)]
    return points + [points[0]]

def get_rectangle_with_points(bounding_box, num_points):
    min_x, max_x, min_y, max_y = bounding_box
    width = abs(max_x - min_x)
    height = abs(max_y - min_y)
    # Total perimeter
    perimeter = 2 * (width + height)
    
    if perimeter == 0:
        perimeter = 1
        
    # Use rounding to allocate points more accurately
    top_points_count = max(round((width / perimeter) * num_points),1)
    bottom_points_count = top_points_count
    left_points_count = max(round((height / perimeter) * num_points),1)
    right_points_count = left_points_count
    # Generate points for each side
    top_points = [{'x': min_x + i * width / (top_points_count), 'y': min_y} for i in range(top_points_count)]
    right_points = [{'x': max_x, 'y': min_y + i * height / (right_points_count )} for i in range(right_points_count)]
    bottom_points = [{'x': max_x - i * width / (bottom_points_count), 'y': max_y} for i in range(bottom_points_count)]
    left_points = [{'x': min_x, 'y': max_y - i * height / (left_points_count)} for i in range(left_points_count)]
     # Return the list of points. Remove last point of each side to avoid duplications at the corners
    points = top_points + right_points + bottom_points + left_points
    
    
    return points + [points[0]]
    






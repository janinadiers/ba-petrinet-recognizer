from export_strokes_to_inkml import export_strokes_to_inkml
import numpy as np


def is_a_shape(grouped_ids:list[int], expected_shapes:list[dict], strokes:list[dict]) -> dict:
    stroke = combine_strokes(grouped_ids, strokes)
    stroke = remove_outliers(stroke) 
    
    perfect_circle = get_perfect_mock_shape(stroke)['circle']
    perfect_rect = get_perfect_mock_shape(stroke)['rectangle']
    
    average_distance_circle = calculate_average_min_distance(perfect_circle, stroke)
    average_distance_rect = calculate_average_min_distance(perfect_rect, stroke)
    for dictionary in expected_shapes:
        for shape_name, trace_ids in dictionary.items():
            if set(trace_ids) == set(grouped_ids) and (shape_name == 'circle' or shape_name == 'rectangle'):
                export_to_inkml(stroke, perfect_rect, perfect_circle, grouped_ids[0])
                if average_distance_circle < average_distance_rect:
                    print('als Kreis erkannt')
                    if not shape_name == 'circle':
                        print(grouped_ids[0])
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!aber falsch erkannt')
                    return {'valid': {'circle': grouped_ids}}
                else:
                    print('als Rechteck erkannt')
                    if not shape_name == 'rectangle':
                        print(grouped_ids[0])
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!aber falsch erkannt')
                    return {'valid': {'rectangle': grouped_ids}}
                     
    return {'invalid': grouped_ids}     
    
 
def export_to_inkml(stroke, perfect_rect, perfect_circle, id):
    export_strokes_to_inkml([perfect_rect, perfect_circle, stroke], str(id) + '_perfect_mock_shape.inkml')

def calculate_average_min_distance(ideal_shape, candidate):
    # print('candidate: ', candidate)
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_shape_arr = np.array([[point['x'], point['y']] for point in ideal_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in candidate])
    
    # Calculate pairwise distances between all points in ideal_shape and candidate
    # np.newaxis increases the dimension where applied, making the array broadcasting possible
    distances = np.sqrt(((ideal_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    print('distances: ', distances)
    # Find the minimum distance for each point in ideal_shape to any point in candidate
    min_distances = np.min(distances, axis=1)
    
    # Calculate the average of these minimum distances
    average_min_distance = np.mean(min_distances)
    
    return average_min_distance
    
    
def get_bounding_box(stroke:list[dict]):
    # get the bounding box of the grouped strokes
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    print('stroke: ', stroke)
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
    

    return {'rectangle': perfect_mock_rect, 'circle': perfect_cyclic_mock_shape}
    

def remove_outliers(stroke:list[dict]):
    new_stroke = []

    sorted_points = list(stroke)
    # # Calculate the number of points to retain
    retain_count = round(0.9 * len(stroke))
    remove_count = len(stroke) - retain_count
        
    remove_each_end = int(remove_count / 2)  # Use integer division for slicing
    # # Sort and slice based on 'x'
    sorted_points.sort(key=lambda point: point['x'])
    sorted_points = sorted_points[remove_each_end:-remove_each_end]
    # # Sort and slice based on 'y'
    sorted_points.sort(key=lambda point: point['y'])
    sorted_points = sorted_points[remove_each_end:-remove_each_end]
    # # Filter the original points list to only include those that remain in sorted_points
    new_stroke.append([point for point in stroke if point in sorted_points])
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
    






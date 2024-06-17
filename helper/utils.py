import numpy as np
import copy
from helper.normalizer import distance
from helper.normalizer import normalize
import matplotlib.pyplot as plt

def combine_strokes(grouped_ids:list[int], strokes:list[dict]):
    combined_strokes = []  
    for stroke_id in grouped_ids:
        stroke = strokes[stroke_id]
        combined_strokes += stroke
    return combined_strokes
        

def get_bounding_box(stroke:list[dict]):
    _stroke = copy.deepcopy(stroke)
    # get the bounding box of the grouped strokes
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for point in _stroke:
        
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
    width = max_x - min_x
    height = max_y - min_y
    return min_x, max_x, min_y, max_y, width, height


def calculate_diagonal_length(bounding_box):
    min_x, max_x, min_y, max_y, width, height = bounding_box
    return np.sqrt((max_x - min_x)**2 + (max_y - min_y)**2)
    
def calculate_total_stroke_length(stroke):
    _stroke = copy.deepcopy(stroke)
    total_length = 0
    for i in range(1, len(_stroke)):
        total_length += np.sqrt((_stroke[i]['x'] - _stroke[i-1]['x'])**2 + (_stroke[i]['y'] - _stroke[i-1]['y'])**2)
    
    total_length += np.sqrt((_stroke[-1]['x'] - _stroke[0]['x'])**2 + (_stroke[-1]['y'] - _stroke[0]['y'])**2)
    return total_length


def get_perfect_mock_shape(stroke:list[dict]) -> dict:
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    # get the bounding box of the grouped strokes
    min_x, max_x, min_y, max_y, width, height = bounding_box
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
    

def get_rectangle_shape_with_vertical_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    min_x, max_x, min_y, max_y, width, height = bounding_box
    
    rectangle_with_points = get_rectangle_with_points(bounding_box, 68)
    vertical_lines = []
    vertical_lines.append([point for point in rectangle_with_points if point['x'] == min_x])
    vertical_lines.append([point for point in rectangle_with_points if point['x'] == max_x])

    plot_strokes(vertical_lines)
    return vertical_lines
    
def get_rectangle_shape_with_horizontal_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    min_x, max_x, min_y, max_y, width, height = bounding_box
    rectangle_with_points = get_rectangle_with_points(bounding_box, 68)
    horizontal_lines = []
    horizontal_lines.append([point for point in rectangle_with_points if point['y'] == min_y])
    horizontal_lines.append([point for point in rectangle_with_points if point['y'] == max_y])

    # plot_strokes(horizontal_lines)
    return horizontal_lines
    
         
def get_circle_with_points(cx, cy, radius, num_points):
    # Winkelabstand zwischen den Punkten
    angle_step = 2 * np.pi / num_points

    # Punkte auf dem Kreis berechnen
    points = [{'x': cx + radius * np.cos(i * angle_step), 'y': cy + radius * np.sin(i * angle_step)} for i in range(num_points)]
    return points + [points[0]]

def get_rectangle_with_points(bounding_box, num_points):
    min_x, max_x, min_y, max_y, width, height = bounding_box
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




# Function to find the closest stroke to the given end point
def find_closest_stroke(end_point, strokes):
    min_distance = float('inf')
    closest_stroke = None
    closest_index = -1
    for i, stroke in enumerate(strokes):
        start_point = stroke[0]
        dist = distance(end_point, start_point)
        if dist < min_distance:
            min_distance = dist
            closest_stroke = stroke
            closest_index = i
    return closest_stroke, closest_index



def order_strokes(strokes):
    _strokes = copy.deepcopy(strokes)
    if not _strokes:
        return []

    ordered_strokes = [_strokes.pop(0)]  # Start with the first stroke
    while _strokes:
        current_end_point = ordered_strokes[-1][-1]  # End point of the current stroke
        closest_stroke, closest_index = find_closest_stroke(current_end_point, _strokes)
        ordered_strokes.append(closest_stroke)
        _strokes.pop(closest_index)
    return ordered_strokes
 

def get_vertical_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    min_x, max_x, min_y, max_y, width, height = bounding_box
    left_vertical_line = []
    right_vertical_line = []
    vertical_lines = []
    for i in range(0, 16):
        y = min_y + i * height / 15
        left_vertical_line.append({'x': min_x, 'y': y})
        right_vertical_line.append({'x': max_x, 'y': y})
    vertical_lines.append(left_vertical_line)
    vertical_lines.append(right_vertical_line)
    # vertical_lines.append(stroke)
    # plot_strokes(vertical_lines)
    return [left_vertical_line, right_vertical_line]

def get_horizontal_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    min_x, max_x, min_y, max_y, width, height = bounding_box
    top_horizontal_line = []
    bottom_horizontal_line = []
    horizontal_lines = []
    for i in range(0, 16):
        x = min_x + i * width / 15
        top_horizontal_line.append({'x': x, 'y': min_y})
        bottom_horizontal_line.append({'x': x, 'y': max_y})
    horizontal_lines.append(top_horizontal_line)
    horizontal_lines.append(bottom_horizontal_line)
    # horizontal_lines.append(stroke)
    # plot_strokes(horizontal_lines)
    return [top_horizontal_line, bottom_horizontal_line]

# def remove_outliers(stroke:list[dict]):
#     new_stroke = []

#     sorted_points = list(stroke)
#     # # Calculate the number of points to retain
#     retain_count = round(0.9 * len(stroke))
#     remove_count = len(stroke) - retain_count
        
#     remove_each_end = int(remove_count / 2)  # Use integer division for slicing
#     if remove_each_end == 0:
#         return stroke
#     # # Sort and slice based on 'x'
#     sorted_points.sort(key=lambda point: point['x'])
#     sorted_points = sorted_points[remove_each_end:-remove_each_end]
#     # # Sort and slice based on 'y'
#     sorted_points.sort(key=lambda point: point['y'])
#     sorted_points = sorted_points[remove_each_end:-remove_each_end]
#     # # Filter the original points list to only include those that remain in sorted_points
#     new_stroke.append([point for point in stroke if point in sorted_points])
#     if len(new_stroke[0]) == 0:
#         pass

#     return new_stroke[0]

# Function to plot strokes correctly
def plot_strokes(strokes):
    plt.figure(figsize=(8, 8))
    print('strokes', len(strokes))
    for stroke in strokes:
        print('stroke', stroke)
        _points = [(point['x'], point['y']) for point in stroke]  # Extract points for the current stroke
        x, y = zip(*_points)  # Unpack the stroke into x and y coordinates
        plt.plot(x, y, marker='o', linestyle='-', color='b')  # Plot the stroke
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Strokes Visualization')
    plt.grid(True)
    plt.show()
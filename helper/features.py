
from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length, plot_strokes
import numpy as np
import copy
from helper.utils import get_perfect_mock_shape, order_strokes,get_horizontal_lines, get_vertical_lines, stroke_has_only_duplicates
from shapely.geometry import Polygon, LineString
from helper.normalizer import distance, translate_to_origin, scale



def get_aspect_ratio(stroke):
    bounding_box = get_bounding_box(stroke)
    width = bounding_box[4]
    height = bounding_box[5]
    return width / height


def get_number_of_convex_hull_vertices(stroke):
    _stroke = copy.deepcopy(stroke)
    points = [(point['x'], point['y']) for point in _stroke]
    try:
        hull = ConvexHull(points)
       
        return len(hull.vertices)
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
    

def get_convexity(strokes):
    # Flatten the list of strokes into a list of points
    points = np.array([(point['x'], point['y']) for stroke in strokes for point in stroke])
    
    # Create a LineString from the points to calculate the perimeter
    linestring = LineString(points)
    shape_perimeter = linestring.length
    
    # Compute the convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    
    # Create a Polygon from the hull points to calculate the convex hull perimeter
    hull_polygon = Polygon(hull_points)
    hull_perimeter = hull_polygon.length
    
    # Calculate convexity
    convexity = hull_perimeter / shape_perimeter
    
    return convexity

def compute_convex_hull(points):
    hull = ConvexHull(points)
    return hull

def calculate_concavity(stroke):
    points = np.array([(point['x'], point['y']) for point in stroke])
    polygon = Polygon(points)
    hull = compute_convex_hull(points)
    hull_polygon = Polygon(points[hull.vertices])
    
    shape_area = polygon.area
    hull_area = hull_polygon.area
    
    concavity_area = hull_area - shape_area
    concavity_index = concavity_area / hull_area if hull_area != 0 else 0
    
    return concavity_index


def is_closed_shape(stroke, edge_point_positions=None):
    _stroke = copy.deepcopy(stroke)
    edge_points = []
    for edge_point_position in edge_point_positions:
        edge_points.append(_stroke[edge_point_position])
    min_distances = []
    for template_point in edge_points:
        distances = []
        for point2 in edge_points:
            if template_point == point2:
                continue
            distances.append(distance(template_point, point2))
        min_distances.append(min(distances))
        
    # return np.mean(min_distances)
    return max(min_distances)

# compactness ratio: 
# Circles: For a perfect circle, the ratio of area to perimeter (compactness) is maximized, because circles have the highest area for a given perimeter compared to other shapes. This makes the compactness ratio close to that of a circle.
# Rectangles and Other Polygons: Shapes like rectangles, especially elongated ones, have a lower compactness ratio compared to circles. This is because they have more perimeter for the same area compared to a circle.
def compute_convex_hull_perimeter_to_area_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    try:
        hull = ConvexHull(_points)
        hull_area = hull.volume  # For 2D, volume is the area
        hull_perimeter = hull.area  # For 2D, area is the perimeter
        return hull_perimeter / hull_area
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
        
    
def compute_convex_hull_area_to_perimeter_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    
    try:
        hull = ConvexHull(_points)
        hull_area = hull.volume  # For 2D, volume is the area
        hull_perimeter = hull.area  # For 2D, area is the perimeter
        return hull_area / hull_perimeter
    except Exception as e:
        raise Exception("Convex hull could not be computed.")
  

    
def compute_total_stroke_length_to_diagonal_length(stroke):
    _stroke = copy.deepcopy(stroke)
    diagonal_length = calculate_diagonal_length(get_bounding_box(_stroke))
    total_stroke_length = calculate_total_stroke_length(_stroke)
    
    return total_stroke_length / diagonal_length


# def calculate_average_distance_to_template_shape_with_horizontal_lines(stroke, edge_point_positions):
#     # strokes = []
#     # print('edge_point_positions', edge_point_positions)
#     # for i in range(0, len(edge_point_positions)-1):
#     #     strokes.append(stroke[edge_point_positions[i]:edge_point_positions[i+1]])
#     # print('len strokes', len(strokes)) 
#     _stroke = copy.deepcopy(stroke)    
#     horizontal_lines_template = get_horizontal_lines(_stroke)
#     # plot_strokes(strokes)
#     # calculate the average distance of each point to the template shape
#     distances = []
#     closest_points = []
#     points_to_plot = []
#     for template_stroke in horizontal_lines_template:
#         for idx,template_point in enumerate(template_stroke):
#             # print('template_point', template_point)

#             min_distance = float('inf')
#             # print('next point', template_point)
#             # for stroke in strokes:
#             #     print('loop 2 durch strokes')
#             print(len(_stroke))
#             for j in range(len(_stroke) -1):
#                 point_pair = (stroke[j], stroke[j+1])
#                 print(stroke[j], stroke[j+1])
#                 # print('point_pair', point_pair, template_point, distance(template_point, point_pair[0]), distance(template_point, point_pair[1]))
#                 if template_point['x'] >= point_pair[0]['x'] and template_point['x'] <= point_pair[1]['x']:
#                     eucl_distance_1 = distance(template_point, point_pair[0])
#                     eucl_distance_2 = distance(template_point, point_pair[1])
#                     new_min_distance = min(eucl_distance_1, eucl_distance_2)
#                     # print('new_min_distance', new_min_distance)
#                     if new_min_distance < min_distance:
#                         if eucl_distance_1 < eucl_distance_2:
#                             min_distance = eucl_distance_1
#                             if len(closest_points)-1 < idx:
#                                 closest_points.insert(idx, point_pair[0])
#                             else:
#                                 closest_points[idx] = point_pair[0]
#                         else:
#                             min_distance = eucl_distance_2
#                             if len(closest_points)-1 < idx:
#                                 closest_points.insert(idx, point_pair[1])
#                             else:
#                                 closest_points[idx] = point_pair[1]
                        
                    
#             if min_distance == float('inf'):
#                 distances.append(1)
#             else:
#                 distances.append(min_distance)
#         points_to_plot.extend(closest_points)
#         closest_points = []
#     # print('hihfsjk', distances[:16], distances[16:32])

#     print(np.median(distances))
#     # if np.median(distances) < 0.1:                        
#     horizontal_lines_template.extend([stroke])
    
#     plot_strokes(horizontal_lines_template, points_to_plot )
#     return np.median(distances)

def calculate_average_distance_to_template_shape_with_vertical_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    vertical_lines_template = get_vertical_lines(stroke)
    distances = []
    points_to_plot = []
    print(len(_stroke))

    for template_stroke in vertical_lines_template:
        for template_point in template_stroke:
            min_distance = float('inf')
            closest_point = None
            
            for j in range(len(_stroke) - 1):
                point_pair = (_stroke[j], _stroke[j+1])
                
                if point_pair[0]['y'] <= template_point['y'] <= point_pair[1]['y']:
                    # Calculate distances to the segment endpoints
                    dist_to_p0 = distance(template_point, point_pair[0])
                    dist_to_p1 = distance(template_point, point_pair[1])
                    
                    # Check which endpoint is closer
                    if dist_to_p0 < min_distance:
                        min_distance = dist_to_p0
                        closest_point = point_pair[0]
                    if dist_to_p1 < min_distance:
                        min_distance = dist_to_p1
                        closest_point = point_pair[1]
            
            if min_distance != float('inf'):
                distances.append(min_distance)
                points_to_plot.append(closest_point)
            else:
                distances.append(1)

    vertical_lines_template.append(_stroke)
    plot_strokes(vertical_lines_template, points_to_plot)
    return np.median(distances)


def calculate_average_distance_to_template_shape_with_horizontal_lines(stroke):
    _stroke = copy.deepcopy(stroke)
    print(len(_stroke))
    horizontal_lines_template = get_horizontal_lines(stroke)
    distances = []
    points_to_plot = []
    counter = 0
    for template_stroke in horizontal_lines_template:
        print('template_stroke',counter)
        for template_point in template_stroke:
            min_distance = float('inf')
            closest_point = None
            for j in range(len(_stroke) - 1):
                print('loop through stroke points', counter)
                point_pair = (_stroke[j], _stroke[j+1])
                print('distance', distance(template_point, point_pair[0]), distance(template_point, point_pair[1]), point_pair[0]['x'], template_point['x'], point_pair[1]['x'])
                if point_pair[0]['x'] <= template_point['x'] <= point_pair[1]['x']:
                    # Calculate distances to the segment endpoints
                    dist_to_p0 = distance(template_point, point_pair[0])
                    dist_to_p1 = distance(template_point, point_pair[1])
                    
                    # Check which endpoint is closer
                    if dist_to_p0 < min_distance:
                        min_distance = dist_to_p0
                        closest_point = point_pair[0]
                    if dist_to_p1 < min_distance:
                        min_distance = dist_to_p1
                        closest_point = point_pair[1]
                    print('min_distance', min_distance)
            if min_distance != float('inf'):
                distances.append(min_distance)
                points_to_plot.append(closest_point)
            else:
                distances.append(1)
                points_to_plot.append(closest_point)
        counter+=1

    horizontal_lines_template.append(_stroke)
    plot_strokes(horizontal_lines_template, points_to_plot)
    return np.median(distances)
# def calculate_average_distance_to_template_shape_with_vertical_lines(stroke, edge_point_positions):
#     # strokes = []
#     # # print('edge_point_positions', edge_point_positions)

#     # for i in range(0, len(edge_point_positions)-1, 2):
#     #     strokes.append(stroke[edge_point_positions[i]:edge_point_positions[i+1]]) 
#     # print('len strokes', len(strokes))     
#     _stroke = copy.deepcopy(stroke)
#     vertical_lines_template = get_vertical_lines(stroke)
#     # calculate the average distance of each point to the template shape
#     distances = []
#     points_to_plot = []
#     closest_points = []
#     for template_stroke in vertical_lines_template:
#         # print('looop')
#         for idx,template_point in enumerate(template_stroke):
#             # print('template_point', template_point)
#             min_distance = float('inf')
#             # for stroke in strokes:
#             #     print('loop 2 durch strokes')
#             #     print(len(strokes), len(stroke))
#             print(len(_stroke))
#             for j in range(len(_stroke) -1):
#                 # print('loop 3 durch points')

#                 point_pair = (_stroke[j], _stroke[j+1])
#                 # print('point_pair', point_pair)
#                 if template_point['y'] >= point_pair[0]['y'] and template_point['y'] <= point_pair[1]['y']:
#                     eucl_distance_1 = distance(template_point, point_pair[0])
#                     eucl_distance_2 = distance(template_point, point_pair[1])
#                     new_min_distance = min(eucl_distance_1, eucl_distance_2)
#                     # print('new_min_distance', new_min_distance)
#                     if new_min_distance < min_distance:
#                         if eucl_distance_1 < eucl_distance_2:
#                             min_distance = eucl_distance_1
#                             if len(closest_points)-1 < idx:
#                                 closest_points.insert(idx, point_pair[0])
#                             else:
#                                 closest_points[idx] = point_pair[0]
#                         else:
#                             min_distance = eucl_distance_2
#                             if len(closest_points)-1 < idx:
#                                 closest_points.insert(idx, point_pair[1])
#                             else:
#                                 closest_points[idx] = point_pair[1]
                        
#             if min_distance == float('inf'):
#                 distances.append(1)
#             else:
#                 distances.append(min_distance)
#         # print('closest_points', closest_points)
#         points_to_plot.extend(closest_points)
#         closest_points = []
#     # print('hihfsjk', distances[:16], distances[16:32])
#     print(np.median(distances))
#     # if np.median(distances) < 0.1:  
                      
#     vertical_lines_template.extend([_stroke])
    
#     plot_strokes(vertical_lines_template, points_to_plot )
#     return np.median(distances)
            
   
def calculate_average_min_distance_to_template_shape(candidate):
    ideal_circle_shape = get_perfect_mock_shape(candidate)['circle']
    ideal_rect_shape = get_perfect_mock_shape(candidate)['rectangle']
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_circle_shape_arr = np.array([[point['x'], point['y']] for point in ideal_circle_shape])
    ideal_rect_shape_arr = np.array([[point['x'], point['y']] for point in ideal_rect_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in candidate])
    bounding_box = get_bounding_box(candidate)
    
    diagonal_of_bounding_box = calculate_diagonal_length(bounding_box)
    # Calculate pairwise distances between all points in ideal_shape and candidate
    # np.newaxis increases the dimension where applied, making the array broadcasting possible
    distances_to_ideal_circle_shape = np.sqrt(((ideal_circle_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    distances_to_ideal_rect_shape = np.sqrt(((ideal_rect_shape_arr[:, np.newaxis] - candidate_arr) ** 2).sum(axis=2))
    # Find the minimum distance for each point in ideal_shape to any point in candidate
    min_distances_to_ideal_circle_shape = np.min(distances_to_ideal_circle_shape, axis=1)
    min_distances_to_ideal_rect_shape = np.min(distances_to_ideal_rect_shape, axis=1)
   
    # Calculate the average of these minimum distances
    average_min_distance_ideal_circle = np.mean(min_distances_to_ideal_circle_shape)
    average_min_distance_ideal_rect = np.mean(min_distances_to_ideal_rect_shape)
   
    return average_min_distance_ideal_circle, average_min_distance_ideal_rect
   
   
def calculate_x_cluster_distribution(points):
    x_coords = [stroke['x'] for stroke in points] 
    sorted_x_coords = sorted(x_coords)
    max_x = max(sorted_x_coords)
    min_x = min(sorted_x_coords)
    number_of_x_values = len(sorted_x_coords)
    twenty_percent = int(number_of_x_values * 0.2)
    eighty_percent = int(number_of_x_values * 0.8)
    twenty_percent_x = sorted_x_coords[twenty_percent]
    eighty_percent_x = sorted_x_coords[eighty_percent]
    span = max_x - min_x
    if span == 0:
        return 1, 0
    span_traveled_twenty_percent = (twenty_percent_x - min_x) / span
    span_traveled_eighty_percent = (eighty_percent_x - min_x) / span
    return span_traveled_twenty_percent, span_traveled_eighty_percent

def calculate_y_cluster_distribution(points):
    y_coords = [stroke['y'] for stroke in points] 
    sorted_y_coords = sorted(y_coords)
    max_y = max(sorted_y_coords)
    min_y = min(sorted_y_coords)
    number_of_y_values = len(sorted_y_coords)
    twenty_percent = int(number_of_y_values * 0.2)
    eighty_percent = int(number_of_y_values * 0.8)
    twenty_percent_y = sorted_y_coords[twenty_percent]
    eighty_percent_y = sorted_y_coords[eighty_percent]
    span = max_y - min_y
    if span == 0:
        return 1, 0
    span_traveled_twenty_percent = (twenty_percent_y - min_y) / span
    span_traveled_eighty_percent = (eighty_percent_y - min_y) / span
    return span_traveled_twenty_percent, span_traveled_eighty_percent

def get_cluster_amount(stroke):
    x_cluster_twenty_percent = calculate_x_cluster_distribution(stroke)[0]
    x_cluster_eighty_percent = calculate_x_cluster_distribution(stroke)[1]
    y_cluster_twenty_percent = calculate_y_cluster_distribution(stroke)[0]
    y_cluster_eighty_percent = calculate_y_cluster_distribution(stroke)[1]
    amount_cluster = 0
    if x_cluster_twenty_percent < 0.1:
        amount_cluster+=1
    if x_cluster_eighty_percent > 0.9:
        amount_cluster+=1
    if y_cluster_twenty_percent < 0.1:
        amount_cluster+=1
    if y_cluster_eighty_percent > 0.9:
        amount_cluster+=1
    return amount_cluster



def get_strokes_from_candidate(candidate, strokes):
    _strokes = []
    
    for index in candidate:
        _strokes.append(strokes[index])
    ordered_strokes = order_strokes(_strokes)

    return ordered_strokes

def get_edge_points(strokes_of_candidate):
    edge_point_positions = []
    for idx, stroke in enumerate(strokes_of_candidate):
        if idx == 0:
            edge_point_positions.append(0)
            edge_point_positions.append(len(stroke) - 1)
        else:
            edge_point_positions.append(edge_point_positions[-1] + 1)
            edge_point_positions.append(edge_point_positions[-1] + len(stroke) - 1)

def get_shape_no_shape_features(candidate, strokes):
    """ Extract feature vector from stroke """
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    edge_point_positions = get_edge_points(strokes_of_candidate)
    scaled_strokes = scale(strokes_of_candidate)
    translated_strokes = translate_to_origin(scaled_strokes)
    # plot_strokes(translated_strokes)
    stroke = translated_strokes[0]   
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    bounding_box = get_bounding_box(stroke)
    
    if (len(stroke) < 5 or has_only_duplicates or bounding_box[4] < 1 or bounding_box[5] < 1):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
   
    closed_shape = is_closed_shape(stroke, edge_point_positions)
    
 
    return {'feature_names': ['closed_shape'], 'features': [closed_shape]}
   

def get_circle_features(candidate, strokes):
    edge_point_positions = []
    for idx, stroke in enumerate(strokes):
        edge_point_positions.append(edge_point_positions[-1] + 1) if idx > 0 else edge_point_positions.append(0)
        edge_point_positions.append(edge_point_positions[-1] + len(stroke) - 1)
         
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    scaled_strokes = scale(strokes_of_candidate)
    translated_strokes = translate_to_origin(scaled_strokes)
    edge_points_to_be_plotted = [translated_strokes[edge_point_position] for edge_point_position in edge_point_positions]
    # plot_strokes(translated_strokes, edge_points_to_be_plotted)
    stroke = translated_strokes[0]
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    if (len(stroke) < 5 or has_only_duplicates):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    closed_shape = is_closed_shape(stroke, edge_point_positions)
    aspect_ratio = get_aspect_ratio(stroke)

    convex_hull_perimeter_to_area_ratio = compute_convex_hull_perimeter_to_area_ratio(stroke)
    total_stroke_length_to_diagonal_length = compute_total_stroke_length_to_diagonal_length(stroke)

    return {'feature_names': ['closed_shape', 'convex_hull_perimeter_to_area_ratio', 'total_stroke_length_to_diagonal_length', 'aspect_ratio'], 'features': [closed_shape, convex_hull_perimeter_to_area_ratio, total_stroke_length_to_diagonal_length, aspect_ratio]}


def get_rectangle_features(candidate, strokes):

    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    print('strokes_of_candidate', len(strokes_of_candidate), len(strokes_of_candidate[0]), len(strokes_of_candidate[1]))
    # edge_point_positions = []
    # for idx, stroke in enumerate(strokes_of_candidate):
    #     if idx == 0:
    #         edge_point_positions.append(0)
    #         edge_point_positions.append(len(stroke) - 1)
    #     else:
    #         edge_point_positions.append(edge_point_positions[-1] + 1)
    #         edge_point_positions.append(edge_point_positions[-1] + len(stroke) - 1)
    
    scaled_strokes = scale(strokes_of_candidate)
    translated_strokes = translate_to_origin(scaled_strokes)

    stroke = translated_strokes[0]   
    # print('stroke', stroke) 
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    if (len(stroke) < 5 or has_only_duplicates):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    number_of_convex_hull_vertices = get_number_of_convex_hull_vertices(stroke)
    average_distance_to_template_with_vertical_lines =calculate_average_distance_to_template_shape_with_vertical_lines(stroke)
    average_distance_to_template_with_horizontal_lines = calculate_average_distance_to_template_shape_with_horizontal_lines(stroke)
   
    print('median_distance_to_template_with_vertical_lines', average_distance_to_template_with_vertical_lines)
    print('median_distance_to_template_with_horizontal_lines', average_distance_to_template_with_horizontal_lines)
    return {'feature_names': ['number_of_convex_hull_vertices', 'average_distance_to_template_with_vertical_lines', 'average_distance_to_template_with_horizontal_lines'], 'features': [number_of_convex_hull_vertices, average_distance_to_template_with_vertical_lines, average_distance_to_template_with_horizontal_lines]}

    
    

def get_circle_rectangle_features(candidate, strokes):
    """ Extract feature vector from stroke """
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    scaled_strokes = scale(strokes_of_candidate)
    translated_strokes = translate_to_origin(scaled_strokes)
    # plot_strokes(translated_strokes)
    stroke = translated_strokes[0]
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    if (len(stroke) < 5 or has_only_duplicates):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    amount_cluster = get_cluster_amount(stroke)
    number_of_convex_hull_vertices = get_number_of_convex_hull_vertices(stroke)
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
   
    return {'feature_names': ['number_of_convex_hull_vertices', 'amount_cluster'], 'features': [number_of_convex_hull_vertices, amount_cluster]}



from scipy.spatial import ConvexHull
from helper.utils import get_bounding_box, calculate_diagonal_length, calculate_total_stroke_length, plot_strokes, plot_strokes_without_scala
import numpy as np
import copy
from helper.utils import get_perfect_mock_shape, get_horizontal_lines, get_vertical_lines, stroke_has_only_duplicates, reconstruct_strokes_from_combined_strokes, get_strokes_from_candidate
from shapely.geometry import Polygon, LineString
from helper.normalizer import distance, translate_to_origin, scale
from scipy.spatial import distance_matrix
from sklearn.cluster import DBSCAN
from sklearn import decomposition
from sklearn.preprocessing import MinMaxScaler
from helper.export_strokes_to_inkml import export_strokes_to_inkml
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import networkx as nx
import math



def calculate_direction(point1, point2):
    dx = point2['x'] - point1['x']
    dy = point2['y'] - point1['y']
    
    angle = math.atan2(dy, dx)
    return math.degrees(angle)  # Convert to degrees


def analyze_stroke_directions(stroke, tolerance=5):
    amount_up_down_directions = 0
    amount_left_right_directions = 0
    
    for i in range(len(stroke) - 1):
        angle = calculate_direction(stroke[i], stroke[i + 1])
        # Normalize the angle to the range [-180, 180]
        angle = (angle + 180) % 360 - 180
        # # Normalize angle difference
        # if angle_diff > math.pi:
        #     angle_diff = 2 * math.pi - angle_diff
     # calculate up and down directions and calculate left and right directions
        if math.isclose(angle, 0, abs_tol=tolerance) or math.isclose(angle, 180, abs_tol=tolerance) or math.isclose(angle, -180, abs_tol=tolerance):
            amount_up_down_directions += 1
        if math.isclose(angle, 90, abs_tol=tolerance) or math.isclose(angle, -90, abs_tol=tolerance):
            amount_left_right_directions += 1
    # # Count the number of direction changes close to 90 degrees (pi/2 radians)
    # # Check if the angle difference is close to 90 degrees
    #     print('hiiier: ', angle_diff_degrees)
    #     if 90 - tolerance <= angle_diff_degrees <= 90 + tolerance:
    #         perpendicular_changes += 1
   
    return amount_up_down_directions + amount_left_right_directions


def truncate_lists_to_same_length(list1, list2):
    min_length = min(len(list1), len(list2))
    return list1[:min_length], list2[:min_length]

def count_clusters(labels):
    unique_labels = set(labels)
    if -1 in unique_labels:
        unique_labels.remove(-1)
    return len(unique_labels)

def visualize_vectors(points, direction_vectors, labels):
    # Initialize a list to collect points
    _points = []
    x_lim=(-2, 2)
    y_lim=(-2, 2)

    # Collect every third point
    for i in range(0, len(points), 1):
        _points.append(points[i])
    # Convert list to a numpy array
    _points = np.array(_points)
    
    plt.figure(figsize=(8, 8))
    unique_labels = np.unique(labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
    colors = np.array([col if label != -1 else [0.5, 0.5, 0.5, 1] for label, col in zip(unique_labels, colors)])

    for k, col in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = _points[:-1][class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=8)
    
    for i in range(len(_points) - 1):
        plt.arrow(_points[i, 0], _points[i, 1], direction_vectors[i, 0], direction_vectors[i, 1],
                  head_width=0.05, head_length=0.1, fc='k', ec='k', label='Direction Vector')
    # for i in range(0, len(_points) - 1,10):
        # plt.text(_points[i, 0], _points[i, 1], str({'x': round(direction_vectors[i, 0],3), 'y': round(direction_vectors[i, 1],3)}), fontsize=12)

    # Set fixed limits for x and y axes
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    
    plt.title('Clusters of Direction Vectors')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def visualize_clusters(features):
    x_lim=(-2, 2)
    y_lim=(-2, 2)
    plt.figure(figsize=(8, 8))
    points_array = np.array(features)

    # Create a scatter plot
    plt.scatter(points_array[:, 0], points_array[:, 1], color='blue', marker='o')

    # Set fixed limits for x and y axes
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    
    plt.title('Clusters of 2D Feature Values')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()
    
def visualize_clusters_without_scala(features):
   
    plt.figure(figsize=(8, 8))
    points_array = np.array(features)

    # Create a scatter plot
    plt.scatter(points_array[:, 0], points_array[:, 1], color='blue', marker='o')
    
    plt.title('Clusters of 2D Feature Values')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def calculate_direction_vectors(points):
    
    _points = np.array([(point['x'], point['y']) for point in points])
    # Calculate direction vectors for consecutive points
    vectors = np.diff(_points, axis=0)
    # Normalize the vectors
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized_vectors = vectors / norms
    return normalized_vectors

def calculate_angle_between_vectors(v1, v2):
    """
    Berechnet den Winkel zwischen zwei Vektoren in Grad.
    :param v1: Erster Vektor (Liste oder numpy-Array)
    :param v2: Zweiter Vektor (Liste oder numpy-Array)
    :return: Winkel in Grad
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    # Berechne das Skalarprodukt
    dot_product = np.dot(v1, v2)
    
    # Berechne die Normen der Vektoren
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    # Berechne den Kosinus des Winkels
    cos_theta = dot_product / (norm_v1 * norm_v2)
    
    # Korrigiere numerische Fehler
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    
    # Berechne den Winkel in Radiant
    angle_radians = np.arccos(cos_theta)
    
    # Konvertiere den Winkel in Grad
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees

def count_180_degree_angles(direction_vectors):
    count = 0
    degree_vector = [1, 0]
    for i in range(len(direction_vectors) - 1):
        angle = calculate_angle_between_vectors(direction_vectors[i], degree_vector)
        if angle < 2:
           count += 1
    return count

def count_minus_180_degree_angles(direction_vectors):
    count = 0
    degree_vector = [-1, 0]
    for i in range(len(direction_vectors) - 1):
        angle = calculate_angle_between_vectors(direction_vectors[i], degree_vector)
        if angle < 2:
           count += 1
    return count

def count_90_degree_angles(direction_vectors):
    count = 0
    degree_vector = [0, 1]
    for i in range(len(direction_vectors) - 1):
        angle = calculate_angle_between_vectors(direction_vectors[i], degree_vector)
        if angle < 2:
           count += 1
    return count

def count_minus_90_degree_angles(direction_vectors):
    count = 0
    degree_vector = [0, -1]
    for i in range(len(direction_vectors) - 1):
        angle = calculate_angle_between_vectors(direction_vectors[i], degree_vector)
        if angle < 2:
           count += 1
    return count

def cluster_direction_vectors(direction_vectors, points, eps=0.05, min_samples=12):
    # remove nan values
    for i in range(len(direction_vectors)):
        if np.isnan(direction_vectors[i]).any():
            direction_vectors[i] = direction_vectors[i-1]
            points[i] = points[i-1]
    doubled_points = [point * 2 for point in points]
    # set doubled_points to the same length as direction_vectors
    # doubled_points, direction_vectors = truncate_lists_to_same_length(doubled_points, direction_vectors)
    combined_features = np.hstack((direction_vectors, doubled_points[:-1]))
    
    # Scale the data to the range [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler.fit_transform(combined_features)
    pca = decomposition.PCA(n_components=2)
    pca.fit(scaled_features)
    combined_features = pca.transform(scaled_features)
    # visualize_clusters(combined_features)

    # Use DBSCAN to cluster the direction vectors
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(combined_features)
    # clustering = DBSCAN(eps=eps, min_samples=int(len(points) * 0.15), metric='cosine').fit(combined_features)


    return clustering.labels_

def standard_deviation_of_distances(points):

    _points = np.array([(point['x'], point['y']) for point in points if not point == None])
    dist_matrix = distance_matrix(_points, _points)
    upper_triangular_indices = np.triu_indices_from(dist_matrix, k=1)
    distances = dist_matrix[upper_triangular_indices]
    standard_deviation = np.std(distances)
    return standard_deviation

def get_aspect_ratio(stroke):
    bounding_box = get_bounding_box(stroke)
    width = bounding_box[4]
    height = bounding_box[5]
    return width / height


def get_number_of_convex_hull_vertices(stroke):
    _stroke = copy.deepcopy(stroke)
    points = [(point['x'], point['y']) for point in _stroke]
    points = np.array(points)
    # unique_points = np.unique(points, axis=0)
    try:
        hull = ConvexHull(points)
        # hull_points = [{'x': points[idx][0], 'y': points[idx][1]} for idx in hull.vertices]

        # plot_strokes([_stroke],hull_points)
        return len(hull.vertices)
    except Exception as e:
        print("Convex hull could not be computed.", e)
        # Vermutlich handelt es sich in diesem Fall um eine Linie
        return 2
    

def get_convexity(stroke):
    # Flatten the list of strokes into a list of points
    points = np.array([(point['x'], point['y']) for point in stroke])
    
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

# def compute_convex_hull(points):
#     hull = ConvexHull(points)
#     return hull

# def calculate_concavity(stroke):
#     points = np.array([(point['x'], point['y']) for point in stroke])
#     polygon = Polygon(points)
#     hull = compute_convex_hull(points)
#     hull_polygon = Polygon(points[hull.vertices])
    
#     shape_area = polygon.area
#     hull_area = hull_polygon.area
    
#     concavity_area = hull_area - shape_area
#     concavity_index = concavity_area / hull_area if hull_area != 0 else 0
    
#     return concavity_index


def is_closed_shape(stroke, edge_point_positions=None):
    _stroke = copy.deepcopy(stroke)
    edge_points = []
    for edge_point_position in edge_point_positions:
        edge_points.append(_stroke[edge_point_position])
    min_distances = []
    for edge_point in edge_points:
        distances = []
        for point2 in edge_points:
            if edge_point == point2:
                continue
            distances.append(distance(edge_point, point2))
        min_distances.append(min(distances))
        
    return sum(min_distances)

def is_closed_convex_hull(stroke):
    points = np.array([(point['x'], point['y']) for point in stroke])
    try:
        hull = ConvexHull(points)
    except Exception as e:
        print("Convex hull could not be computed.", e)
        # Vermutlich handelt es sich in diesem Fall um eine Linie
        return 0
    
    hull_points = [{'x': points[idx][0], 'y': points[idx][1]} for idx in hull.vertices]

    # plot_strokes([stroke],hull_points)
    # return len(hull.vertices) == len(points)
    return len(hull.vertices) / len(points)

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
        print("Convex hull could not be computed.")
        return 0
        
    
def compute_convex_hull_area_to_perimeter_ratio(points):
    _points = [(point['x'], point['y']) for point in points]
    
    try:
        hull = ConvexHull(_points)
        hull_area = hull.volume  # For 2D, volume is the area
        hull_perimeter = hull.area  # For 2D, area is the perimeter
        return hull_area / hull_perimeter
    except Exception as e:
        print("Convex hull could not be computed.")
        return 0
  
def find_nearest_point_for_everey_edge_point(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    top_left = {'x': bounding_box[0], 'y': bounding_box[2]}
    bottom_right = {'x': bounding_box[0] + bounding_box[4], 'y': bounding_box[2]}
    bottom_left = {'x': bounding_box[0], 'y': bounding_box[2] + bounding_box[5]}
    top_right = {'x': bounding_box[0] + bounding_box[4], 'y': bounding_box[2] + bounding_box[5]}
    edge_points = [top_left, top_right, bottom_left, bottom_right]
    min_distances = []
    closest_points = []
    for edge_point in edge_points:
        distances = []
        for point2 in _stroke:
            distances.append(distance(edge_point, point2))
        min_distances.append(min(distances))
        # get index of the closest point
        closest_point_index = distances.index(min(distances))
        closest_points.append(_stroke[closest_point_index])
    # plot_strokes([_stroke], edge_points)
    # plot_strokes([_stroke], closest_points)
    
    return sum(min_distances)
    
def compute_total_stroke_length_to_diagonal_length(stroke):
    _stroke = copy.deepcopy(stroke)
    diagonal_length = calculate_diagonal_length(get_bounding_box(_stroke))
    total_stroke_length = calculate_total_stroke_length(_stroke)
    
    return total_stroke_length / diagonal_length

def is_closed_graph(stroke):
    G = nx.Graph()
    for i in range(len(stroke) - 1):
        point1 = (stroke[i]['x'], stroke[i]['y'])
        point2 = (stroke[i + 1]['x'], stroke[i + 1]['y'])
        G.add_edge(point1, point2)
    return nx.is_eulerian(G)

def calculate_average_distance_to_template_shape_with_vertical_lines(strokes, stroke, candidate):
   
    vertical_lines_template = get_vertical_lines(stroke)
    distances = []
    points_to_plot = []
    reconstructed_strokes = reconstruct_strokes_from_combined_strokes(strokes, stroke)


    for template_stroke in vertical_lines_template:
        for template_point in template_stroke:
            min_distance = float('inf')
            closest_point = None
            
            for stroke in reconstructed_strokes:
                for j in range(len(stroke) - 1):
                    point_pair = (stroke[j], stroke[j+1])
                    
                    if point_pair[0]['y'] <= template_point['y'] <= point_pair[1]['y'] or point_pair[1]['y'] <= template_point['y'] <= point_pair[0]['y']:
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
    
        
    vertical_lines_template.extend(reconstructed_strokes)
    # plot_strokes(vertical_lines_template, points_to_plot)
    standard_deviation_of_match_points = standard_deviation_of_distances(points_to_plot)
    # return np.median(distances)
    # return np.mean(distances)
    return standard_deviation_of_match_points


def calculate_average_distance_to_template_shape_with_horizontal_lines(strokes, stroke, candidate):
    horizontal_lines_template = get_horizontal_lines(stroke)
    distances = []
    points_to_plot = []
    counter = 0
    reconstructed_strokes = reconstruct_strokes_from_combined_strokes(strokes, stroke)
    for template_stroke in horizontal_lines_template:
        for template_point in template_stroke:
            min_distance = float('inf')
            closest_point = None
            
            for stroke in reconstructed_strokes:
                for j in range(len(stroke) - 1):
                    point_pair = (stroke[j], stroke[j+1])
                    if point_pair[0]['x'] <= template_point['x'] <= point_pair[1]['x'] or point_pair[1]['x'] <= template_point['x'] <= point_pair[0]['x']:
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
                points_to_plot.append(closest_point)
        counter+=1
   
    horizontal_lines_template.extend(reconstructed_strokes)
    # plot_strokes(horizontal_lines_template, points_to_plot)
    standard_deviation_of_match_points = standard_deviation_of_distances(points_to_plot)
    # return np.median(distances)
    # return np.mean(distances)
    return standard_deviation_of_match_points
            
   
def calculate_average_min_distance_to_template_shape(stroke, candidate):
    ideal_circle_shape = get_perfect_mock_shape(stroke)['circle']
    ideal_rect_shape = get_perfect_mock_shape(stroke)['rectangle']
    # Convert lists of dictionaries to NumPy arrays for faster operations
    ideal_circle_shape_arr = np.array([[point['x'], point['y']] for point in ideal_circle_shape])
    ideal_rect_shape_arr = np.array([[point['x'], point['y']] for point in ideal_rect_shape])
    candidate_arr = np.array([[point['x'], point['y']] for point in stroke])
    bounding_box = get_bounding_box(stroke)
    
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
   
def calculate_circumference_to_stroke_length_ratio(stroke):
    _stroke = copy.deepcopy(stroke)
    bounding_box = get_bounding_box(_stroke)
    circumference = bounding_box[4] * 2 + bounding_box[5] * 2
    stroke_length = calculate_total_stroke_length(_stroke)
    return circumference / stroke_length
   
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

def findparallel(strokes):

    parallel_lines = []
    for i in range(len(strokes)):
        for j in range(len(strokes)):
            if (i == j):continue
            if (abs(strokes[i][0]['y'] - strokes[j][0]['y']) < 0.1):          
                #You've found a parallel line!
                parallel_lines.append((i,j))
            if (abs(strokes[i][0]['x'] - strokes[j][0]['x']) < 0.1):          
                #You've found a parallel line!
                parallel_lines.append((i,j))


    return len(parallel_lines)

def is_continuous(stroke, tolerance=1):
    distances = []
    for i in range(len(stroke) - 1):
        point1 = stroke[i]
        point2 = stroke[i + 1]
        distance = np.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)
        distances.append(distance)
    return max(distances)

def get_edge_points(strokes_of_candidate):
    edge_point_positions = []
    for idx, stroke in enumerate(strokes_of_candidate):
        if idx == 0:
            edge_point_positions.append(0)
            edge_point_positions.append(len(stroke) - 1)
        else:
            edge_point_positions.append(edge_point_positions[-1] + 1)
            edge_point_positions.append(edge_point_positions[-1] + len(stroke) - 1)
    return edge_point_positions

def get_shape_no_shape_features(candidate, strokes):
    """ Extract feature vector from stroke """
    
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    edge_point_positions = get_edge_points(strokes_of_candidate)
    edge_points = []
    
    scaled_strokes = scale(strokes_of_candidate)
    translated_strokes = translate_to_origin(scaled_strokes)
    
  
    stroke = translated_strokes[0]   
    for edge_point_position in edge_point_positions:
        edge_points.append(stroke[edge_point_position])
    # print(edge_points)
    # plot_strokes(translated_strokes, edge_points)
    
    has_only_duplicates = stroke_has_only_duplicates(stroke)
   
    if (len(stroke) < 5 or has_only_duplicates):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    closed_shape = is_closed_shape(stroke, edge_point_positions)
    # aspect ratio
    # compute_convex_hull_area_to_perimeter_ratio(stroke)
    
    return {'feature_names': ['closed_convex_hull'], 'features': [closed_shape]}


def get_circle_rectangle_features(candidate, strokes):
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    scaled_strokes = scale(strokes_of_candidate)
    
    translated_strokes = translate_to_origin(scaled_strokes)

    stroke = translated_strokes[0]   
    
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    bounding_box = get_bounding_box(stroke)
    if (len(stroke) < 5 or has_only_duplicates or bounding_box[4] == 0 or bounding_box[5] == 0):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
    number_of_convex_hull_vertices = get_number_of_convex_hull_vertices(stroke)
    average_distance_to_template_with_vertical_lines =calculate_average_distance_to_template_shape_with_vertical_lines(strokes_of_candidate, stroke, candidate)
    average_distance_to_template_with_horizontal_lines = calculate_average_distance_to_template_shape_with_horizontal_lines(strokes_of_candidate, stroke, candidate)
    nearest_point_for_every_edge_point = find_nearest_point_for_everey_edge_point(stroke)


    # amount_of_strokes = len(strokes_of_candidate)
    direction_vectors = calculate_direction_vectors(stroke)
    labels = cluster_direction_vectors(direction_vectors, np.array([[point['x'], point['y']] for point in stroke]))
    # visualize_vectors(np.array([[point['x'], point['y']] for point in stroke]), direction_vectors, labels)
    # average_distance_to_template_shape_circle = calculate_average_min_distance_to_template_shape(stroke, candidate)[0]
    # return {'feature_names': ['number_of_convex_hull_vertices','standard_deviation_to_template_with_vertical_lines', 'standard_deviation_to_template_with_horizontal_lines', 'directional_clusters'], 'features': [number_of_convex_hull_vertices, nearest_point_for_every_edge_point]}
    return {'feature_names': ['number_of_convex_hull_vertices','standard_deviation_to_template_with_vertical_lines', 'standard_deviation_to_template_with_horizontal_lines', 'direction_vectors'], 'features': [number_of_convex_hull_vertices, average_distance_to_template_with_vertical_lines, average_distance_to_template_with_horizontal_lines, count_clusters(labels)]}
    # return {'feature_names': ['number_of_convex_hull_vertices'], 'features': [number_of_convex_hull_vertices]}
    # return {'feature_names': ['directional_clusters'], 'features': [count_clusters(labels) ]}
    # return {'feature_names': ['is_closed_shape', ], 'features': [closed_shape] }
    # return {'feature_names': ['directional_clusters'], 'features': [count_clusters(labels)]}

def get_hellinger_correlation_features(candidate, strokes):
    strokes_of_candidate = get_strokes_from_candidate(candidate, strokes)
    edge_point_positions = get_edge_points(strokes_of_candidate)
    scaled_strokes = scale(strokes_of_candidate)
    
    translated_strokes = translate_to_origin(scaled_strokes)

    stroke = translated_strokes[0]   
    
    has_only_duplicates = stroke_has_only_duplicates(stroke)
    bounding_box = get_bounding_box(stroke)
    if (len(stroke) < 5 or has_only_duplicates or bounding_box[4] == 0 or bounding_box[5] == 0):
        return {'feature_names': ['distance_between_stroke_edge_points'], 'features': None}
   
    closed_shape_sum = is_closed_shape(stroke, edge_point_positions)
    closed_convex_hull = is_closed_convex_hull(stroke)
    nearest_point_for_everey_edge_point = find_nearest_point_for_everey_edge_point(stroke)
   
    return {'feature_names': ['is_closed_shape', 'closed_convex_hull', 'nearest_point_for_everey_edge_point'], 'features': [closed_shape_sum, closed_convex_hull, nearest_point_for_everey_edge_point]}


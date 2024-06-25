from helper.parsers import parse_ground_truth
from helper.features import get_circle_rectangle_features
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler
from helper.utils import distance
from matplotlib.patches import Ellipse
import math


def calculate_ellipse_parameters(cluster_points, cluster_center):
    
    _cluster_points = [{'x': point[0], 'y': point[1]} for point in cluster_points]
    _cluster_center = {'x': cluster_center[0], 'y': cluster_center[1]}
    
    furthest_point = max(_cluster_points, key=lambda point: distance(point, _cluster_center))
    F1 = furthest_point
    F2 = {}
    
   
    _cluster_center = {'x': cluster_center[0], 'y': cluster_center[1]}
      
    translated_F1 = {'x': F1['x'] - _cluster_center['x'], 'y': F1['y'] - _cluster_center['y']}
    translated_F2 = {'x': -translated_F1['x'], 'y': -translated_F1['y']}

     # Move the translated points back to their original positions
    F1 = {'x': translated_F1['x'] + _cluster_center['x'], 'y': translated_F1['y'] + _cluster_center['y']}
    F2 = {'x': translated_F2['x'] + _cluster_center['x'], 'y': translated_F2['y'] + _cluster_center['y']}
    
    dx = F1['x'] - F2['x']
    dy = F1['y'] - F2['y']
    
    # Calculate the angle using atan2
    angle = math.atan2(dy, dx)
    
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle)
    
       
    sum_of_absolute_distances = []
    for point in _cluster_points:
        distance_to_F1 = [abs(point['x'] - F1['x']), abs(point['y'] - F1['y'])]
        distance_to_F2 = [abs(point['x'] - F2['x']), abs(point['y'] - F2['y'])]
        distancejdfsjl = [distance_to_F1[0] + distance_to_F2[0], distance_to_F1[1] + distance_to_F2[1]]
        
        sum_of_absolute_distances.append(distancejdfsjl)
    S = np.max(sum_of_absolute_distances, axis=0)
    S = sum(S)
   
    return F1, F2, S, angle_degrees

def calculate_ellipse_parameters_n_dimensional(feature_vectors, cluster_center):
    furthest_point = max(feature_vectors, key=lambda vector: distance(vector, cluster_center))
    F1 = furthest_point
    F2 = [0 for _ in range(len(F1))]
    translated_F1 = []
    translated_F2 = []
    for idx,entry in enumerate(F1):
        # print('jfakls', entry, cluster_center[idx])
        translated_F1.append(entry - cluster_center[idx])
        translated_F2.append(-translated_F1[idx])
    for idx,entry in enumerate(translated_F1):
        F1[idx] = entry + cluster_center[idx]
        F2[idx] = translated_F2[idx] + cluster_center[idx]
        
    sum_of_absolute_distances = []
    for vector in feature_vectors:
        # calculate the absolute distance from the vector to F1 and F2
        distance_to_F1 = [abs(vector[dim] - F1[dim]) for dim in range(len(F1))]
        distance_to_F2 = [abs(vector[dim] - F2[dim]) for dim in range(len(F2))]
        total_distance = [distance_to_F1[dim] + distance_to_F2[dim] for dim in range(len(distance_to_F1))]
        
        sum_of_absolute_distances.append(total_distance)
        # distance_to_F1 = distance(vector, F1)
        # distance_to_F2 = distance
        # sum_of_absolute_distances.append(distance_to_F1 + distance_to_F2)
    S = np.max(sum_of_absolute_distances, axis=0)
    S = sum(S)
    return F1, F2, S
    
def calculate_S(feature_vector, F1, F2, distance_function):
    
    distance_to_F1 = distance_function(feature_vector, F1)
    distance_to_F2 = distance_function(feature_vector, F2)
    sum_of_absolute_distances = distance_to_F1 + distance_to_F2
    
    return sum_of_absolute_distances
    
def get_all_strokes_with_label(label:str, truth:dict)->list:
    strokes = []
    for item in truth:
        if label in item:
            strokes.append(item[label])
    return strokes

def get_all_no_shapes(truth:dict, candidates)->list:
    strokes = []
    for candidate in candidates:
        candidate_in_truth = False
        for dictionary in truth:
            for shape_name, trace_ids in dictionary.items():
                if set(trace_ids) == set(candidate): 
                    candidate_in_truth = True
        if not candidate_in_truth:
            strokes.append(candidate)
    return strokes
                    

def get_features(file_path, strokes, candidates)->dict:
    truth = parse_ground_truth(file_path)
    circles = get_all_strokes_with_label('circle', truth)
    ellipses = get_all_strokes_with_label('ellipse', truth)
    rectangles = get_all_strokes_with_label('rectangle', truth)
    no_shapes = get_all_no_shapes(truth, candidates)
    circle_features = []
    rectangle_features = []
    ellipse_features = []
    # no_shape_features = []
   
    for circle in circles:
        circle_features.append(get_circle_rectangle_features(circle, strokes)['features'])
    for rectangle in rectangles:
        rectangle_features.append(get_circle_rectangle_features(rectangle, strokes)['features'])
    for ellipse in ellipses:
        ellipse_features.append(get_circle_rectangle_features(ellipse, strokes)['features'])
    circle_features.extend(ellipse_features)
    # for no_shape in no_shapes:
    #     no_shape_features.append(get_circle_rectangle_features(no_shape, strokes)['features'])
     
    return circle_features, rectangle_features
    
def visualize_clusters(X, labels):
  

    x_lim=(-1, 1)
    y_lim=(-1, 1)
    # # transform the data to be within a specified range to avoid biasing the MDS results towards features with larger ranges.
    scaler = MinMaxScaler() 
    X_normalized = scaler.fit_transform(X)
    
     # Calculate cluster centers based on the normalized data
    unique_labels = np.unique(labels)
    cluster_centers = np.array([X_normalized[labels == label].mean(axis=0) for label in unique_labels])
    
    combined_data = np.vstack([X_normalized, cluster_centers])
    dissimilarity_matrix = pairwise_distances(combined_data, metric='euclidean')

    # Apply MDS
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    combined_transformed = mds.fit_transform(dissimilarity_matrix)
    
    # Separate transformed data points and cluster centers
    cluster_transformed = combined_transformed[:len(X)]
    cluster_centers_transformed = combined_transformed[len(X):]
   
    plt.figure(figsize=(10, 8))
    # colors = ['green', 'blue', 'red']
    colors = ['green', 'blue']
    # shape_labels = ['circle', 'rectangle', 'no_shape']
    shape_labels = ['circle', 'rectangle']
    for label in unique_labels:
        indices = np.where(labels == label)
        plt.scatter(cluster_transformed[indices, 0], cluster_transformed[indices, 1],
                    c=colors[label], label=shape_labels[label], s=50, alpha=0.2)
    
    
    # Plot the cluster centers and their respective circles
    for center_transformed, label in zip(cluster_centers_transformed, unique_labels):
        plt.scatter(center_transformed[0], center_transformed[1],
                    c='red', marker='x', s=100, linewidths=3)
        
        # Calculate radius as the maximum distance from the center to points in the cluster
        cluster_indices = np.where(labels == label)
        cluster_points_transformed = cluster_transformed[cluster_indices]
        # furthest_point = find_furthest_point(cluster_points_transformed, center_transformed)
        F1, F2, S, angle = calculate_ellipse_parameters(cluster_points_transformed, center_transformed  )
        radius = np.max(np.linalg.norm(cluster_points_transformed - center_transformed, axis=1))
        # Find the location of the other end of the semi-major axis and consider it as F2.
        ellipse = Ellipse((center_transformed[0], center_transformed[1]), width=distance(F1, F2), height=S, angle=angle, lw=2, fc='None', color='r', fill=False, linestyle='--')
        circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
                            color='r', fill=False)
        point1 = plt.Circle((F1['x'], F1['y']), 0.01, color='black')
        point2 = plt.Circle((F2['x'], F2['y']), 0.01, color='black')
        plt.gca().add_patch(ellipse)
        plt.gca().add_patch(circle)
        plt.gca().add_patch(point1)
        plt.gca().add_patch(point2)
        # circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
        #                     color='r', fill=False, linestyle='--')
        # plt.gca().add_patch(circle)   
    
    # Set fixed limits for x and y axes
    # plt.xlim(x_lim)
    # plt.ylim(y_lim)
    
    # Add a legend
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
    
    # # Save the clusters to a file
    # with open('clusters.pkl', 'wb') as f:
    #     pickle.dump((cluster_centers), f)
        
    # Load the clusters from the file
    # with open('clusters.pkl', 'rb') as f:
    #     cluster_centers, labels = pickle.load(f)
    
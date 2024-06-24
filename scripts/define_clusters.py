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
    
    # Calculate the distance from the cluster center to the origin
    cluster_center_to_origin_x = _cluster_center['x']
    cluster_center_to_origin_y = _cluster_center['y']
    
    
    translated_F1 = {'x': F1['x'] - cluster_center_to_origin_x, 'y': F1['y'] - cluster_center_to_origin_y}
    translated_F2 = {'x': -translated_F1['x'], 'y': -translated_F1['y']}

     # Move the translated points back to their original positions
    F1 = {'x': translated_F1['x'] + cluster_center_to_origin_x, 'y': translated_F1['y'] + cluster_center_to_origin_y}
    F2 = {'x': translated_F2['x'] + cluster_center_to_origin_x, 'y': translated_F2['y'] + cluster_center_to_origin_y}
    
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
   
    S = np.max(sum_of_absolute_distances)

    print('angle degrees:', angle_degrees)
    return F1, F2, S, angle_degrees


def get_all_strokes_with_label(label:str, truth:dict)->list:
    strokes = []
    for item in truth:
        if label in item:
            strokes.append(item[label])
    return strokes

def get_features(file_path, strokes)->dict:
    truth = parse_ground_truth(file_path)
    circles = get_all_strokes_with_label('circle', truth)
    ellipses = get_all_strokes_with_label('ellipse', truth)
    rectangles = get_all_strokes_with_label('rectangle', truth)
    
    
    circle_features = []
    rectangle_features = []
    ellipse_features = []
   
    for circle in circles:
        print('circle')
        circle_features.append(get_circle_rectangle_features(circle, strokes)['features'])
    for rectangle in rectangles:
        print('rect')
        rectangle_features.append(get_circle_rectangle_features(rectangle, strokes)['features'])
    for ellipse in ellipses:
        print('ellipse')
        ellipse_features.append(get_circle_rectangle_features(ellipse, strokes)['features'])
        
    return circle_features, rectangle_features, ellipse_features
    
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
    colors = ['green', 'blue', 'yellow']
    shape_labels = ['circle', 'rectangle', 'ellipse']
    
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
        F1, F2, S, angle = calculate_ellipse_parameters(cluster_points_transformed, center_transformed)
        radius = np.max(np.linalg.norm(cluster_points_transformed - center_transformed, axis=1))
        # Find the location of the other end of the semi-major axis and consider it as F2.
        print('angle:', angle)
        ellipse = Ellipse((center_transformed[0], center_transformed[1]), width=distance(F1, F2), height=S, angle=angle, lw=2, fc='None', color='r', fill=False, linestyle='--')
        circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
                            color='r', fill=False)
        print('F1:', F1, 'F2:', F2)
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
    
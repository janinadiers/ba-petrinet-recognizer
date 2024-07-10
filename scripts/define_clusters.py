from helper.parsers import parse_ground_truth
from helper.features import get_circle_rectangle_features, get_hellinger_correlation_features, get_shape_no_shape_features
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler
from helper.utils import distance
from matplotlib.patches import Ellipse
from helper.utils import get_strokes_from_candidate
import math
import seaborn as sns
import networkx as nx
import pandas as pd


def is_closed_graph(stroke):
    G = nx.Graph()
    for i in range(len(stroke) - 1):
        point1 = (stroke[i]['x'], stroke[i]['y'])
        point2 = (stroke[i + 1]['x'], stroke[i + 1]['y'])
        G.add_edge(point1, point2)
    return nx.is_eulerian(G) or nx.is_hamiltonian(G)

def calculate_ellipse_parameters_n_dimensional(feature_vectors, cluster_center):
    furthest_point = max(feature_vectors, key=lambda vector: distance(vector, cluster_center))
    F1 = furthest_point
    F2 = 2 * np.array(cluster_center) - np.array(F1)
    
    sum_of_distances = []
    for vector in feature_vectors:
        distance_to_F1 = distance(vector, F1)
        distance_to_F2 = distance(vector, F2)
        total_distance = distance_to_F1 + distance_to_F2
        sum_of_distances.append(total_distance)
    try:
        angle = np.degrees(np.arctan2(F2[1] - F1[1], F2[0] - F1[0]))
    except Exception as e:
        print('error', e)
        angle = 0

    S = max(sum_of_distances)
    return F1, F2, S, angle
    
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
    # no_shapes = get_all_no_shapes(truth, candidates)
    circle_features = []
    rectangle_features = []
    ellipse_features = []
    no_shape_features = []
   
    for circle in circles:
        circle_features.append(get_circle_rectangle_features(circle, strokes)['features'])
    for rectangle in rectangles:
        rectangle_features.append(get_circle_rectangle_features(rectangle, strokes)['features'])
    for ellipse in ellipses:
        ellipse_features.append(get_circle_rectangle_features(ellipse, strokes)['features'])
    circle_features.extend(ellipse_features)
    # for no_shape in no_shapes:
    #     features = get_circle_rectangle_features(no_shape, strokes)['features']
    #     no_shape_features.append(features)
    return circle_features, rectangle_features
    # return circle_features, rectangle_features, no_shape_features
    
def visualize_clusters(X, labels):
  

    for i, elem in enumerate(X):
        if not isinstance(elem, (list, np.ndarray)):
            X.remove(elem)
            labels.remove(labels[i])
    labels = np.array(labels)
    # print('X', X, labels)
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
    
     # Create a mapping from unique labels to color indices
    label_to_color_index = {label: index for index, label in enumerate(unique_labels)}
    
    for label in unique_labels:
        indices = np.where(labels == label)
        plt.scatter(cluster_transformed[indices, 0], cluster_transformed[indices, 1],
                    c=colors[label_to_color_index[label]], label=shape_labels[label_to_color_index[label]], s=50, alpha=0.2)
    
    
    # Plot the cluster centers and their respective circles
    for center_transformed, label in zip(cluster_centers_transformed, unique_labels):
        plt.scatter(center_transformed[0], center_transformed[1],
                    c='black', marker='x', s=100, linewidths=3)
        
        # Calculate radius as the maximum distance from the center to points in the cluster
        cluster_indices = np.where(labels == label)
        cluster_points_transformed = cluster_transformed[cluster_indices]
        # furthest_point = find_furthest_point(cluster_points_transformed, center_transformed)
        F1, F2, S, angle = calculate_ellipse_parameters_n_dimensional(cluster_points_transformed, center_transformed  )
        radius = np.max(np.linalg.norm(cluster_points_transformed - center_transformed, axis=1))
        # Find the location of the other end of the semi-major axis and consider it as F2.
        a = S / 2
    
        # Distance between foci
        d = distance(F1, F2)
        
        # Semi-minor axis
        b = np.sqrt(a**2 - (d / 2)**2)
        ellipse = Ellipse((center_transformed[0], center_transformed[1]), width=d, height=2 * b, angle=angle, lw=2, fc='None', color='r', fill=False, linestyle='--')
        circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
                            color='r', fill=False)
        point1 = plt.Circle((F1[0], F1[1]), 0.01, color='black')
        point2 = plt.Circle((F2[0], F2[1]), 0.01, color='black')
        plt.gca().add_patch(ellipse)
        plt.gca().add_patch(circle)
        plt.gca().add_patch(point1)
        plt.gca().add_patch(point2)
        circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
                            color='r', fill=False, linestyle='--')
        plt.gca().add_patch(circle)   
    
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
    
    
def visualize_feature_separation(values, labels):
    
    for i, elem in enumerate(values):
        if not isinstance(elem, (list, np.ndarray)):
           #elemnt ist none und soll entfernt werden
            values.remove(elem)
            labels.remove(labels[i])
            
    values = np.array(values)
    labels = np.array(labels)
    
    # Erstellen Sie eine Farbkodierung für die Labels
    unique_labels = np.unique(labels)
    
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
  
    color_dict = {label: color for label, color in zip(unique_labels, colors)}
    
    # Plotten Sie die Werte
    plt.figure(figsize=(10, 6))
    

    for label in unique_labels:
        indices = labels == label
        plt.scatter(values[indices],np.arange(len(values))[indices], color=color_dict[label], label=label)
    
    plt.xlabel('Values')
    plt.ylabel('Index')
    plt.title('Scatter Plot of Values with Different Colors for Labels')
    plt.legend(title='Labels')
    plt.grid(True)
    plt.show()
    
from helper.parsers import parse_ground_truth
from helper.features import get_circle_rectangle_features
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler


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
    print('cluster_centers:', cluster_centers, X_normalized)
    
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
        radius = np.max(np.linalg.norm(cluster_points_transformed - center_transformed, axis=1))
        
        circle = plt.Circle((center_transformed[0], center_transformed[1]), radius,
                            color='r', fill=False, linestyle='--')
        plt.gca().add_patch(circle)   
    
    # Set fixed limits for x and y axes
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    
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
    
from helper.parsers import parse_ground_truth
from helper.features import get_circle_rectangle_features, get_shape_no_shape_features
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler

# Der Input ist ein Set von vektoren, die das Cluster repräsentieren
def get_cluster_center(cluster: np.ndarray[np.ndarray]):
    # Calculate the mean of all points in the cluster
    cluster_center = np.mean(cluster, axis=0)
    return cluster_center

def get_hyper_sphere(cluster_center, cluster)->dict:
    # Calculate the radius of the hyper sphere
    radius = 0
    for point in cluster:
        distance = np.linalg.norm(cluster_center - point)
        if distance > radius:
            radius = distance
    return radius

    

def get_all_strokes_with_label(label:str, truth:dict)->list:
    strokes = []
    for item in truth:
        if label in item:
            strokes.append(item[label])
    return strokes

def define_clusters(file_path, strokes)->dict:
    truth = parse_ground_truth(file_path)
    circles = get_all_strokes_with_label('circle', truth)
    ellipses = get_all_strokes_with_label('ellipse', truth)
    rectangles = get_all_strokes_with_label('rectangle', truth)
    parallelograms = get_all_strokes_with_label('parallelogram', truth)
    line = get_all_strokes_with_label('line', truth)
    double_circles = get_all_strokes_with_label('double circle', truth)
    diamond = get_all_strokes_with_label('diamond', truth)
    circle_features = []
    rectangle_features = []
    ellipse_features = []
    parallelogram_features = []
    line_features = []
    double_circle_features = []
    diamond_features = []
    print('define clusters')
    cluster_centers = {'circle': [], 'rectangle': []}
    cluster_hyper_spheres = {'circle': [], 'rectangle': []}
    for circle in circles:
        print('circle')
        circle_features.append(get_circle_rectangle_features(circle, strokes)['features'])
    for rectangle in rectangles:
        print('rect')
        rectangle_features.append(get_circle_rectangle_features(rectangle, strokes)['features'])
    for ellipse in ellipses:
        print('ellipse')
        ellipse_features.append(get_circle_rectangle_features(ellipse, strokes)['features'])
        
    # for parallelogram in parallelograms:
    #     print('para')
    #     parallelogram_features.append(get_feature_vector(parallelogram, strokes))
    # for double_circle in double_circles:
    #     print('double')
    #     double_circle_features.append(get_feature_vector(double_circle, strokes))
    # for line_ in line:
    #     print('line')
    #     line_features.append(get_shape_no_shape_features(line_, strokes)['features'])
    # for diamond in diamond:
    #     print('diamond')
    #     diamond_features.append(get_shape_no_shape_features(diamond, strokes)['features'])
        
    # cluster_centers['circle'] = get_cluster_center(circle_features)
    # cluster_centers['rectangle'] = get_cluster_center(rectangle_features)
    # cluster_hyper_spheres['circle'] = get_hyper_sphere(cluster_centers['circle'], circle_features)
    # cluster_hyper_spheres['rectangle'] = get_hyper_sphere(cluster_centers['rectangle'], rectangle_features)
    
    return circle_features, rectangle_features, ellipse_features
    
    
def visualize_clusters(X, labels):
    print('visualize clusters', X, labels)
    # transform the data to be within a specified range to avoid biasing the MDS results towards features with larger ranges.
    scaler = MinMaxScaler()
    # print('X', X)
    # for feature_vector in X:
        
    X_normalized = scaler.fit_transform(X)
    dissimilarity_matrix = pairwise_distances(X_normalized, metric='euclidean')
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    cluster_transformed = mds.fit_transform(dissimilarity_matrix)
    plt.figure(figsize=(10, 8))
    # colors = ['green', 'blue', 'yellow', 'red', 'black', 'purple', 'orange']
    colors = ['green', 'blue', 'yellow']
    # shape_labels = ['circle', 'rectangle', 'ellipse', 'parallelogram', 'line', 'double circle', 'diamond']
    shape_labels = ['circle', 'rectangle', 'ellipse']
    for label in np.unique(labels):
        indices = np.where(labels == label)
        plt.scatter(cluster_transformed[indices, 0], cluster_transformed[indices, 1],
        c=colors[label], label=shape_labels[label], s=50, alpha=0.2)
    
    # Add a legend
    plt.legend(loc='upper left')
    # plt.colorbar()
    # plt.title('MDS Projection')
    # plt.xlabel('Component 1')
    # plt.ylabel('Component 2')
    plt.grid(True)
    plt.show()
#     we use Multi-Dimensional Scaling (MDS)
#     (Torgerson 1952) to reduce the dimensions to 2 for plotting
    
    # # Save the clusters to a file
    # with open('clusters.pkl', 'wb') as f:
    #     pickle.dump((cluster_centers), f)
        
    # Load the clusters from the file
    # with open('clusters.pkl', 'rb') as f:
    #     cluster_centers, labels = pickle.load(f)
    
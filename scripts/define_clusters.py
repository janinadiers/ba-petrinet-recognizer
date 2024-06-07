from helper.parsers import parse_ground_truth, parse_strokes_from_inkml_file
from helper.features import get_feature_vector
import numpy as np
import pickle
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances


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
    # print(truth)
    # loop through the truth and check if a key is in the item dict
    circles = get_all_strokes_with_label('circle', truth)
    circles.extend(get_all_strokes_with_label('ellipse', truth))
    rectangles = get_all_strokes_with_label('rectangle', truth)
    circle_features = []
    rectangle_features = []
    cluster_centers = {'circle': [], 'rectangle': []}
    cluster_hyper_spheres = {'circle': [], 'rectangle': []}
    for circle in circles:
        circle_features.append(get_feature_vector(circle, strokes))
    for rectangle in rectangles:
        rectangle_features.append(get_feature_vector(rectangle, strokes))
    
    cluster_centers['circle'] = get_cluster_center(circle_features)
    cluster_centers['rectangle'] = get_cluster_center(rectangle_features)
    cluster_hyper_spheres['circle'] = get_hyper_sphere(cluster_centers['circle'], circle_features)
    cluster_hyper_spheres['rectangle'] = get_hyper_sphere(cluster_centers['rectangle'], rectangle_features)
    
    return circle_features, rectangle_features
    
    
def visualize_clusters(cluster):
    dissimilarity_matrix = pairwise_distances(cluster, metric='euclidean')
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    cluster_transformed = mds.fit_transform(dissimilarity_matrix)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(cluster_transformed[:, 0], cluster_transformed[:, 1], c=[i for i in range(len(cluster))], cmap='viridis', s=50)
    plt.colorbar()
    plt.title('MDS Projection')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
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
    
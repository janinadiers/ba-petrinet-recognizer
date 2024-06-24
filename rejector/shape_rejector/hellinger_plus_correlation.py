import numpy as np

# Ich denke der Input für die Funktion sollte ein Array von Punkten sein
def pearsons_correlation(x, y):
    # Calculate Pearson's correlation coefficient
    correlation_matrix = np.corrcoef(x, y)
    pearson_correlation = correlation_matrix[0, 1]
    return pearson_correlation



def hellinger_distance(P, Q):
    # Ensure P and Q are numpy arrays
    P = np.array(P)
    Q = np.array(Q)
    
    # Compute the Hellinger distance
    distance = np.sqrt(np.sum((np.sqrt(P) - np.sqrt(Q)) ** 2)) / np.sqrt(2)
    
    return distance


def use():
    pass
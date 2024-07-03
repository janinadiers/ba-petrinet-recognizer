import numpy as np

def get_neighbors(matrix, candidate_shape, neighbors):
    #  we want to extend the neighbors by the neighbors of the new added element in candidate_shape
    last_index = candidate_shape[-1]
    # an element can only be a neighbor, if it has a distance under the threshold (matrix[last_index] > 0) and it is not already recognized (matrix[last_index] < np.inf)
    potential_neighbors = np.where((matrix[last_index] > 0) & (matrix[last_index] < np.inf))[0]
    row = matrix[last_index]
    distances = row[potential_neighbors]
    sorted_potential_neighbors = potential_neighbors[np.argsort(distances)]
    # a neighbor should be added only if it is not already in the candidate_shape and not already in the neighbors
    new_neighbors = [n for n in sorted_potential_neighbors if n not in candidate_shape and n not in neighbors and matrix[n, n] == 0]
    neighbors.extend(new_neighbors)
    
    return neighbors


def group(unrecognized_strokes: list[dict], recognized_shapes: list[dict], strokes) -> list[dict]:
    # Loop over elements of recognized_shapes
    for shape in recognized_shapes:
        matrix = None
        neighbors = get_neighbors(matrix, shape, neighbors)
        # find spatial neighbors of the shape (hier braauchen wir aber nur die direkten Nachbarn der shape und nicht noch die Nachbarn der Nachbarn)
        
import itertools
import numpy as np
from typing import Callable
import time
    
def get_unrecognized_strokes(matrix:np.ndarray, strokes:list[dict]) -> list[dict]: 
    """ Returns the strokes that have an entry of 0 in the diagonal of the adjacency matrix"""
    unrecognized_strokes = []
    for i in range(matrix.shape[0]):
        if matrix[i, i] == 0:
            unrecognized_strokes.append(strokes[i])
    return unrecognized_strokes  

    
def get_neighbors(matrix, candidate_shape, neighbors, strokes):
    last_index = candidate_shape[-1]
    # Using NumPy to directly find non-zero elements which are not self-loops and not already in the shape
    potential_neighbors = np.where((matrix[last_index] > 0) & (np.arange(matrix.shape[0]) != last_index))[0]
    new_neighbors = [n for n in potential_neighbors if n not in candidate_shape and n not in neighbors]
    neighbors.extend(new_neighbors)
    return neighbors

def get_new_subsets(candidate_shape: list[int], new_stroke: int) -> set:
    # Ensure new_stroke is part of the candidate_shape
    if new_stroke not in candidate_shape:
        raise Exception("new_stroke is not part of the candidate_shape")

    # Generate all combinations of the candidate_shape
    all_combinations = set()
    for r in range(1, len(candidate_shape) + 1):  # start from 1 to include at least one element
        for combination in itertools.combinations(candidate_shape, r):
            all_combinations.add(frozenset(combination))

    return all_combinations


# Function to check if a subset (regardless of order) is in the list of subsets
def subset_already_checked(subset: frozenset, subsets: set) -> bool:
    return subset in subsets


def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    MAX_STROKE_LIMIT:int = 11
    current_stroke_limit:int = 5
    recognized_shapes:list[dict] = []
    checked_subsets = set()
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    
    while (current_stroke_limit < MAX_STROKE_LIMIT) and (current_stroke_limit <= len(strokes)):
        # every stroke in strokes should be a primary stroke at least once
        for stroke in strokes: 
            primary_stroke = stroke
            # strokes are stored with their index in the matrix, so we need to get the index of the primary stroke
            index_of_primary_stroke = strokes.index(primary_stroke)
            # Wir wollen keien stroke in shape candidate haben, der bereits erkannt wurde, also soll ein neuer primary stroke gewählt werden
            if matrix[index_of_primary_stroke, index_of_primary_stroke] == 1:
                continue
            
            candidate_shape:list[int] = [index_of_primary_stroke]
            found_shape = False
            neighbors:list[int] = []
            next_neighbor_index:int = 0
             
            # Die dritte bedingung wurde weggelassen, da ein stroke alleine ja auch eine gültige shape sein kann
            while (len(candidate_shape) <= current_stroke_limit) and (not found_shape):
                # Hier sollen alle neuen neighbors hinzugefügt werden, die nicht bereits in neighbors sind
                neighbors:list[int] = get_neighbors(matrix, candidate_shape, neighbors, strokes)
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    if not subset_already_checked(frozenset(candidate_shape), checked_subsets):
                        checked_subsets.add(frozenset(candidate_shape))
                        is_shape:dict = is_a_shape(candidate_shape, expected_shapes)
                        if 'valid' in is_shape:
                            # Update the diagonal entry to indicate recognition of the new shape
                            matrix[candidate_shape[0], candidate_shape[0]] = 1
                            recognized_shapes.append(is_shape['valid'])
                            found_shape = True    
                    break
                
                if next_neighbor_index > len(neighbors) -1:
                    break
                next_neighbour:int = neighbors[next_neighbor_index]
                candidate_shape.append(next_neighbour)
                next_neighbor_index += 1 
                 
                for subset in get_new_subsets(candidate_shape, candidate_shape[-1]):
                    if not subset_already_checked(frozenset(subset), checked_subsets):
                        checked_subsets.add(frozenset(subset))
                        is_shape = is_a_shape(subset, expected_shapes)
                        if 'valid' in is_shape:
                            for stroke_index in list(subset):
                                matrix[stroke_index, stroke_index] = 1
                                
                            recognized_shapes.append(is_shape['valid'])
                            found_shape = True
                              
        current_stroke_limit += 1      
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes}

import itertools
import numpy as np
from typing import Callable
    
def get_unrecognized_strokes(matrix:np.ndarray, strokes:list[dict]) -> list[dict]: 
    """ Returns the strokes that have an entry of 0 in the diagonal of the adjacency matrix"""
    unrecognized_strokes = []
    for i in range(matrix.shape[0]):
        if matrix[i, i] == 0:
            unrecognized_strokes.append(strokes[i])
    return unrecognized_strokes  


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


def get_new_subsets(candidate_shape: list[int], new_stroke: int) -> list[list[int]]:
    # Ensure new_stroke is part of the candidate_shape
    if new_stroke in candidate_shape:
        remaining_elements = [x for x in candidate_shape if x != new_stroke]
    else:
        Exception("new_stroke is not part of the candidate_shape")

    # Generate all combinations of the remaining elements
    all_combinations = []
    for r in range(len(remaining_elements) + 1):
        for combination in itertools.combinations(remaining_elements, r):
            # Add new_stroke to each combination
            all_combinations.append([new_stroke] + list(combination))
    return all_combinations


# Function to check if a subset (regardless of order) is in the list of subsets
def candidate_shape_already_created(candidate_shape: frozenset, created_candidate_shapes: set) -> bool:
    return candidate_shape in created_candidate_shapes


def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    MAX_STROKE_LIMIT:int = 12
    current_stroke_limit:int = 5
    recognized_shapes:list[dict] = []
    created_candidate_shapes = set()
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    recognizer_cache = {}
    counter = 0
    while (current_stroke_limit < MAX_STROKE_LIMIT) and (current_stroke_limit <= len(strokes)):
        # every stroke in strokes should be a primary stroke at least once
        for index,stroke in enumerate(strokes): 
            # Wir wollen keien stroke in shape candidate haben, der bereits erkannt wurde, also soll ein neuer primary stroke gewählt werden
            if matrix[index, index] == float('inf'):
                continue
            candidate_shape:list[int] = [index]
            found_shape = False
            neighbors:list[int] = []
            next_neighbor_index:int = 0
            
            # Die dritte bedingung wurde weggelassen, da ein stroke alleine ja auch eine gültige shape sein kann
            while (len(candidate_shape) <= current_stroke_limit) and (not found_shape):
                # Hier sollen alle neuen neighbors hinzugefügt werden, die nicht bereits in neighbors sind
                neighbors:list[int] = get_neighbors(matrix, candidate_shape, neighbors)
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    if not candidate_shape_already_created(frozenset(candidate_shape), created_candidate_shapes):
                        counter += 1
                        try:
                            # Zuerst wird geprüft, ob die shape bereits im cache ist, ansonsten kommen wir in die exception
                            is_shape = recognizer_cache[frozenset(candidate_shape)]
                        except KeyError:
                            is_shape = is_a_shape(candidate_shape, expected_shapes)
                            recognizer_cache[frozenset(candidate_shape)] = is_shape
                            if 'valid' in is_shape:
                                # Update the diagonal entry to indicate recognition of the new shape
                                matrix[candidate_shape[0], candidate_shape[0]] = float('inf')
                                recognized_shapes.append(is_shape['valid'])
                                found_shape = True 
                    break
                
                if next_neighbor_index > len(neighbors) -1:
                    break
                
                if not candidate_shape_already_created(frozenset(candidate_shape), created_candidate_shapes):
                    for subset in get_new_subsets(candidate_shape, candidate_shape[-1]):
                        counter += 1
                        try:
                            is_shape = recognizer_cache[frozenset(subset)]
                        except KeyError:
                            is_shape = is_a_shape(subset, expected_shapes)
                            recognizer_cache[frozenset(subset)] = is_shape
                            if 'valid' in is_shape:
                                for stroke_index in list(subset):
                                    matrix[stroke_index, stroke_index] = float('inf')
                                recognized_shapes.append(is_shape['valid'])
                                found_shape = True  
                created_candidate_shapes.add(frozenset(candidate_shape))  
                next_neighbour:int = neighbors[next_neighbor_index]
                candidate_shape.append(next_neighbour)
                next_neighbor_index += 1 
             
        current_stroke_limit += 1      
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes, 'counter': counter}

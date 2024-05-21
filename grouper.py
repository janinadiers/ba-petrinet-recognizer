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


def get_neighbors(matrix:np.ndarray, candidate_shape:list[int], neighbors:list[int]) -> list[int]:
    #  we want to extend the neighbors by the neighbors of the new added element in candidate_shape
    last_index = candidate_shape[-1]
    # an element can only be a neighbor, if it has a distance under the threshold (matrix[last_index] > 0) and it is not already recognized (matrix[last_index] < np.inf)
    potential_neighbors = np.where((matrix[last_index] > 0) & (matrix[last_index] < np.inf))[0]
    row = matrix[last_index]
    distances = row[potential_neighbors]
    # print('distances', distances, potential_neighbors)
    sorted_potential_neighbors = potential_neighbors[np.argsort(distances)]
    # a neighbor should be added only if it is not already in the candidate_shape and not already in the neighbors
    new_neighbors = [n for n in sorted_potential_neighbors if n not in candidate_shape and n not in neighbors and matrix[n, n] == 0]
    neighbors.extend(new_neighbors)
    print('neighbors', neighbors, candidate_shape)
    return neighbors

def generate_shape_candidates(matrix:np.ndarray) -> list[list[int]]:
    shape_candidates = [[[i] for i in range(len(matrix))]] # [[[0],[1],2,3,4,5], []...]
    print('shape_candidates', shape_candidates)
    for i in range(len(matrix)): # 0,1,2,3,4,5
        for j in range(len(shape_candidates[-1])): 
            neighbors = get_neighbors(matrix, [shape_candidates[i][j][-1]], [])
            for neighbor in neighbors:
                if j+1 > len(shape_candidates) -1: 
                    shape_candidates.append([])
                new_candidate = shape_candidates[i][j].copy()
                new_candidate.append(neighbor)
                shape_candidates[j+1].append(new_candidate)
                print('shape_candidates', shape_candidates)

def get_new_subsets(candidate_shape: list[int], new_stroke: int, matrix) -> list[list[int]]:
    # Ensure new_stroke is part of the candidate_shape
    if new_stroke in candidate_shape:
        remaining_elements = [x for x in candidate_shape if x != new_stroke]
    else:
        Exception("new_stroke is not part of the candidate_shape")

    # Generate all combinations of the remaining elements
    all_combinations = []
    for r in range(len(remaining_elements) + 1):
        for combination in itertools.combinations(remaining_elements, r):
            # prüfen, ob alle elemente in combination eine Verbindung haben
            combination_is_coherent_path = True
            combination = [new_stroke] + list(combination)
            
            for i in range(len(combination) -1):
                current = combination[i]
                next_elem = combination[i+1]
                if matrix[current, next_elem] == 0:
                    combination_is_coherent_path = False
                    
            # Add new_stroke to each combination
            if combination_is_coherent_path:
                all_combinations.append(combination)
    return all_combinations


# Function to check if a subset (regardless of order) is in the list of subsets
def candidate_shape_already_created(candidate_shape: frozenset, created_candidate_shapes: set) -> bool:
    return candidate_shape in created_candidate_shapes

def subset_already_created(subset: frozenset, created_subsets: set) -> bool:
    # print('created_subsets', created_subsets, subset)
    return subset in created_subsets

def subset_is_circular(matrix, subset):
    
    # Es sollen immer alle subsets der Größe 1 oder 2 geprüft werden, ob sie eine gültige shape sind
    if len(subset) < 3:
        return True
    if matrix[subset[0], subset[-1]] > 0:
        return True
    return False

    
def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    MAX_STROKE_LIMIT:int = 11
    current_stroke_limit:int = 5
    recognized_shapes:list[dict] = []
    created_candidate_shapes = set()
    created_subsets = set()
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)  
    recognizer_calls = 0
    
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
                # print('candidate_shape', candidate_shape, candidate_shape_already_created(frozenset(candidate_shape), created_candidate_shapes))
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    if not candidate_shape_already_created(frozenset(candidate_shape), created_candidate_shapes):
                        recognizer_calls += 1
                        is_shape = is_a_shape(candidate_shape, expected_shapes)
                        if 'valid' in is_shape:
                            # Update the diagonal entry to indicate recognition of the new shape
                            matrix[candidate_shape[0], candidate_shape[0]] = float('inf')
                            recognized_shapes.append(is_shape['valid'])
                            found_shape = True 
                            print('found_shape', is_shape['valid'])
                    
                    break
                
                if next_neighbor_index > len(neighbors) -1:
                    break
                
                
                if not candidate_shape_already_created(frozenset(candidate_shape), created_candidate_shapes):
                    for subset in get_new_subsets(candidate_shape, candidate_shape[-1], matrix):
                        
                        
                        if not subset_already_created(frozenset(subset), created_subsets) and subset_is_circular(matrix, subset):
                            recognizer_calls += 1
                            is_shape = is_a_shape(subset, expected_shapes)
                            created_subsets.add(frozenset(subset))
                            if 'valid' in is_shape:
                                for stroke_index in list(subset):
                                    matrix[stroke_index, stroke_index] = float('inf')
                                recognized_shapes.append(is_shape['valid'])
                                found_shape = True 
                                print('found_shape', is_shape['valid'])

                
                    
                created_candidate_shapes.add(frozenset(candidate_shape))  
                next_neighbour:int = neighbors[next_neighbor_index]
                candidate_shape.append(next_neighbour)
                next_neighbor_index += 1 
             
        current_stroke_limit += 1      
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes, 'recognizer calls': recognizer_calls}

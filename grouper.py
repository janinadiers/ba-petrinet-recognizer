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
    
def find_neighbors(matrix:np.ndarray, stroke_index:int) -> list[int]:
    """ Returns the indices of the neighbors of the given stroke_index which not already belong to a recognized shape"""
    neighbors = np.where((matrix[stroke_index] == 1) & (matrix[stroke_index][stroke_index] != 1))[0]
    return neighbors

def get_all_subsets(candidate_shape:list[int]) -> list[list[int]]:
    all_subsets = list(itertools.chain.from_iterable(itertools.combinations(candidate_shape, r) for r in range(1, len(candidate_shape)+1)))
    return all_subsets


# Function to check if a subset (regardless of order) is in the list of subsets
def subset_already_checked(subset, subsets):
    for existing_subset in subsets:
        if sorted(existing_subset) == sorted(subset):
            return True
    return False

def get_ids_from_index(subset, strokes):
    stroke_ids = []
    for index in subset:
        stroke_ids.append(int(next(iter(strokes[index]))))
    return stroke_ids


def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    
    MAX_STROKE_LIMIT:int = 6
    current_stroke_limit:int = 5 
    recognized_shapes:list[dict] = []
    checked_subsets:list[list[int]] = []
    
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    while current_stroke_limit < MAX_STROKE_LIMIT:
        # set next stroke as primary stroke and add it to the new candidate shape
        for stroke in strokes: 
            primary_stroke = stroke
            index_of_primary_stroke = strokes.index(primary_stroke)
            if matrix[index_of_primary_stroke, index_of_primary_stroke] == 1:
                continue
            candidate_shape:list[int] = [index_of_primary_stroke]
            found_shape = False
            neighbors:list[int] = find_neighbors(matrix, index_of_primary_stroke)
            next_neighbor_index = 0
            
            while (len(candidate_shape) < current_stroke_limit) and (not found_shape) and next_neighbor_index < len(neighbors):
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    is_shape:dict = is_a_shape(candidate_shape, expected_shapes)
                    if 'valid' in is_shape:
                        # Update the diagonal entry to indicate recognition of the new shape
                        matrix[candidate_shape[0], candidate_shape[0]] = 1
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                    break
                
                next_neighbour:int = neighbors[next_neighbor_index]
                candidate_shape.append(next_neighbour)
                for subset in get_all_subsets(candidate_shape):
                    if subset_already_checked(subset, checked_subsets):
                        continue
                    subset_with_ids = get_ids_from_index(subset, strokes)
                    is_shape = is_a_shape(subset_with_ids, expected_shapes)
                    if 'valid' in is_shape:
                        for stroke_index in list(subset):
                            # Update the diagonal entry to indicate recognition of the new shape
                            matrix[stroke_index, stroke_index] = 1
                            
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                        checked_subsets.append(subset)
                next_neighbor_index += 1
        current_stroke_limit += 1     
        
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes}

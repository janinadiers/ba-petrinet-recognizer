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

    
def get_neighbors(matrix:np.ndarray, candidate_shape:list[int], neighbors:list[int], strokes) -> list[int]:
    """ Returns the indices of the neighbors of the given stroke_index which not already belong to a recognized shape"""
    new_neighbors = list(neighbors)
    neighbors_of_stroke = np.where((matrix[candidate_shape[-1]] > 0) & (matrix[candidate_shape[-1]][candidate_shape[-1]] != 1))[0]
    for neighbor in neighbors_of_stroke:
        if neighbor not in new_neighbors and neighbor not in candidate_shape and matrix[neighbor, neighbor] != 1:
            new_neighbors.append(neighbor)
    return new_neighbors

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
def subset_already_checked(subset, subsets):
    for existing_subset in subsets:
        if sorted(existing_subset) == sorted(subset):
            return True
    return False

# def get_ids(subset, strokes):
#     stroke_ids = []
#     for index in subset:
#         stroke_ids.append(int(next(iter(strokes[index]))))
#     return stroke_ids

def get_ids(subset, strokes):
    return [next(iter(strokes[index])) for index in subset]


def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    MAX_STROKE_LIMIT:int = 11
    current_stroke_limit:int = 5
    recognized_shapes:list[dict] = []
    checked_subsets:list[list[int]] = []
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
                start_time = time.time()  # Start timing
                neighbors:list[int] = get_neighbors(matrix, candidate_shape, neighbors, strokes)
                end_time = time.time()  # End timing
                # print(f" get_neighbors Function ran for {end_time - start_time} seconds")
                
                # print('neighbors', len(neighbors))
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    subset_with_ids = get_ids(candidate_shape, strokes)
                    is_shape:dict = is_a_shape(subset_with_ids, expected_shapes)
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
                    if subset_already_checked(subset, checked_subsets):
                        continue
                    
                    # because the subset contains a list of stroke indices, we need to get the corresponding stroke ids from strokes
                    # The recognizer expects a list of stroke ids, so we need to convert the indices to ids
                    # This is because we cannot be sure, that the indices of the strokes are the same as the ids
                    # Which they are not since the text is removed manually
                    start_time = time.time()  # Start timing
                    subset_with_ids = get_ids(subset, strokes)
                    end_time = time.time()  # End timing
                    print(f" get_ids Function ran for {end_time - start_time} seconds")
                    start_time = time.time()  # Start timing
                    is_shape = is_a_shape(subset_with_ids, expected_shapes)
                    end_time = time.time()  # End timing
                    # print(f"is_a_shape Function ran for {end_time - start_time} seconds")
                    if 'valid' in is_shape:
                        for stroke_index in list(subset):
                            matrix[stroke_index, stroke_index] = 1
                            
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                        checked_subsets.append(subset)
                
                  
                
                
        current_stroke_limit += 1      
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes}

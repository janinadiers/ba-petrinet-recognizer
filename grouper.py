import itertools
import numpy as np
from typing import Callable
import time
from export_points_to_inkml import export_points_to_inkml

average_time_for_initialization = 0
    
def get_unrecognized_strokes(matrix:np.ndarray, strokes:list[dict]) -> list[dict]: 
    """ Returns the strokes that have an entry of 0 in the diagonal of the adjacency matrix"""
    unrecognized_strokes = []
    for i in range(matrix.shape[0]):
        if matrix[i, i] == 0:
            unrecognized_strokes.append(strokes[i])
    return unrecognized_strokes  


    
def get_neighbors(matrix:np.ndarray, candidate_shape:list[int], neighbors:list[int]) -> list[int]:
    """ Returns the indices of the neighbors of the given stroke_index which not already belong to a recognized shape"""
    new_neighbors = list(neighbors)
    for stroke_index in candidate_shape:
        neighbors_of_stroke = np.where((matrix[stroke_index] == 1) & (matrix[stroke_index][stroke_index] != 1))[0]
        for neighbor in neighbors_of_stroke:
            if neighbor not in new_neighbors and neighbor not in candidate_shape:
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

def get_ids_from_index(subset, strokes):
    stroke_ids = []
    for index in subset:
        stroke_ids.append(int(next(iter(strokes[index]))))
    return stroke_ids

def get_average_time_for_initialization():
    global average_time_for_initialization
    return average_time_for_initialization

def is_direct_successor(num1, num2):
    return num2 == num1 + 1

def shape_candidate_has_only_strokes_in_temporal_order_with_only_one_exception(candidate_shape:list[int]) -> dict:
    """Checks if the strokes in the candidate shape are temporally concurrent with only one exception"""
    exception_exists = False
    for index in candidate_shape:
        if is_direct_successor(index, index + 1):
            continue
        else:
            if exception_exists:
                return False
            exception_exists = True
    return True



def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    global average_time_for_initialization
    MAX_STROKE_LIMIT:int = 11
    current_stroke_limit:int = 5 
    recognized_shapes:list[dict] = []
    checked_subsets:list[list[int]] = []
    start_time = time.time()  # Startzeit speichern
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    end_time = time.time()  # Endzeit speichern
    average_time_for_initialization += end_time - start_time
    
    while (current_stroke_limit < MAX_STROKE_LIMIT) and (MAX_STROKE_LIMIT <= len(strokes)):
        # every stroke in strokes should be a primary stroke at least once
        for stroke in strokes: 
            primary_stroke = stroke
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
                neighbors:list[int] = get_neighbors(matrix, candidate_shape, neighbors)
                # falls ein stroke keinen Nachbarn hat soll trotzdem geprüft werden, ob er alleine eine gültige shape ist
                if(len(neighbors) == 0):
                    is_shape:dict = is_a_shape(candidate_shape, expected_shapes)
                    if 'valid' in is_shape:
                        # Update the diagonal entry to indicate recognition of the new shape
                        matrix[candidate_shape[0], candidate_shape[0]] = 1
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                    break
                
                for subset in get_new_subsets(candidate_shape, candidate_shape[-1]):
                    if subset_already_checked(subset, checked_subsets):
                        continue
                    
                    # because the subset contains a list of stroke indices, we need to get the corresponding stroke ids from strokes
                    # The recognizer expects a list of stroke ids, so we need to convert the indices to ids
                    # This is because we cannot be sure, that the indices of the strokes are the same as the ids
                    subset_with_ids = get_ids_from_index(subset, strokes)
                    is_shape = is_a_shape(subset_with_ids, expected_shapes)
                    if 'valid' in is_shape:
                        for stroke_index in list(subset):
                            matrix[stroke_index, stroke_index] = 1
                            
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                        checked_subsets.append(subset)
                
                if next_neighbor_index >= len(neighbors):
                    break
                next_neighbour:int = neighbors[next_neighbor_index]
                next_neighbor_index += 1 
                if shape_candidate_has_only_strokes_in_temporal_order_with_only_one_exception(candidate_shape):
                    candidate_shape.append(next_neighbour)    
                else:
                    print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ELSE') 
                
        current_stroke_limit += 1      
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes}

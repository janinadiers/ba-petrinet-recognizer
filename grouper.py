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
    
def find_neighbors(matrix:np.ndarray, stroke_index:int) -> list[int]:
    """ Returns the indices of the neighbors of the given stroke_index which not already belong to a recognized shape"""
    # Filter out tuples where the first element is 1
    filtered_tuples = []
    for i, item in enumerate(matrix[stroke_index]):
        if type(item) == tuple and item[0] == 1:
            new_tuple = item + (i,)
            filtered_tuples.append(new_tuple)
    print('filtered_tuples: ', filtered_tuples)
    # Sort the filtered tuples by the distance value (second element of tuple)
    neighbors = sorted(filtered_tuples, key=lambda x: x[1])
    print('sorted neighbors: ', neighbors)
    result = []
    for neighbor in neighbors:
        result.append(neighbor[2])
        
    return result

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

def get_average_time_for_initialization():
    global average_time_for_initialization
    return average_time_for_initialization



def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    global average_time_for_initialization
    MAX_STROKE_LIMIT:int = 6
    current_stroke_limit:int = 5 
    recognized_shapes:list[dict] = []
    checked_subsets:list[list[int]] = []
    start_time = time.time()  # Startzeit speichern
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    end_time = time.time()  # Endzeit speichern
    average_time_for_initialization += end_time - start_time
    
    while (current_stroke_limit < MAX_STROKE_LIMIT) and (MAX_STROKE_LIMIT <= len(strokes)):
        # set next stroke as primary stroke and add it to the new candidate shape
        for stroke in strokes: 
            primary_stroke = stroke
            index_of_primary_stroke = strokes.index(primary_stroke)
            # Wir wollen keien stroke in shape candidate haben, der bereits erkannt wurde, also soll ein neuer primary stroke gewählt werden
            if matrix[index_of_primary_stroke, index_of_primary_stroke] == 1:
                continue
            
            candidate_shape:list[int] = [index_of_primary_stroke]
            found_shape = False
            # Im ursprünglichen Algorithmus werden die Nachbarn erst in der While loop berechnet und zwar jedes mal neu, weil sich ja beim hinzufügen von neuen strokes in candidate_shape auch die Nachbarn ändern
            # Ich berechne die Nachbarn einmalig und speichere sie in einer Liste, um die Berechnung zu beschleunigen. Verzichte also darauf auch die Nachbarn der Nachbarn zu berechnen, ob sich das nachteilig auf die Erkennung auswirkt, müsste genauer untersucht werden
            neighbors:list[int] = find_neighbors(matrix, index_of_primary_stroke)
            next_neighbor_index = 0
            print('neighbors: ', len(neighbors))
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
                        print('subset already checked')
                        continue
                    
                    # because the subset contains a list of stroke indices, we need to get the corresponding stroke ids from strokes
                    # The recognizer expects a list of stroke ids, so we need to convert the indices to ids
                    # This is because we cannot be sure, that the indices of the strokes are the same as the ids
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

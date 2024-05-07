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
    neighbors = np.where((matrix[stroke_index] == 1) & (matrix[stroke_index][stroke_index] != 1))[0]

    return neighbors


def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    MAX_STROKE_LIMIT:int = 6
    current_stroke_limit:int = 5 
    recognized_shapes:list[dict] = []
    
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)
    while current_stroke_limit < MAX_STROKE_LIMIT:
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
                all_subsets = list(itertools.chain.from_iterable(itertools.combinations(candidate_shape, r) for r in range(1, len(candidate_shape)+1)))
                for subset in all_subsets:
                    is_shape = is_a_shape(subset, expected_shapes)
                    if 'valid' in is_shape:
                        for stroke_index in list(subset):
                            # Update the diagonal entry to indicate recognition of the new shape
                            matrix[stroke_index, stroke_index] = 1
                            
                        recognized_shapes.append(is_shape['valid'])
                        found_shape = True
                next_neighbor_index += 1
        current_stroke_limit += 1     
        
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    print('recognized shapes: ', recognized_shapes)
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes}

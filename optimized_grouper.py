import numpy as np
from typing import Callable
import networkx as nx
    
def get_unrecognized_strokes(matrix:np.ndarray, strokes:list[dict]) -> list[dict]: 
    """ Returns the strokes that have an entry of 0 in the diagonal of the adjacency matrix"""
    unrecognized_strokes = []
    for i in range(matrix.shape[0]):
        if matrix[i, i] == 0:
            unrecognized_strokes.append(strokes[i])
    return unrecognized_strokes  


def get_all_simple_cycles(adj_matrix):
    G = nx.Graph()

    # Benachbarte Strokes hinzufügen
    for i in range(len(adj_matrix)):
        for j in range(i , len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
                
    # Finde alle einfachen Zyklen
    to_directed = G.to_directed()
    
    simple_cycles = nx.simple_cycles(to_directed, length_bound=8)
    
    # Store unique cycles
    unique_cycles = []
    seen = set()
    for cycle in simple_cycles:
        # Sort the cycle to canonical form and use a tuple to make it hashable
        normalized_cycle = tuple(sorted(cycle))
        if normalized_cycle not in seen:
            seen.add(normalized_cycle)
            unique_cycles.append(cycle)
    return unique_cycles
    

  
def group(strokes:list[dict], is_a_shape:Callable, initialize_adjacency_matrix:Callable, expected_shapes:list[dict]) -> dict:
    recognized_shapes:list[dict] = []
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)  
    recognizer_calls = 0
    cycles = get_all_simple_cycles(matrix)
            
    for cycle in cycles:
        recognizer_calls += 1
        is_shape = is_a_shape(cycle, expected_shapes)
        if 'valid' in is_shape:
            recognized_shapes.append(is_shape['valid'])
          
               
    unrecognized_strokes = get_unrecognized_strokes(matrix, strokes)
    
    return {'recognized shapes': recognized_shapes, 'unrecognized strokes': unrecognized_strokes, 'recognizer calls': recognizer_calls}

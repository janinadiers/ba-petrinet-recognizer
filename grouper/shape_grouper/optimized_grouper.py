import numpy as np
import networkx as nx
from grouper.shape_grouper.distance_calculators.distance_between_all_points import initialize_adjacency_matrix

def sort_by_length(strokes:list[dict]) -> list[dict]:
    strokes.sort(key=lambda x: len(x))
    return strokes
    
def get_all_simple_cycles(adj_matrix):
    G = nx.Graph()
    # Benachbarte Striche hinzufügen
    for i in range(len(adj_matrix)):
        for j in range(i , len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    
    to_directed = G.to_directed()
    simple_cycles = nx.simple_cycles(to_directed, length_bound=8)
    unique_cycles = []
    seen = set()
    for cycle in simple_cycles:
        normalized_cycle = tuple(sorted(cycle))
        if normalized_cycle not in seen:
            seen.add(normalized_cycle)
            unique_cycles.append(cycle)
    
            
    return sort_by_length(unique_cycles)  
    

  
def group(strokes:list[dict]) -> dict:
    matrix:np.ndarray = initialize_adjacency_matrix(strokes)  
    return get_all_simple_cycles(matrix)

            
 
          
               
    

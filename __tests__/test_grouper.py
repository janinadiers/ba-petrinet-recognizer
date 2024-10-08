import unittest
from grouper.shape_grouper.optimized_grouper import get_all_simple_cycles
from grouper.shape_grouper.thesis_grouper import get_new_subsets, candidate_shape_already_created, get_neighbors, get_unrecognized_strokes
import numpy as np

class TestGrouperMethods(unittest.TestCase):
    
    def test_get_all_simple_cycles(self):
        # generate a matrix of 6 by 6 with 0 an 1
        matrix = np.zeros((6, 6), dtype=int)
        matrix[0, 0] = 1
        matrix[0, 1] = 1
        matrix[0, 2] = 0
        matrix[0, 3] = 0
        matrix[0, 4] = 1
        matrix[0, 5] = 0
        
        matrix[1, 0] = 1
        matrix[1, 1] = 1
        matrix[1, 2] = 1
        matrix[1, 3] = 0
        matrix[1, 4] = 1
        matrix[1, 5] = 0
        
        matrix[2, 0] = 0
        matrix[2, 1] = 1
        matrix[2, 2] = 1
        matrix[2, 3] = 0
        matrix[2, 4] = 1
        matrix[2, 5] = 0
        
        matrix[3, 0] = 0
        matrix[3, 1] = 0
        matrix[3, 2] = 0
        matrix[3, 3] = 1
        matrix[3, 4] = 1
        matrix[3, 5] = 0
        
        matrix[4, 0] = 1
        matrix[4, 1] = 1
        matrix[4, 2] = 1
        matrix[4, 3] = 1
        matrix[4, 4] = 1
        matrix[4, 5] = 0
        
        matrix[5, 0] = 0
        matrix[5, 1] = 0
        matrix[5, 2] = 0
        matrix[5, 3] = 0
        matrix[5, 4] = 0
        matrix[5, 5] = 1
        
       
       
        simple_cycles = get_all_simple_cycles(matrix)
        self.assertTrue(has_duplicates(simple_cycles) == False)
        self.assertTrue(has_duplicates([[3], [1, 3], [3, 1], [3, 2], [2, 3]]) == True)
        print('hiiier: ', simple_cycles)
        # self.assertEqual(simple_cycles, [[0], [1], [4], [2], [3], [5], [0,1], [0,1,2,4], [0,1,4], [0,4], [1,2], [1,2,4], [1,4], [2,4], [3,4]])
        

    # def test_get_new_subsets(self):
    #     self.assertEqual(get_new_subsets([1, 2, 3], 3), [[3],[3,1], [3, 2], [3, 1, 2]])
    #     self.assertNotEqual(get_new_subsets([1, 2, 3], 3), [[3], [1, 3], [3, 1], [3, 2], [2, 3], [3, 2, 1], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    #     self.assertNotEqual(get_new_subsets([1, 2, 3], 3), [[1], [2], [3], [1, 2],[1, 3], [2, 3], [1, 2, 3]])
    #     self.assertEqual(get_new_subsets([2, 3, 1], 1), [[1], [1,2], [1, 3], [1,2, 3]])
    
    # def test_candidate_shape_already_created(self):
    #     subsets = {frozenset([1, 2, 3]), frozenset([1, 2, 3, 4]), frozenset([1, 2, 7])}
    #     # These should return True as [1, 2, 3] and any permutation of it should already be recognized
    #     self.assertTrue(candidate_shape_already_created(frozenset([1, 2, 3]), subsets))
    #     self.assertTrue(candidate_shape_already_created(frozenset([2, 3, 1]), subsets))
    #     # These should return False as they are not in the original set of subsets
    #     self.assertFalse(candidate_shape_already_created(frozenset([4, 8]), subsets))
    #     self.assertFalse(candidate_shape_already_created(frozenset([6, 7, 9]), subsets))
        
   
    
    
    # def test_get_neighbors(self):
    #     expected_matrix = np.zeros((5, 5), dtype=int)
    #     expected_matrix[0, 0] = 0
    #     expected_matrix[0, 1] = 100
    #     expected_matrix[0, 2] = 50
    #     expected_matrix[0, 3] = 0
    #     expected_matrix[0,4] = 230
    #     expected_matrix[1, 0] = 100
    #     expected_matrix[1, 1] = 0
    #     expected_matrix[1, 2] = 200
    #     expected_matrix[1, 3] = 0
    #     expected_matrix[1,4] = 0
    #     expected_matrix[2, 0] = 50
    #     expected_matrix[2, 1] = 200
    #     expected_matrix[2, 2] = 0
    #     expected_matrix[2, 3] = 400
    #     expected_matrix[2,4] = 0
    #     expected_matrix[3, 0] = 0
    #     expected_matrix[3, 1] = 0
    #     expected_matrix[3, 2] = 400
    #     expected_matrix[3, 3] = 0
    #     expected_matrix[3,4] = 80
    #     expected_matrix[4,0] = 230
    #     expected_matrix[4,1] = 0
    #     expected_matrix[4,2] = 0
    #     expected_matrix[4,3] = 80
    #     expected_matrix[4,4] = 0
        
    #     expected_result1 = np.array([2, 1, 4])
    #     expected_result2 = np.array([2,1,4,3])
    #     expected_result3 = np.array([2,1,4,3])
        
    #     np.testing.assert_array_equal(get_neighbors(expected_matrix, [0], []), expected_result1)
    #     np.testing.assert_array_equal(get_neighbors(expected_matrix, [0,2], [2,1,4]), expected_result2)
    #     np.testing.assert_array_equal(get_neighbors(expected_matrix, [0,2,1], [2,1,4,3]), expected_result3)
    #     np.testing.assert_array_equal(get_neighbors(expected_matrix, [0,2,1,4], [2,1,4,3]), expected_result3)


    # def test_get_unrecognized_strokes(self):
        
    #     strokes:list[dict] = [{'0': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}, 
    #                {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 8, 'y': 10, 't': 2}]},
    #                {'2': [{'x': 6, 'y': 0, 't': 0}, {'x': 9, 'y': 4, 't': 1}, {'x': 20, 'y': 8, 't': 2}]},
    #                {'3': [{'x': 3000, 'y': 4000, 't': 0}, {'x': 3400, 'y': 8000, 't': 1}, {'x': 6000, 'y': 1200, 't': 2}]}]
        
    #     expected_matrix = np.zeros((4, 4), dtype=int)
    #     expected_matrix[0, 0] = 0
    #     expected_matrix[0, 1] = 1
    #     expected_matrix[0, 2] = 1
    #     expected_matrix[0, 3] = 0
    #     expected_matrix[1, 0] = 0
    #     expected_matrix[1, 1] = 1
    #     expected_matrix[1, 2] = 1
    #     expected_matrix[1, 3] = 0
    #     expected_matrix[2, 0] = 0
    #     expected_matrix[2, 1] = 0
    #     expected_matrix[2, 2] = 1
    #     expected_matrix[2, 3] = 0
    #     expected_matrix[3, 0] = 0
    #     expected_matrix[3, 1] = 0
    #     expected_matrix[3, 2] = 0
    #     expected_matrix[3, 3] = 0
        
    #     expected_result1 = [{'0': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}, {'3': [{'x': 3000, 'y': 4000, 't': 0}, {'x': 3400, 'y': 8000, 't': 1}, {'x': 6000, 'y': 1200, 't': 2}]}]
    #     self.assertEqual(get_unrecognized_strokes(expected_matrix, strokes), expected_result1)
        

def has_duplicates(lists):
    # Sortiere jede Liste in der Liste von Listen
    sorted_lists = [sorted(sublist) for sublist in lists]
    
    # Erstelle ein Set zum Überprüfen der Einzigartigkeit
    seen = set()
    
    for sublist in sorted_lists:
        # Konvertiere jede sortierte Liste in ein Tuple, da Sets nur unveränderliche (hashable) Typen akzeptieren
        sublist_tuple = tuple(sublist)
        
        if sublist_tuple in seen:
            # Wenn das Tuple bereits im Set ist, gibt es ein Duplikat
            return True
        
        # Füge das Tuple zum Set hinzu
        seen.add(sublist_tuple)
    
    # Wenn keine Duplikate gefunden wurden, gib False zurück
    return False        

if __name__ == '__main__':
    unittest.main()
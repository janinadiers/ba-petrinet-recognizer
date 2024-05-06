import unittest
from helpers import count_common_elements, trace_ids_are_unique, count_different_elements

class TestHelperMethods(unittest.TestCase):

    def test_count_common_elements(self):
        list1 = [{'a': [1,6]}, {'b': [2]}, {'c': [3,8]}]
        list2 = [{'b': [2]}, {'c': [3,8]}, {'d': [4]}]
        self.assertEqual(count_common_elements(list1, list2), 2)
    
    def test_count_different_elements(self):
        list1 = [{'a': [1,6]}, {'b': [2]}, {'c': [3,8]}, {'e': [5]}, {'f': [6]}]
        list2 = [{'b': [2]}, {'c': [3,8]}, {'d': [4]}]
        self.assertEqual(count_different_elements(list1, list2), 3)
    
    def test_trace_ids_are_unique(self):
        list1 = [{'a': [1,6]}, {'b': [2]}, {'c': [3,8]}]
        list2 = [{'b': [2]}, {'c': [2,8]}, {'d': [4]}]
        list3 = [{'b': [2]}, {'c': [3,8]}, {'d': [4]}]
        list4 = [{'b': [2]}, {'c': [3,8]}, {'d': [4, 2]}]
        
        self.assertEqual(trace_ids_are_unique(list1), True)
        self.assertEqual(trace_ids_are_unique(list2), False)
        self.assertEqual(trace_ids_are_unique(list3), True)
        self.assertEqual(trace_ids_are_unique(list4), False)
        
        
       
        
    

if __name__ == '__main__':
    unittest.main()
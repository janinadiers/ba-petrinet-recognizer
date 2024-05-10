import unittest
from recognizer.perfectMockRecognizer import is_a_shape
class TestPerfectMockRecognizerMethods(unittest.TestCase):

    def test_is_a_shape(self):
        grouped_ids = [[27], [32,5], [28, 13]]
        expected_shapes = [{'circle': [27]}, {'circle': [2]}, {'circle': [5]}, {'circle': [28, 13]}]
        self.assertEqual(is_a_shape(grouped_ids[0], expected_shapes), {'valid': {'circle': [27]}})
        self.assertEqual(is_a_shape(grouped_ids[1], expected_shapes), {'invalid': [32,5]})
        self.assertEqual(is_a_shape(grouped_ids[2], expected_shapes), {'valid': {'circle': [28, 13]}})
        
       
if __name__ == '__main__':
    unittest.main()
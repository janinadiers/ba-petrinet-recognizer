import unittest
from grouper import distance, get_bounding_box, get_start_and_end_time

class TestHelperMethods(unittest.TestCase):

    def test_distance(self):
        pointA = [0, 0]
        pointB = [3, 4]
        pointC = [6, 8]
        pointD = [7, 22]
        self.assertEqual(distance(pointA, pointB), 5)
        self.assertEqual(distance(pointC, pointD), 14.035668847618199)
    
    def test_get_bounding_box(self):
        stroke = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}
        self.assertEqual(get_bounding_box(stroke), (3, 4))
    
    def test_get_start_and_end_time(self):
        stroke = {'1': [{'x': 0, 'y': 0, 't': 0}, {'x': 3, 'y': 4, 't': 1}, {'x': 6, 'y': 8, 't': 2}]}
        self.assertEqual(get_start_and_end_time(stroke), {'start point': 0, 'end point': 2})
   

if __name__ == '__main__':
    unittest.main()
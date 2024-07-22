import unittest
from helper.normalizer import convert_coordinates

class TestCornerDetectionMethods(unittest.TestCase):

    def test_convert_coordinates(self):
        stroke = [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}, {'x': 3, 'y': 3}]
        converted_stroke = convert_coordinates([stroke], 10, 10)
        print(converted_stroke)
        
            
       
     
       
        
        
       
if __name__ == '__main__':
    unittest.main()
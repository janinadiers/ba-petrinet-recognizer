import unittest
from helper.normalizer import translate_to_origin
class TestNormalizerMethods(unittest.TestCase):

    def test_translate_to_origin(self):
        strokes_rect = [[{'x': 3, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}],[{'x': 1, 'y': 4}, {'x': 2, 'y': 4}, {'x': 3, 'y': 4}, {'x': 3, 'y': 3}, {'x': 3, 'y': 2}, {'x': 3, 'y': 1}]]
        print(translate_to_origin([point for stroke in strokes_rect for point in stroke]))
        # self.assertEqual(translate_to_origin([{'x': 1, 'y': 1}, {'x': 2, 'y': 2}]), [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}], )
     
       
        
        
       
if __name__ == '__main__':
    unittest.main()
import unittest
from helper.utils import order_strokes
from helper.export_strokes_to_inkml import export_strokes_to_inkml

class TestOrderStrokesMethods(unittest.TestCase):

    def test_order_strokes(self):
        strokes_rect4 = [[{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}], [{'x': 3, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}],[{'x': 3, 'y': 4}, {'x': 3, 'y': 3}, {'x': 3, 'y': 2}, {'x': 3, 'y': 1}], [{'x': 1, 'y': 4}, {'x': 2, 'y': 4}, {'x': 3, 'y': 4}]]
        ordered_strokes = order_strokes(strokes_rect4)
        export_strokes_to_inkml(ordered_strokes, 'test_order_strokes.inkml')
        # self.assertEqual(ordered_strokes,[[{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}],[{'x': 1, 'y': 4}, {'x': 2, 'y': 4}, {'x': 3, 'y': 4}],[{'x': 3, 'y': 4}, {'x': 3, 'y': 3}, {'x': 3, 'y': 2}, {'x': 3, 'y': 1}], [{'x': 3, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}]]
# )
            
       
if __name__ == '__main__':
    unittest.main()
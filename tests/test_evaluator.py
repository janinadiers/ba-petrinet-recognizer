import unittest
from evaluator import check_soundness, does_trace_grouping_exist_in_expected_shapes

class TestEvaluatorMethods(unittest.TestCase):

    def test_check_soundness(self):
        example1 = [{'circle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        example2 = [{'circle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        example3 = [{'circle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}, {'circle': ['0', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        example4 = [{'circle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        example5 = [{'circle': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}, {'circle': ['0', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        example6 = [{'circle': []}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        self.assertEqual(check_soundness(example1),True)
        self.assertEqual(check_soundness(example2),True)
        with self.assertRaises(ValueError):
            check_soundness(example3)
        self.assertEqual(check_soundness(example4),True)
        with self.assertRaises(ValueError):
            check_soundness(example5)
        with self.assertRaises(ValueError):
            check_soundness(example6)
    
    def test_does_trace_grouping_exist_in_expected_shapes(self):
        grouped_traces1 = {'circle': ['0']}
        expected_shapes1 = [{'circle': ['0']}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        self.assertEqual(does_trace_grouping_exist_in_expected_shapes(next(iter(grouped_traces1.values())), expected_shapes1),True)
        grouped_traces2 = {'rectangle': ['2']}
        expected_shapes2 = [{'circle': ['0']}, {'circle': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']}, {'rectangle': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']}]
        self.assertEqual(does_trace_grouping_exist_in_expected_shapes(next(iter(grouped_traces2.values())), expected_shapes2),False)
            
    

if __name__ == '__main__':
    unittest.main()
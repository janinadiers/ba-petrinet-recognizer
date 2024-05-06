import math
import numpy as np

class DistanceBetweenAllPoints:
    
    
    def get_min_distance(self, stroke1, stroke2):
        """Calculate the minimum Euclidean distance between all point pairs of two strokes."""
        min_distance = float('inf')
        for point1 in next(iter(stroke1.values())):
            for point2 in next(iter(stroke2.values())):
                distance = self.euclidean_distance(point1, point2)
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    def euclidean_distance(self, point1, point2):
        """Calculate the Euclidean distance between two points."""
        point1X = int(point1['x'])
        point1Y = int(point1['y'])
        point2X = int(point2['x'])
        point2Y = int(point2['y'])
        return math.sqrt((point1X - point2X)**2 + (point1Y - point2Y)**2)
    
    
    def initialize_adjacency_matrix(self, strokes):
        """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
        num_strokes = len(strokes)
        matrix = np.zeros((num_strokes, num_strokes), dtype=int)
        max_dist=300
        # Iterate over all pairs of strokes and determine if they are neighbors
        for i in range(num_strokes):
            for j in range(i + 1, num_strokes):
                distance = self.get_min_distance(strokes[i], strokes[j])
                # If distance is less than or equal to threshold, mark them as neighbors
                if distance <= max_dist:
                    matrix[i, j] = 1
          
        return matrix
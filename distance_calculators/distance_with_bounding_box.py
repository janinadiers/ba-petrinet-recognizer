import math
import numpy as np

class DistanceWithBoundingBox:

    def get_bounding_box_center(self, stroke):
        
        points = next(iter(stroke.values()))
        min_x = min(int(point['x']) for point in points)
        max_x = max(int(point['x']) for point in points)
        min_y = min(int(point['y']) for point in points)
        max_y = max(int(point['y']) for point in points)
        center_point = (min_x + max_x) / 2, (min_y + max_y) / 2
        return center_point

    def distance(self, point1, point2):
        # This should compute some form of distance between strokes, simple Euclidean distance between their centroids for example
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


    def get_distance(self, stroke1, stroke2):
        """Calculate the distance between two strokes based on their bounding box centers."""
        center1 = self.get_bounding_box_center(stroke1)
        center2 = self.get_bounding_box_center(stroke2)
        return self.distance(center1, center2)
        
    def initialize_adjacency_matrix(self,strokes):
        """Initialize the adjacency matrix A based on the spatial proximity of strokes."""
        num_strokes = len(strokes)
        matrix = np.zeros((num_strokes, num_strokes), dtype=int)
        max_dist=1200
        # Iterate over all pairs of strokes and determine if they are neighbors
        for i in range(num_strokes):
            for j in range(i + 1, num_strokes):
                distance = self.get_distance(strokes[i], strokes[j])
                # If distance is less than or equal to threshold, mark them as neighbors
                if distance <= max_dist:
                    matrix[i, j] = 1
          
        return matrix
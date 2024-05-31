# Der Classifier ist bei mir die Zuordnung der shape_candidates zu einer bestimmten Form aufgrund von Distanzmessung
# Der Rejector ist bei mir der nicht erreichte Threshold, der nach der Distanzmessung nicht erreicht wurde


import numpy as np

        
def is_a_shape(grouped_ids:list[int], expected_shapes:list[dict]) -> dict:
   
    calculate_orientation_features()



def calculate_orientation_features(stroke, size=(24, 24)):
    feature_images = np.zeros((5, size[0], size[1]))  # 4 orientation + 1 endpoint feature image
    reference_angles = np.array([0, 45, 90, 135]) * np.pi / 180  # Convert to radians
    
    for (x1, y1), (x2, y2) in zip(stroke[:-1], stroke[1:]):
        dx, dy = x2 - x1, y2 - y1
        angle = np.arctan2(dy, dx) % (2 * np.pi)  # Ensure angle is positive
        
        # Calculate differences from each reference angle
        angle_diffs = np.abs(angle - reference_angles)
        angle_diffs = np.minimum(angle_diffs, 2 * np.pi - angle_diffs)  # Wrap around 360 degrees
        
        # Feature strength based on angle difference
        strength = 1 - np.clip(angle_diffs / (np.pi / 4), 0, 1)
        
        # Map coordinates to feature image grid
        grid_x, grid_y = int(size[0] * (x1 / max_x)), int(size[1] * (y1 / max_y))
        
        # Assign feature values to grid, using maximum value if overlapping occurs
        for i in range(4):
            feature_images[i, grid_x, grid_y] = max(feature_images[i, grid_x, grid_y], strength[i])
        
        # Set endpoint features
        if (x1, y1) == stroke[0] or (x2, y2) == stroke[-1]:
            feature_images[4, grid_x, grid_y] = 1

    return feature_images

# Example usage for one stroke
max_x, max_y = 1000, 1000  # Maximum dimensions for normalization
feature_images = calculate_orientation_features(strokes[0], size=(24, 24))

    

    



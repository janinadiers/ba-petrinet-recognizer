import math
import copy
from helper.export_strokes_to_inkml import export_strokes_to_inkml
import numpy as np
from scipy.interpolate import interp1d

  
# Die Skalierung ist notwendig, um die Punkte auf eine einheitliche Größe zu bringen, sodass die Punkte in einem einheitlichen Koordinatensystem liegen
def scale(strokes: list[dict]) -> list[dict]:
    _points = [point for stroke in strokes for point in stroke]

    # _points = copy.deepcopy(points[0])
    xmin = min(point['x'] for point in _points)
    xmax = max(point['x'] for point in _points)
    ymin = min(point['y'] for point in _points)
    ymax = max(point['y'] for point in _points)

    scale = max(xmax - xmin, ymax - ymin)
    if(scale == 0):
        return
    for point in _points:
        
        # Those lines ensure, that the points are in the range of 0 and 1
        point['x'] = (point['x'] - xmin) / scale
        point['y'] = (point['y'] - ymin) / scale
    
    return [_points]
       

def map_values_in_range(value, old_min, old_max, new_min, new_max): 
    print('value', value)
    print('old_min', old_min)
    print('old_max', old_max)
    print('new_min', new_min)
    print('new_max', new_max)
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def normalize_strokes(strokes, canvas_width, canvas_height):
    
    dataset_canvas_width = 59414
    dataset_canvas_height = 49756
    
    # calculate the bounding box for all points
    # min_x = min([point['x'] for stroke in strokes for point in stroke])
    # min_y = min([point['y'] for stroke in strokes for point in stroke])
    min_x = 0
    min_y = 0
    # max_x = max([point['x'] for stroke in strokes for point in stroke])
    # max_y = max([point['y'] for stroke in strokes for point in stroke])
    
    # # Scaling for the entire drawing
    # width = max_x - min_x;
    # height = max_y - min_y;
    scaleX = dataset_canvas_width / canvas_width;
    scaleY = dataset_canvas_height / canvas_height;
    scale = min(scaleX, scaleY);
    
    # mittig setzen
    offsetX = (dataset_canvas_width - canvas_width * scale) / 2;
    offsetY = (dataset_canvas_height - canvas_height * scale) / 2;
    
    # Normalize the coordinates
    normalized_strokes = []
    for stroke in strokes:
        normalized_stroke = []
        for point in stroke:
            normalized_stroke.append({'x': (point['x']- min_x) * scale + offsetX, 'y': (point['y'] - min_y) * scale + offsetY})
        normalized_strokes.append(normalized_stroke)
    return normalized_strokes
 
         
def resample_strokes(strokes: list[dict]) -> list[dict]:
    _strokes = copy.deepcopy(strokes)
    resampled_strokes = []

    for stroke in _strokes:
        resampled_strokes.append(resample(stroke))
    
    return resampled_strokes          
 
# def resample(points:list[dict]) -> list[dict]:
    
#     if len(points) < 2:
#         return points
    
#     pixel_distance = 200
#     # pixel_distance = 100
#     # Wenn die path_length(points) / 32 < 2 ist, dann wollen wir aber trotzdem zwei Punkte setzen, das kann passieren, wenn der Pfad sehr kurz ist, sodass wir den Abstand von 32 Pixeln nicht einhalten können 
#     if((path_length(points) / pixel_distance) < 2):
#         pixel_distance = path_length(points) / 1.5
#     # else:
#     #     amount_new_points = path_length(points) / pixel_distance # Anzahl der neuen Punkte, die hinzugefügt werden sollen: Die Anzahl setzt sich aus der Länge des Pfades zusammen, wo wir jeweils nach 32 Pixeln einen neuen Punkt setzen wollen
    
#     I = pixel_distance # beschreibt die Länge der Abstände zwischen den Punkten, die -1 ist deshalb nötig, weil der letzte Punkt keien Verbindung zu einem weiteren Punkt hat
#     # I ist null, wenn es nur Punkte mit den gleichen Koordinaten gibt
#     # if(I == 0):
#     #     return points
#     # I = 100
#     D = 0 # Beschreibt die bisher zurückgelegte Pfadlänge
#     new_points = [points[0]] 
#     i = 1
#     print('pixel distance: ', pixel_distance, (path_length(points) / pixel_distance))
#     while i < len(points):
#         d = round(distance(points[i-1], points[i]))
#         if D + d >= I:
#             t = (I - D) / d
#             qx = points[i-1]['x'] + t * (points[i]['x'] - points[i-1]['x'])
#             qy = points[i-1]['y'] + t * (points[i]['y'] - points[i-1]['y'])
#             q = {'x': qx, 'y': qy}

#             new_points.append(q)
#             points.insert(i, q)

#             D = 0
#         else:
#             D += d
#         i += 1 

#     # append the last point in the right distance
#     # new_points.append(points[-1])
#     for i in range(len(new_points) -1):
#         print('hier', distance(new_points[i], new_points[i+1]))
     
#     return new_points

def resample(points, pixel_distance=32):
    if len(points) < 2:
        return points
    # total_length = path_length(points)
    # if total_length / pixel_distance < 2:
    #     pixel_distance = total_length / 1.5

    I = pixel_distance
    D = 0
    new_points = [points[0]]
    i = 1

    while i < len(points):
        d = distance(points[i-1], points[i])
        if D + d >= I:
            t = (I - D) / d
            qx = points[i-1]['x'] + t * (points[i]['x'] - points[i-1]['x'])
            qy = points[i-1]['y'] + t * (points[i]['y'] - points[i-1]['y'])
            q = {'x': qx, 'y': qy}

            new_points.append(q)
            points.insert(i, q)

            D = 0
        else:
            D += d
        i += 1

    # Append the last point in the right distance
    # if new_points[-1] != points[-1]:
    #     new_points.append(points[-1])
    

    return new_points

# Function to calculate cumulative distance along points
def cumulative_distance(points):
    distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    return np.insert(np.cumsum(distances), 0, 0)

# Generate new evenly spaced points based on cumulative distance
def resample_evenly(points, num_points):
    cum_dist = cumulative_distance(points)
    interp_func = interp1d(cum_dist, points, kind='linear', axis=0)
    new_distances = np.linspace(0, cum_dist[-1], num_points)
    return interp_func(new_distances)

# def resample(points):
#     points_array = np.array([[point['x'], point['y']] for point in points])
#     # Desired number of points after resampling
#     num_resampled_points = 50

#     # Resample the points to have a specified number of evenly spaced points
#     evenly_resampled_points = resample_evenly(points_array, num_resampled_points)
#     resampled_points = []
#     # Convert the resampled NumPy array back to list of dictionaries
#     for point in evenly_resampled_points:
#         print('point: ', point)
#         if point[0] != None and point[1] != None:
#             resampled_points.append({'x': point[0], 'y': point[1]})
#     print('resampled points: ', resampled_points)   
#     return resampled_points 
    # resampled_points = [{'x': int(point[0]), 'y': int(point[1])} for point in evenly_resampled_points]


# translate the points from all strokes to have the centroid at the origin
def translate_to_origin(points:list[dict]) -> list[dict]:
    # _points = [point for stroke in strokes for point in stroke]
    _points = copy.deepcopy(points[0])
    centroid = [0,0]
    # Translate points to have the centroid at the origin
    for point in _points:
        # print('point: ', point)
        centroid = [centroid[0] + point['x'], centroid[1] + point['y']]
      
    centroid = [centroid[0] / len(_points), centroid[1] / len(_points)]
    for point in _points:
        point['x'] -= centroid[0]
        point['y'] -= centroid[1]
    return [_points]
 

def path_length(points):
    return sum(distance(points[i], points[i+1]) for i in range(len(points) - 1))

def distance(p1:dict, p2:dict) -> float:
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)


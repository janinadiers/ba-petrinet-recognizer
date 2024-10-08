import copy
from helper.utils import distance, path_length


# Die Skalierung ist notwendig, um die Punkte auf eine einheitliche Größe zu bringen, sodass die Punkte in einem einheitlichen Koordinatensystem liegen
def scale(strokes: list[dict]) -> list[dict]:
    _points = [point for stroke in strokes for point in stroke]
    xmin = min(point['x'] for point in _points)
    xmax = max(point['x'] for point in _points)
    ymin = min(point['y'] for point in _points)
    ymax = max(point['y'] for point in _points)
    scale = max(xmax - xmin, ymax - ymin)
    if(scale == 0):
        return [_points]
    for point in _points:
        # Those lines ensure, that the points are in the range of 0 and 1
        point['x'] = (point['x'] - xmin) / scale
        point['y'] = (point['y'] - ymin) / scale
    
    return [_points]
       

def convert_coordinates(strokes, canvas_width, canvas_height):
    
    # Das ist die Canvas Größe des FC dataset
    dataset_canvas_width = 59414
    dataset_canvas_height = 49756
    
    # calculate the bounding box for all points
    min_x = min([point['x'] for stroke in strokes for point in stroke])
    min_y = min([point['y'] for stroke in strokes for point in stroke])
    # max_x = max([point['x'] for stroke in strokes for point in stroke])
    # max_y = max([point['y'] for stroke in strokes for point in stroke])
    
    # # Scaling for the entire drawing
    # canvas_width = max_x - min_x;
    # canvas_height = max_y - min_y;
    scaleX = dataset_canvas_width / canvas_width ;  
    scaleY =  dataset_canvas_height/ canvas_height;
    scale = min(scaleX, scaleY);
    
    # mittig setzen
    # offsetX = (dataset_canvas_width - canvas_width * scale) / 2;
    # offsetY = (dataset_canvas_height - canvas_height * scale) / 2;
    
    # Normalize the coordinates
    converted_strokes = []
    for stroke in strokes:
        normalized_stroke = []
        for point in stroke:
            normalized_stroke.append({'x': (point['x']- min_x) * scale, 'y': (point['y'] - min_y) * scale })
        converted_strokes.append(normalized_stroke)
    return converted_strokes
 
         
def resample_strokes(strokes: list[dict]) -> list[dict]:
    _strokes = copy.deepcopy(strokes)
    resampled_strokes = []

    for stroke in _strokes:
        resampled_strokes.append(resample(stroke))
    
    return resampled_strokes          
 

def resample(points, n=80):
    if len(points) < 2:
        return points
   
    total_length = path_length(points)
    
    I = total_length / (n - 1)
  
    if I == 0:
        return points
   
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

    return new_points


# translate the points from all strokes to have the centroid at the origin
def translate_to_origin(points:list[dict], n= 80,) -> list[dict]:
    _points = copy.deepcopy(points[0])
    
    centroid = [0,0]
    # Translate points to have the centroid at the origin
    for point in _points:
        centroid = [centroid[0] + point['x'], centroid[1] + point['y']]
      
    centroid = [centroid[0] / n, centroid[1] / n]
    
    for point in _points:
        point['x'] -= centroid[0]
        point['y'] -= centroid[1]
    
    
    return [_points]
 




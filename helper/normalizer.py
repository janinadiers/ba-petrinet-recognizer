import math
import copy
from helper.export_strokes_to_inkml import export_strokes_to_inkml

def normalize(strokes: list[dict]) -> list[dict]:
    _strokes = copy.deepcopy(strokes)
    resampled_strokes = []
    for stroke in _strokes:
        resampled_strokes.append(resample(stroke))
    
    # combined_strokes = [point for stroke in resampled_strokes for point in stroke]
    # translated_points = translate_to_origin(combined_strokes)

    # start_index = 0
    # for stroke in resampled_strokes:
    #     amount_points = len(stroke)
    #     translated_strokes.append(translated_points[start_index:start_index+ amount_points])
    #     start_index += amount_points
      
   
    # export_strokes_to_inkml(translated_strokes, 'translated_points.inkml')
    # exit()
    # return normalized_strokes
    return resampled_strokes
    

# def pixels_to_himetrics(pixels, dpi):
#     himetrics_per_inch = 2540
#     return pixels * (himetrics_per_inch / dpi)
    
# Die Skalierung ist notwendig, um die Punkte auf eine einheitliche Größe zu bringen, sodass die Punkte in einem einheitlichen Koordinatensystem liegen
def scale(points: list[dict]) -> list[dict]:
    
    xmin = min(point['x'] for point in points)
    xmax = max(point['x'] for point in points)
    ymin = min(point['y'] for point in points)
    ymax = max(point['y'] for point in points)

    scale = max(xmax - xmin, ymax - ymin)
    if(scale == 0):
        return
    for point in points:
        
        # Those lines ensure, that the points are in the range of 0 and 1
        point['x'] = (point['x'] - xmin) / scale
        point['y'] = (point['y'] - ymin) / scale
       
    
def normalize_strokes(strokes):
    
    dataset_canvas_width = 59414
    dataset_canvas_height = 49756
    
    # calculate the bounding box for all points
    min_x = min([point['x'] for stroke in strokes for point in stroke])
    min_y = min([point['y'] for stroke in strokes for point in stroke])
    max_x = max([point['x'] for stroke in strokes for point in stroke])
    max_y = max([point['y'] for stroke in strokes for point in stroke])
    
    # Scaling for the entire drawing
    width = max_x - min_x;
    height = max_y - min_y;
    scaleX = dataset_canvas_width / width;
    scaleY = dataset_canvas_height / height;
    scale = min(scaleX, scaleY);
    
    # mittig setzen
    offsetX = (dataset_canvas_width - width * scale) / 2;
    offsetY = (dataset_canvas_height - height * scale) / 2;
    
 
    # Normalize the coordinates
    normalized_strokes = []
    for stroke in strokes:
        normalized_stroke = []
        for point in stroke:
            normalized_stroke.append({'x': int((point['x']- min_x) * scale + offsetX), 'y': int((point['y'] - min_y) * scale + offsetY)})
        normalized_strokes.append(normalized_stroke)
    return normalized_strokes
 
         
def resample_strokes(strokes: list[dict]) -> list[dict]:
    _strokes = copy.deepcopy(strokes)
    resampled_strokes = []
    for stroke in _strokes:
        resampled_strokes.append(resample(stroke))
    
    return resampled_strokes          
 
def resample(points:list[dict]) -> list[dict]:
    pixel_distance = 32
    # pixel_distance = 100
    # Wenn die path_length(points) / 32 < 2 ist, dann wollen wir aber trotzdem zwei Punkte setzen, das kann passieren, wenn der Pfad sehr kurz ist, sodass wir den Abstand von 32 Pixeln nicht einhalten können 
    if((path_length(points) / pixel_distance) < 2):
        amount_new_points = 2
    else:
        amount_new_points = path_length(points) / pixel_distance # Anzahl der neuen Punkte, die hinzugefügt werden sollen: Die Anzahl setzt sich aus der Länge des Pfades zusammen, wo wir jeweils nach 32 Pixeln einen neuen Punkt setzen wollen
    
    print('amount_new_points', amount_new_points)
    I = path_length(points) / (amount_new_points - 1) # beschreibt die Länge der Abstände zwischen den Punkten, die -1 ist deshalb nötig, weil der letzte Punkt keien Verbindung zu einem weiteren Punkt hat
    # I ist null, wenn es nur Punkte mit den gleichen Koordinaten gibt
    if(I == 0):
        return points
    D = 0 # Beschreibt die bisher zurückgelegte Pfadlänge
    new_points = [points[0]] 
    i = 1

    while i < len(points):
       
        d = distance(points[i-1], points[i])
        if D + d >= I:
            t = (I - D) / d
            qx = points[i-1]['x'] + t * (points[i]['x'] - points[i-1]['x'])
            qy = points[i-1]['y'] + t * (points[i]['y'] - points[i-1]['y'])
            q = {'x': round(qx), 'y': round(qy)}

            new_points.append(q)
            points.insert(i, q)

            D = 0
        else:
            D += d
        i += 1 

    # append the last point in the right distance
    new_points.append(points[-1])
    
     
    return new_points

# translate the points from all strokes to have the centroid at the origin
def translate_to_origin(points:list[dict]) -> list[dict]:
    _points = copy.deepcopy(points)
    centroid = [0,0]
    # Translate points to have the centroid at the origin
    for point in _points:
        centroid = [centroid[0] + point['x'], centroid[1] + point['y']]
      
    centroid = [centroid[0] / len(_points), centroid[1] / len(_points)]
    for point in _points:
        point['x'] -= centroid[0]
        point['y'] -= centroid[1]
    return _points


    
def path_length(points:list[dict]) -> float:
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d    

def distance(p1:dict, p2:dict) -> float:
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)


def remove_junk_strokes(strokes:list[dict]) -> list[dict]:
    _strokes = copy.deepcopy(strokes)
    # Remove strokes with less than 4 points
    _strokes = [stroke for stroke in _strokes if len(stroke) > 3]
    return _strokes
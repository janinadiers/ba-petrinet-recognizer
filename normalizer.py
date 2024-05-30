import math

def normalize(points: list[dict]) -> list[dict]:
    points = resample(points)
    # print('translate')
    # translate_to_origin(points)
    # print('scale')
    # scale(points)
    
    return points
    

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
       
    
   
 
def resample(points:list[dict]) -> list[dict]:
    pixel_distance = 32
    # pixel_distance = 100
    # Wenn die path_length(points) / 32 < 2 ist, dann wollen wir aber trotzdem zwei Punkte setzen, das kann passieren, wenn der Pfad sehr kurz ist, sodass wir den Abstand von 32 Pixeln nicht einhalten können 
    if((path_length(points) / pixel_distance) < 2):
        amount_new_points = 2
    else:
        amount_new_points = path_length(points) / pixel_distance # Anzahl der neuen Punkte, die hinzugefügt werden sollen: Die Anzahl setzt sich aus der Länge des Pfades zusammen, wo wir jeweils nach 32 Pixeln einen neuen Punkt setzen wollen
       
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

def translate_to_origin(points:list[dict]) -> list[dict]:
      # Calculate the centroid
    origin_x = sum(point['x'] for point in points) / len(points)
    origin_y = sum(point['y'] for point in points) / len(points)
    # Translate points to have the centroid at the origin
    for point in points:
        point['x'] -= origin_x
        point['y'] -= origin_y


    
def path_length(points:list[dict]) -> float:
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d    

def distance(p1:dict, p2:dict) -> float:
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
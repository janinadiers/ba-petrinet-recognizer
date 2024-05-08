import math

def normalize(points: list[dict], n:int) -> list[dict]:
    points = resample(points, n)
    return points
    # eventuell noch scale und translate???

 
def resample(points:list[dict]):
    # Wenn path_length(points) / 32 < 2 ist, dann wollen wir aber trotzdem zwei Punkte setzen, das kann passieren, wenn der Pfad sehr kurz ist, sodass wir den Abstand von 32 Pixeln nicht einhalten können 
    amount_new_points = 0
    if(path_length(points) / 32 < 2):
        amount_new_points = 2
    else:
        amount_new_points = path_length(points) / 32 # Anzahl der neuen Punkte, die hinzugefügt werden sollen: Die Anzahl setzt sich aus der Länge des Pfades zusammen, wo wir jeweils nach 32 Pixeln einen neuen Punkt setzen wollen
    
    I = path_length(points) / (amount_new_points - 1) # beschreibt die Länge der Abstände zwischen den Punkten, die -1 ist deshalb nötig, weil der letzte Punkt keien Verbindung zu einem weiteren Punkt hat
    D = 0 # Beschreibt die Länge der neu hinzugefügten Punkte zu new_points
    new_points = [points[0]] 
    i = 1
    while len(new_points) < len(points): 
    # for i in range(1, len(points)):
        d = distance(points[i-1], points[i])
        if D + d >= I:
            qx = points[i-1]['x'] + ((I - D) / d) * (points[i]['x'] - points[i-1]['x'])
            qy = points[i-1]['y'] + ((I - D) / d) * (points[i]['y'] - points[i-1]['y'])
            q = {'x': round(qx), 'y': round(qy)}
            new_points.append(q)
            points.insert(i, q)
            D = 0
        else:
            D += d
            if i  < len(points) -1:
                i += 1
            
    return new_points
    
def path_length(points:list[dict]) -> float:
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d    

def distance(p1:dict, p2:dict) -> float:
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
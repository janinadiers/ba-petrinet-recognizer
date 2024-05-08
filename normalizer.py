import math

def normalize(points: list[dict], n:int) -> list[dict]:
    points = resample(points, n)
    # eventuell noch scale und translate???

 
def resample(points:list[dict], n:int):
    I = path_length(points) / (n - 1) # beschreibt die Soll-Länge des Paths, also die Länge der Strecke, die die Punkte verbinden, wobei sich die Distanz zwischen den Punkten aus der euklidischen Distanz ergibt
    #Durch die Aufteilung der Gesamtlänge des Pfads durch n-1 wird vermieden, dass der erste und letzte Punkt des Pfads doppelt gezählt werden, da sie nur eine Verbindung zu einem benachbarten Punkt haben.
    D = 0 # Beschreibt die Länge der neu hinzugefügten Punkte zu new_points
    new_points = [points[0]]  
    for i in range(1, len(points)):
        d = distance(points[i-1], points[i])
        if D + d >= I:
            qx = points[i-1]['x'] + ((I - D) / d) * (points[i]['x'] - points[i-1]['x'])
            qy = points[i-1]['y'] + ((I - D) / d) * (points[i]['y'] - points[i-1]['y'])
            q = {'x': qx, 'y': qy}
            new_points.append(q)
            points.insert(i, q)
            D = 0
        else:
            D += d
    print('path length before normalization: ', path_length(points))
    print('path length after normalization: ', path_length(new_points))
    return new_points
    
def path_length(points:list[dict]) -> float:
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d    

def distance(p1:dict, p2:dict) -> float:
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
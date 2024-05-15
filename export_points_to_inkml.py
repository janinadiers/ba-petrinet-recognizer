def export_points_to_inkml(strokes:list[dict], filename:str):
    """ Export the normalized points to an inkml file"""
    with open(filename, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<ink>\n')
        file.write('  <traceFormat>\n')
        file.write( '    <channel name="X" type="integer" />\n')
        file.write('    <channel name="Y" type="integer" />\n')
        file.write('  </traceFormat>\n')
        for stroke in strokes:
            stroke_points = next(iter(stroke.values()))
            stroke_id = int(next(iter(stroke)))
            file.write('<trace id="' + str(stroke_id) + '">\n')
            for point in stroke_points:
                file.write(str(point['x']) + ' ' + str(point['y']) + ',')
            file.write('</trace>\n')
        file.write('</ink>\n')

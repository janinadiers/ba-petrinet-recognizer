def export_strokes_to_inkml(strokes:list[dict], filename:str):
    """ Export the normalized points to an inkml file"""
    with open(filename, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<ink>\n')
        file.write('  <traceFormat>\n')
        file.write( '    <channel name="X" type="integer" />\n')
        file.write('    <channel name="Y" type="integer" />\n')
        file.write('  </traceFormat>\n')
        for idx, stroke in enumerate(strokes):
            file.write('<trace id="' + str(idx) + '">\n')
            # print('stroke: ', stroke)
            for point in stroke:
                file.write(str(point['x']) + ' ' + str(point['y']) + ',')
            file.write('</trace>\n')
        file.write('</ink>\n')

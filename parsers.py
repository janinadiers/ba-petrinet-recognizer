import xml.etree.ElementTree as ET


def parse_traces_from_inkml_file(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()

    # Namespace handling
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}

    # Extract traces
    traces = []
    for trace in root.findall('trace', namespaces):
        # Extract trace data
        trace_data:list = trace.text.strip().split(',')
        trace_id:str = trace.attrib['id']
        trace_points = []
        # Parse each coordinate in the trace
        for point in trace_data:
            point = list(point.split(' '))
            point = list(filter(None, point))
            trace_points.append({'x': point[0], 'y': point[1], 't': point[2]}) 
        traces.append({trace_id: trace_points})

    return traces


def parse_ground_truth(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    # Namespace handling
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    # Extract shapes
    shapes = []
    
    for symbol in root.findall('symbols', namespaces):
        traceGroups = symbol.findall('traceGroup', namespaces)
        for traceGroup in traceGroups:
            annotations = traceGroup.findall("annotation[@type='truth']", namespaces)
            traceViews = traceGroup.findall('traceView', namespaces)
            
            if annotations[0].text == 'state' or annotations[0].text == 'connection':
                new_entry = {'circle' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
                
            elif annotations[0].text == 'process':
                new_entry = {'rectangle' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'arrow':
                new_entry = {'line' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'label' or annotations[0].text == 'text':
                new_entry = {'text' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'final state':
                new_entry = {'circle in circle' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'data':
                new_entry = {'parallelogram' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'decision':
                new_entry = {'diamond' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            elif annotations[0].text == 'terminator':
                new_entry = {'ellipse' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
            else:
                print('Unknown shape type: ', annotations[0].text, 'please add it to the parser')
    return shapes



def parse_shape_types_with_amount_of_occurence(file_path:str):
     # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    
     # Namespace handling
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    
    amount_circle = 0
    amount_rectangle = 0
    amount_line = 0
    amount_text = 0
    amount_circle_in_circle = 0
    amount_parallelogram = 0
    amount_diamond = 0
    amount_ellipse = 0
    amount_terminator = 0
 
    for symbol in root.findall('symbols', namespaces):
        traceGroups = symbol.findall('traceGroup', namespaces)
        for traceGroup in traceGroups:
            annotations = traceGroup.findall("annotation[@type='truth']", namespaces)
            if annotations[0].text == 'state' or annotations[0].text == 'connection':
                amount_circle += 1 
            elif annotations[0].text == 'process':
                amount_rectangle += 1
            elif annotations[0].text == 'arrow':
                amount_line += 1
            elif annotations[0].text == 'label' or annotations[0].text == 'text':
                amount_text += 1
            elif annotations[0].text == 'final state':
                amount_circle_in_circle += 1
            elif annotations[0].text == 'data':
                amount_parallelogram += 1
            elif annotations[0].text == 'decision':
                amount_diamond += 1
            elif annotations[0].text == 'terminator':
                amount_ellipse += 1
            else:
                print('Unknown shape type: ', annotations[0].text, 'please add it to the parser')
    return {'circle': amount_circle, 'rectangle': amount_rectangle, 'line': amount_line, 'text': amount_text, 'circle in circle': amount_circle_in_circle, 'parallelogram': amount_parallelogram, 'diamond': amount_diamond, 'ellipse': amount_ellipse, 'terminator': amount_terminator}



    
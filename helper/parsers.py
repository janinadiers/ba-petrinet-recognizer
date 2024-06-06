import xml.etree.ElementTree as ET

def parse_strokes_from_inkml_file(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    traces = []
    # adjust_trace_ids(root)
    for trace in root.findall('trace', namespaces):
        # Extract trace data
        trace_data:list = trace.text.strip().split(',')
        # trace_id:str = int(trace.attrib['id'])
        trace_points = []
        # Parse each coordinate in the trace
        for point in trace_data:
            point = list(point.split(' '))
            point = list(filter(None, point))
            trace_points.append({'x': int(point[0]), 'y': int(point[1]), 't': int(point[2])}) 
            
        traces.append(trace_points)
    
    return traces


def parse_ground_truth(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    shapes = []
    # adjust_trace_ids(root)
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
            elif annotations[0].text == 'final state':
                new_entry = {'double circle' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
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
            elif annotations[0].text == 'arrow':
                new_entry = {'line' :[int(traceView.attrib['traceDataRef']) for traceView in traceViews] }
                shapes.append(new_entry)
                
    return shapes


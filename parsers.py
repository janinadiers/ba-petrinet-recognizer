import xml.etree.ElementTree as ET
import os

def parse_strokes_from_inkml_file(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    traces = []
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
    adjust_trace_ids(root)
    return traces


def parse_ground_truth(file_path: str)-> list[dict]:
    # Parse the XML file
    tree:ET.ElementTree = ET.parse(file_path)
    root:ET.Element = tree.getroot()
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
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
    return shapes

def adjust_trace_ids(root) -> str:
    
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}
    
     # adjust trace ids and traceGroup ids to index
    for symbol in root.findall('symbols', namespaces):
        trace_groups = symbol.findall('traceGroup', namespaces)
        for i, trace_group in enumerate(trace_groups):
            trace_group.attrib['id'] = str(i)
            for trace_view in trace_group.findall('traceView', namespaces):
                for i, trace in enumerate(root.findall('trace', namespaces)):
                    if trace.attrib['id'] == trace_view.attrib['traceDataRef']:
                        
                        trace_view.attrib['traceDataRef'] = str(i)
                        for head in trace_group.findall('head', namespaces):
                            for trace_view2 in head.findall('traceView', namespaces):
                                if trace.attrib['id'] == trace_view2.attrib['traceDataRef']:
                                    trace_view2.attrib['traceDataRef'] = str(i)
                        for shaft in trace_group.findall('shaft', namespaces):
                            for trace_view3 in shaft.findall('traceView', namespaces):
                                if trace.attrib['id'] == trace_view3.attrib['traceDataRef']:
                                    trace_view3.attrib['traceDataRef'] = str(i)
                                    
                        trace.attrib['id'] = str(i)   
    
def exclude_text_strokes(file_path: str) -> str:
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'inkml': 'http://www.w3.org/2003/InkML'}

    # This will hold all trace IDs that need to be removed
    traces_to_remove = set()

    for symbol in root.findall('symbols', namespaces):
        trace_groups = symbol.findall('traceGroup', namespaces)
        for trace_group in trace_groups:
            # Check each traceGroup for an annotation indicating 'text' or 'label'
            annotations = trace_group.findall("annotation[@type='truth']", namespaces)
            if annotations[0].text == 'text' or annotations[0].text == 'label':
                # Collect all traceDataRef from traceViews if the annotation condition is met
                trace_views = trace_group.findall('traceView', namespaces)
                for trace_view in trace_views:
                    trace_data_ref = int(trace_view.attrib['traceDataRef'])
                    if trace_data_ref:
                        traces_to_remove.add(trace_data_ref)
                symbol.remove(trace_group)

    # Remove the collected traces from the root
    all_traces = root.findall('trace', namespaces)
    for trace in all_traces:
        if int(trace.attrib['id']) in traces_to_remove:
            root.remove(trace)
    
    adjust_trace_ids(root)
            
    # Save the modified XML to a new file
    directory = os.path.dirname(file_path)
    base_name = os.path.basename(file_path).split('.')[0]
    new_file_path = os.path.join(directory, f"{base_name}_no_text.inkml")
    tree.write(new_file_path)
    return new_file_path

                      
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



    
import xml.etree.ElementTree as ET



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
    # create subdirectory if it does not exist
    if not os.path.exists(os.path.join(directory, 'no_text')):
        os.makedirs(os.path.join(directory, 'no_text'))
    
    base_name = os.path.basename(file_path).split('.')[0]
    # save file in subdirectory
    new_file_path = os.path.join(directory, 'no_text', f"{base_name}.inkml")
    # new_file_path = os.path.join(directory, f"{base_name}_no_text.inkml")
    tree.write(new_file_path)
    return new_file_path


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
    

if __name__ == '__main__':
    import os
    import argparse
    import glob

    parser = argparse.ArgumentParser(description='Remove text strokes from inkml files.')
    parser.add_argument('--files', dest='files', type=glob.glob, nargs='?', action='store',
                        help='glob to inkml file(s)')
    args = parser.parse_args()
    files = args.files
    #print(files)
    if files:
        for file in files:
            print(file)
            exclude_text_strokes(file)
    else:
        print("Please provide a file path to an inkml file.")
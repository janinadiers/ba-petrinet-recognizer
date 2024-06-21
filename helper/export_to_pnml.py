from helper.utils import get_strokes_from_candidate

def export_to_pnml(result:dict, strokes, filename):
    pnml = '<pnml ...'
    for entry in result:
        if 'valid' in entry:
            for key, value in entry['valid'].items():
                first_value = value
                break
            for key, value in entry['valid'].items():
                if key == 'circle':
                    print('valid', first_value)
                    print(get_strokes_from_candidate(first_value, strokes))
                if key == 'rectangle':
                    pass
                if key == 'line':
                    pass
            

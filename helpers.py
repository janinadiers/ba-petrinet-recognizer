from collections import Counter

def count_common_elements(list1, list2):
    set1 = set(str(d) for d in list1)
    set2 = set(str(d) for d in list2)
    common_elements = set1.intersection(set2)
    return len(common_elements)

def count_correctly_recognized_shape_name(recognized_shapes, expected_shapes, shape_name):
    count = 0
    for shape in recognized_shapes:
        if list(shape.keys())[0] == shape_name and shape in expected_shapes:
            count += 1
    return count



def count_different_elements(list1, list2):
    set1 = set(str(d) for d in list1)
    set2 = set(str(d) for d in list2)
    different_elements = set1 - set2
    return len(different_elements)

def count_shape(list_with_dicts, shape_name):
    count = 0
    for shape in list_with_dicts:
        if shape_name in shape:
            count += 1
    return count


def trace_ids_are_unique(dicts):
    values = [list(d.values())[0] for d in dicts]
    flat_list = [item for sublist in values for item in sublist]
    count = Counter(flat_list)
    return not any(c > 1 for c in count.values())

def get_shape_names(expected_shapes):
    shape_names = []
    for shape in expected_shapes:
        if not next(iter(shape.keys())) in shape_names:
            shape_names.append(next(iter(shape.keys())))
    return shape_names
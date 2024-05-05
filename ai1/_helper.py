import ast

def load_dict_from_txt(path):
    result_dict = {}
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            result_dict[key] = ast.literal_eval(value)
    return result_dict


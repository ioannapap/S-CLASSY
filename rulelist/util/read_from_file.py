import os

def find_path_to_file(filename):
    """Finds the path to an existing file"""
    path = os.path.abspath(filename)
    return path

def read_file(filename):
    """Reads the file.
    Input: Raw .txt file (every line represents a pattern or a selector).
        Input format:   pattern_1\n
                        pattern_2\n
                        ...
                        pattern_x\n
                        *\n
                        selector_1\n
                        selector_2\n
                        ...
                        selector_j
    Output: List of expert candidates (can be selectors and/or patterns).
    """
    with open(find_path_to_file(filename), "r", encoding = "utf-8") as f:
        
        file_list = f.readlines()

    return file_list

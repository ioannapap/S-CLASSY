import os
from os.path import exists

def find_path_to_file(filename):
    path = os.path.abspath(filename)
    print(path)
    return path

def clear_content_before_append(filename):
    """ Clears the results from files.
    Input: .txt filename.
    Output: A file with new entries.
    Note: This script is used to clear the results from files, when the file already exists. If it doesn't, it simply skips the clearance.
    """
    path = find_path_to_file(filename)
    file_exists = exists(path)
    if file_exists:
        f = open(path, 'r+')
        f.truncate(0)  # need '0' when using r+


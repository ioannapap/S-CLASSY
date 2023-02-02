import os

def find_path_to_file(filename):

    path = os.path.abspath(filename)

    return path

def append_file(filename, new_text):
    """ Appends to file.
    Input: .txt filename.
    Output: A file with new entries. After each value a '+' is appended.
    Note: The use of these functions are for experimental evaluation.
    """

    f = open(find_path_to_file(filename), "a")
    f.write(new_text + " + ")
    f.close()


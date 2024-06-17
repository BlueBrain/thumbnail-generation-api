"""
Utils module for unit tests
"""


def load_content(json_path: str, encoded: bool = True):
    """
    Loads content from a file
    """
    with open(json_path) as file:
        if encoded:
            return file.read().encode("utf-8")
        return file.read()

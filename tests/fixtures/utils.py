"""
Utils module for unit tests
"""


def load_content(file_path: str, encoded: bool = True):
    """
    Loads content from a file
    """
    with open(file_path) as file:
        if encoded:
            return file.read().encode("utf-8")
        return file.read()


def load_nwb_content(file_path: str):
    """
    Loads content for an NWB file
    """
    with open(file_path, "rb") as file:
        file_content = file.read()

    return file_content

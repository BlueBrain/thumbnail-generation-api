"""
trace_img utils module exposes useful utilities related to the generation of traces
"""

import re
import h5py
import numpy as np
from typing import List
from typing import Union, List
from api.exceptions import (
    NoConversionFound,
    NoResponseFound,
    NoProtocolFound,
    NoRateFound,
    NoUnitFound,
    NoCellFound,
    NoRepetitionFound,
    NoSweepFound,
)
from api.models.enums import MetaType


Num = Union[int, float]


def find_digits(string: str) -> Union[int, None]:
    """
    Get last consecutive digits from string

    Args:
        string: the string to be parsed

    Returns:
        The last consecutive digits or None
    """
    digits = re.findall("([0-9]+)", string)
    if not digits:
        return None
    return int(digits[-1])


def n_smallest_index(lst: List[Num], n: int) -> int:
    """
    Find the n smallest value index from a list

    Args:
        lst (List[Num]): a list of integers or floats
        n (int): the n smallest value index
    Returns:
        The n smallest index
    """
    if n < 0:
        n = max(n, -len(lst))
    else:
        n = min(n, len(lst) - 1)
    return np.argsort(np.array(lst))[n]


def select_element(lst: List[str], n: int = 0, meta: MetaType = MetaType.CELL) -> str:
    """
    Function to select the correct cell/repetition/sweep

    Args:
        lst (List[Num]): a list of integers or floats
        n (int): the n smallest value index
        meta (str):
    Returns:
        The n smallest index
    Raises:
        NoCellFound: HTTPException if no cell is found
        NoRepetitionFound: HTTPException if no repetition is found
        NoSweepFound: HTTPException if no sweep is found
    """
    if not lst:
        if meta == MetaType.CELL:
            raise NoCellFound
        if meta == MetaType.REPETITION:
            raise NoRepetitionFound
        raise NoSweepFound
    if len(lst) == 1:
        return lst[0]
    cell_digits = [find_digits(cell) for cell in lst]
    cell_digits = [d if d is not None else np.nan for d in cell_digits]
    return lst[n_smallest_index(cell_digits, n)]


def select_protocol(lst_protocols: List[str]) -> str:
    """
    Function that selects a protocol

    Args:
        lst_protocols: a list of the protocols
    Returns:
        The selected protocol
    Raises:
        NoProtocolFound: HTTPException if no protocol is found
    """
    if not lst_protocols:
        raise NoProtocolFound
    if "IDRest" in lst_protocols:
        return "IDRest"
    if "APWaveform" in lst_protocols:
        return "APWaveform"
    if "IDThres" in lst_protocols:
        return "IDThres"
    return lst_protocols[0]


def select_response(lst: List[str]) -> str:
    """
    Finds the response element (not the stimulus)

    Args:
        lst: list with responses
    Returns:
        The response element
    Raises:
        NoResponseFound: HTTPException if no Response data is found
    """

    response = next((i for i in lst if any(start_str in i for start_str in ["ic_", "vcs_", "ccs_"])), None)
    if response is None:
        raise NoResponseFound

    return response


def get_unit(h5_handle: h5py.File) -> str:
    """
    Gets the unit from the h5 handle

    Args:
        h5_handle: the h5 file
    Returns:
        The unit of the file
    Raises:
        NoUnitFound: HTTPException if no unit is found
    """
    try:
        return h5_handle["data"].attrs["unit"]
    except Exception as exc:
        raise NoUnitFound from exc


def get_rate(h5_handle: h5py.File) -> float:
    """
    Gets the rate from the h5 handle

    Args:
        h5_handle: the h5 file
    Returns:
        The rate of the file
    Raises:
        NoRateFound: HTTPException if no rate is found
    """
    try:
        return float(h5_handle["starting_time"].attrs["rate"])
    except Exception as exc:
        raise NoRateFound from exc


def get_conversion(h5_handle: h5py.File) -> float:
    """
    Gets the conversion from the h5 handle

    Args:
        h5_handle: the h5 file
    Returns:
        The conversion of the file
    Raises:
        NoConversionFound: HTTPException if no conversion is found
    """
    try:
        return float(h5_handle["data"].attrs["conversion"])
    except Exception as exc:
        raise NoConversionFound from exc

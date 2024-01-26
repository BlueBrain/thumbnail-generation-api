"""
Module: trace_img.py

This module provides functions to generate electrophysiology PNG images.
"""

import io
import re
from typing import Any, Union, List

from fastapi import Header
import h5py
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from api.exceptions import (
    NoCellFound,
    NoConversionFound,
    NoIcDataFound,
    NoProtocolFound,
    NoRateFound,
    NoRepetitionFound,
    NoSweepFound,
    NoUnitFound,
)
from api.util import get_buffer, get_file_content, wrap_exceptions

Num = Union[int, float]


def find_digits(string) -> Union[int, None]:
    "get digits last consecutive digits from string"
    digits = re.findall("([0-9]+)", string)
    if not digits:
        return None
    return int(digits[-1])


def n_smallest_index(lst: List[Num], n: int) -> int:
    "find the n smallest value index from a list"
    if n < 0:
        n = max(n, -len(lst))
    else:
        n = min(n, len(lst) - 1)
    return np.argsort(np.array(lst))[n]


def select_element(lst: List[str], n: int = 0, meta: str = "cell") -> str:
    "function to select the correct cell/repetition/seep"
    if not lst:
        if meta == "cell":
            raise NoCellFound
        if meta == "repetition":
            raise NoRepetitionFound
        raise NoSweepFound
    if len(lst) == 1:
        return lst[0]
    if meta == "cell":
        print(f"found more than 1 {meta}, take {n}")
    cell_digits = [find_digits(cell) for cell in lst]
    cell_digits = [d if d is not None else np.nan for d in cell_digits]
    return lst[n_smallest_index(cell_digits, n)]


def select_protocol(lst_protocols: List[str]) -> str:
    "rule to select protocol"
    if not lst_protocols:
        raise NoProtocolFound
    if "IDRest" in lst_protocols:
        print("Info : Using IDRest for thumbnail plot")
        return "IDRest"
    if "APWaveform" in lst_protocols:
        print("Info : Using APWaveform for thumbnail plot")
        return "APWaveform"
    if "IDThres" in lst_protocols:
        print("Info : Using IDThres for thumbnail plot")
        return "IDThres"
    print("Warning : Standard protocols not found, using ", lst_protocols[0], " for thumbnail plot")
    return lst_protocols[0]


def select_response(lst: List[str]) -> str:
    "find the response element (not the stimulus)"
    for elem in lst:
        if "ic_" in elem:
            return elem
    raise NoIcDataFound


def get_unit(h5_handle) -> str:
    "get the unit from the h5 handle"
    try:
        return h5_handle["data"].attrs["unit"]
    except Exception as exc:
        raise NoUnitFound from exc


def get_rate(h5_handle) -> float:
    "get the rate from the h5 handle"
    try:
        return float(h5_handle["starting_time"].attrs["rate"])
    except Exception as exc:
        raise NoRateFound from exc


def get_conversion(h5_handle) -> float:
    "get the conversion from the h5 handle"
    try:
        return float(h5_handle["data"].attrs["conversion"])
    except Exception as exc:
        raise NoConversionFound from exc


def plot_nwb(data: NDArray[Any], unit: str, rate: Num) -> plt.FigureBase:
    """Plots traces"""

    def new_ticks(start, end, xory):
        if start == end:
            start = np.floor(start)
            end = np.ceil(end)
            return np.array([start, end])

        if xory == "x":
            stepsize = round((end - start) / 5 / 100) * 100
            xt = np.linspace(start, end, 6)
            return np.concatenate((np.unique(np.round(xt[:-1] / 100) * 100), xt[-1]), axis=None)

        if xory == "y":
            stepsize = (end - start) / 4
            return np.arange(start, end + stepsize, stepsize)
        return None

    yrunit = None

    # Plotting
    if unit == "volts":
        data = data * 1e3
        yrunit = "mV"
    elif unit == "amperes":
        data = data * 1e12
        yrunit = "pA"

    npoints = data.shape[0]
    timestamps = 1000 * np.linspace(0, npoints / rate, npoints)
    xunit = "ms"

    figsize = (6, 4)
    fontsize = 16

    fig, ax = plt.subplots(figsize=figsize)
    ax.tick_params(labelsize=fontsize)
    ax.plot(timestamps, data, color="black")
    ax.set_xlabel(xunit, fontsize=fontsize)
    ax.set_ylabel(yrunit, fontsize=fontsize)
    ax.xaxis.set_ticks(new_ticks(timestamps.min(), timestamps.max(), "x"))
    ax.set_xticklabels([f"{l:2.0f}" for l in ax.get_xticks()])
    ax.yaxis.set_ticks(new_ticks(min(data), max(data), "y"))
    ax.set_yticklabels([f"{l:2.0f}" for l in ax.get_yticks()])

    figure = fig.figure

    figure.set_tight_layout(True)

    return figure


@wrap_exceptions
def read_trace_img(authorization: str = Header(None), content_url: str = "", dpi: Union[int, None] = 72) -> bytes:
    """Creates and returns an electrophysiology trace image."""
    content: bytes = get_file_content(authorization=authorization, content_url=content_url)

    h5_handle = h5py.File(io.BytesIO(content), "r")

    h5_handle = h5_handle["data_organization"]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0)]
    h5_handle = h5_handle[select_protocol(list(h5_handle.keys()))]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0, meta="repetiton")]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=-3, meta="sweep")]
    h5_handle = h5_handle[select_response(list(h5_handle.keys()))]

    unit = get_unit(h5_handle)
    rate = get_rate(h5_handle)
    conversion = get_conversion(h5_handle)

    data = np.array(h5_handle["data"][:]) * conversion

    fig = plot_nwb(data, unit, rate)

    buffer = get_buffer(fig, dpi)

    return buffer.getvalue()

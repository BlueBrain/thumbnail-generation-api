"""
Module: trace_img.py

This module exposes the business logic for generating trace thumbnails
"""

import io
import h5py
import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Union
from fastapi import Header
from numpy.typing import NDArray
from api.util import get_buffer
from services.nexus import get_file_content
from api.utils.trace_img import select_element, select_protocol, select_response, get_unit, get_conversion, get_rate


Num = Union[int, float]


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


def generate_electrophysiology_image(
    authorization: str = Header(None), content_url: str = "", dpi: Union[int, None] = 72
) -> bytes:
    """Creates and returns an electrophysiology trace image.

    Args:
        authorization (str): The authorization token
        content_url (str): The content URL that contains the NWB file
        dpi: (int|None): Optional parameter that defines the Dots Per Inch of the image result.
                         Higher DPI means higher resolution

    Returns:
        bytes: The image in bytes format
    """
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

    plt.close()

    return buffer.getvalue()

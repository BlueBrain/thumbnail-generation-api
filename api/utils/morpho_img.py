"""
Module: morpho_img.py

This module provides functions to generate morphology PNG images.
"""

import io
from typing import Union
import matplotlib.pyplot as plt
import neurom as nm
from fastapi import Header
from neurom.view import matplotlib_impl, matplotlib_utils
from api.util import get_buffer, get_file_content


def plot_morphology(nrn) -> plt.FigureBase:
    """Creates and formats a FigureBase object."""
    fig, ax = matplotlib_utils.get_figure()

    matplotlib_impl.plot_morph(nrn, ax)

    ax.set_title("")
    ax.set_aspect("equal")
    ax.set_frame_on(False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    bounds = ax.dataLim.bounds
    white_space = 0.05
    ax.set_xlim(bounds[0] - white_space, bounds[0] + bounds[2] + white_space)
    ax.set_ylim(bounds[1] - white_space, bounds[1] + bounds[3] + white_space)

    fig.set_tight_layout(True)

    return fig


def retrieve_and_generate_morpho_image(
    authorization: str = Header(None), content_url: str = "", dpi: Union[int, None] = 72
) -> bytes:
    """
    Returns a PNG image of a morphology (by generating a matplotlib figure from its SWC distribution).

    Parameters:
        - authorization (str): Authorization header containing the access token.
        - content_url (str): URL of the SWC distribution.

    Returns:
        Response: FastAPI Response object containing the PNG image.
    """
    morph = get_file_content(authorization, content_url).decode(encoding="utf-8")

    nrn = nm.load_morphology(io.StringIO(morph), reader="swc")

    fig = plot_morphology(nrn)

    buffer = get_buffer(fig, dpi)

    plt.close()

    return buffer.getvalue()

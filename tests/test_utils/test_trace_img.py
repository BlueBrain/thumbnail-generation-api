import io
import h5py
import pytest
from unittest.mock import patch
from api.exceptions import NoCellFound, NoProtocolFound, NoRepetitionFound, NoSweepFound
from tests.fixtures.nexus import trace_content
from api.utils.trace_img import select_element, select_protocol


def test_select_element_returns_correct_element_if_correct_trace(trace_content):
    """
    Tests whether the select_element util function returns the correct element
    """

    h5_handle = h5py.File(io.BytesIO(trace_content), "r")

    element = select_element(list(h5_handle.keys()), n=0)
    assert element == "acquisition"


def test_select_element_raises_exception_if_no_list_and_cell():
    """
    Tests whether the select_element util function raises correct exception if no list
    """

    with pytest.raises(NoCellFound):
        select_element([], meta="cell")


def test_select_element_raises_exception_if_no_list_and_repetition():
    """
    Tests whether the select_element util function raises correct exception if no list
    """

    with pytest.raises(NoRepetitionFound):
        select_element([], meta="repetition")


def test_select_element_raises_exception_if_no_list():
    """
    Tests whether the select_element util function raises correct exception if no list
    """

    with pytest.raises(NoSweepFound):
        select_element([], meta="sweep")


def test_select_protocol_returns_correct_protocol():
    """
    Tests whether the select_element util function returns the correct protocol
    """
    protocols = [
        "ADHPdepol",
        "ADHPhyperpol",
        "ADHPrest",
        "APDrop",
        "APThreshold",
        "APWaveform",
        "Delta",
        "IDRest",
        "IDdepol",
        "IDhyperpol",
        "IDthresh",
        "IRdepol",
        "IRhyperpol",
        "IRrest",
    ]
    selected_protocol = select_protocol(protocols)
    assert selected_protocol == "IDRest"


def test_select_protocol_raises_exception_if_no_protocols():
    """
    Tests whether the select_element util function raises exception if no protocols
    """
    with pytest.raises(NoProtocolFound):
        select_protocol([])

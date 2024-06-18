"""
Unit tests related to testing utils of trace image generation
"""

import io
import h5py
import pytest
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
from api.models.enums import MetaType
from tests.fixtures.nexus import trace_content
from api.utils.trace_img import get_conversion, get_rate, get_unit, select_element, select_protocol, select_response


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
        select_element([], meta=MetaType.CELL)


def test_select_element_raises_exception_if_no_list_and_repetition():
    """
    Tests whether the select_element util function raises correct exception if no list
    """

    with pytest.raises(NoRepetitionFound):
        select_element([], meta=MetaType.REPETITION)


def test_select_element_raises_exception_if_no_list():
    """
    Tests whether the select_element util function raises correct exception if no list
    """

    with pytest.raises(NoSweepFound):
        select_element([], meta=MetaType.SWEEP)


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


def test_select_response_returns_correct_response():
    """
    Tests whether the select_response util function returns the correct response
    """

    responses = ["ic__IDRest__033", "ics__IDRest__033"]
    selected_response = select_response(responses)
    assert selected_response == "ic__IDRest__033"


def test_select_response_raises_exception_if_no_response_with_ic():
    """
    Tests whether the select_response util function raises exception if not response with ic prefix
    """

    responses = ["IDRest__033", "test_IDRest__033"]
    with pytest.raises(NoIcDataFound):
        select_response(responses)


def test_get_unit_returns_correct_unit(trace_content):
    """
    Tests whether the get_unit() function returns correct unit
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    h5_handle = h5_handle["data_organization"]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0)]
    h5_handle = h5_handle[select_protocol(list(h5_handle.keys()))]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0, meta="repetiton")]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=-3, meta="sweep")]
    h5_handle = h5_handle[select_response(list(h5_handle.keys()))]
    element = get_unit(h5_handle)
    assert element == "volts"


def test_get_unit_raises_exception_if_no_unit(trace_content):
    """
    Tests whether the get_unit() function raises correct exception if no unit present
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    with pytest.raises(NoUnitFound):
        get_unit(h5_handle)


def test_get_rate_returns_correct_unit(trace_content):
    """
    Tests whether the get_rate() function returns correct rate
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    h5_handle = h5_handle["data_organization"]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0)]
    h5_handle = h5_handle[select_protocol(list(h5_handle.keys()))]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0, meta="repetiton")]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=-3, meta="sweep")]
    h5_handle = h5_handle[select_response(list(h5_handle.keys()))]
    element = get_rate(h5_handle)
    assert element == 4000


def test_get_rate_raises_exception_if_no_unit(trace_content):
    """
    Tests whether the get_rate() function raises correct exception if no rate present
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    with pytest.raises(NoRateFound):
        get_rate(h5_handle)


def test_get_conversion_returns_correct_conversion(trace_content):
    """
    Tests whether the get_conversion() function returns correct conversion
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    h5_handle = h5_handle["data_organization"]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0)]
    h5_handle = h5_handle[select_protocol(list(h5_handle.keys()))]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=0, meta="repetiton")]
    h5_handle = h5_handle[select_element(list(h5_handle.keys()), n=-3, meta="sweep")]
    h5_handle = h5_handle[select_response(list(h5_handle.keys()))]
    element = get_conversion(h5_handle)
    assert element == 0.001


def test_get_conversion_raises_exception_if_no_conversion(trace_content):
    """
    Tests whether the get_conversion() function raises correct exception if no conversion present
    """
    h5_handle = h5py.File(io.BytesIO(trace_content), "r")
    with pytest.raises(NoConversionFound):
        get_conversion(h5_handle)

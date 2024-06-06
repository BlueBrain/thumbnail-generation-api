import pytest
from ..trace_img import (
    find_digits,
    n_smallest_index,
    select_element,
    select_protocol,
    select_response,
    get_unit,
    get_rate,
    get_conversion,
)
from ..exceptions import (
    NoCellFound,
    NoRepetitionFound,
    NoProtocolFound,
    NoIcDataFound,
    NoUnitFound,
    NoRateFound,
    NoConversionFound,
)

import h5py


class TestFindDigits:
    @staticmethod
    def test_find_digits():
        digits = find_digits("123abc321")
        assert digits == 321

    @staticmethod
    def test_find_digits_with_no_digits():
        digits = find_digits("asdqweasd")
        assert digits is None

    @staticmethod
    def test_find_digits_empty_string():
        digits = find_digits("")
        assert digits is None


class TestNSmallest:
    """Tests for the utils.n_smallest_index function."""

    @staticmethod
    def test_n_smallest():
        """
        Finds the correct smallest elements based on the index (n).

        Tests that the function identifies and returns the correct smallest elements
        in a list based on the provided index.
        """
        smallest = n_smallest_index([0, -1, 10, 15, 2], 0)
        assert smallest == 1

        smallest = n_smallest_index([0, -1, 10, 15, 2], 1)
        assert smallest == 0

        smallest = n_smallest_index([0, -1, 10, 15, 2], 2)
        assert smallest == 4

        smallest = n_smallest_index([0, -1, 10, 15, 2], -1)
        assert smallest == 3

    def test_n_smallest_empty_array():
        """
        This test calls n_smallest_index with an empty array.
        Expected behaviour is throwing an exception?
        """

        _ = n_smallest_index([], 0)

    @staticmethod
    def test_n_smallest_unit_array():
        """
        This test validates that the n_smallest_index function can handle cases
        where the input list contains only a single element.
        """
        smallest = n_smallest_index([1], 0)
        assert smallest == 0

    @staticmethod
    def test_n_smallest_n_out_of_bounds():
        """
        This test verifies that the n_smallest_index function behaves
        correctly when the provided index (n) is outside the valid range for
        the list size.
        """
        smallest = n_smallest_index([1], 100)
        assert smallest == 0

        smallest = n_smallest_index([1], -100)
        assert smallest == 0


class TestSelectElement:
    """
    Tests cases for the select_element function.
    """

    @staticmethod
    def test_empty_list():
        """
        Tests that select_element raises a NoCellFound exception
        for cases when the input list is empty and the meta argument is set to "cell".
        """
        with pytest.raises(NoCellFound):
            _ = select_element([], 0, meta="cell")

    @staticmethod
    def test_empty_list_repetition():
        """
        Tests that select_element raises a NoRepetitionFound exception
        for cases when the input list is empty and the meta argument is set to "repetition".
        """
        with pytest.raises(NoRepetitionFound):
            _ = select_element([], 0, meta="repetition")

    @staticmethod
    def test_unit_list():
        """
        Tests that select_element can handle cases where the input list
        contains only a single element, returning that element for both "cell" and
        "repetition" meta types.
        """
        result = select_element(["unit"], 0, meta="repetition")
        assert result == "unit"

        result = select_element(["unit1"], 100, meta="cell")
        assert result == "unit1"

    @staticmethod
    def test_select_element():
        """
        Tests that select_element chooses the smallest element (based
        on string value)
        """
        result = select_element(["unit234", "unit123"], 0, meta="cell")
        assert result == "unit123"

        result = select_element(
            ["unit234", "unit123", "000thisisthesmallest00"], 0, meta="cell"
        )
        assert result == "000thisisthesmallest00"

    @staticmethod
    def test_select_element_equality():
        """
        Tests that select_element returns the first element encountered
        in cases where there are duplicate elements (with the smallest value)
        """
        result = select_element(
            ["thisisalsothesmallest00", "000thisisthesmallest00"], 0, meta="cell"
        )
        assert result == "thisisalsothesmallest00"


class TestSelectProtocol:
    @staticmethod
    def test_empty_list():
        """
        Tests if selecting a protocol from an empty list raises NoProtocolFound exception.
        """
        with pytest.raises(NoProtocolFound):
            select_protocol([])

    @staticmethod
    def test_idrest_found():
        """
        Tests if select_protocol finds "IDRest" protocol from a list with various protocols.
        """
        protocols = ["IDRest", "Other", "Test", "Protocols"]
        selected_protocol = select_protocol(protocols)
        assert selected_protocol == "IDRest"

    @staticmethod
    def test_apwaveform_found():
        """
        Tests if select_protocol finds "APWaveform" protocol from a list with various protocols.
        """
        protocols = ["APWaveform", "Other", "Test", "Protocols"]
        selected_protocol = select_protocol(protocols)
        assert selected_protocol == "APWaveform"

    @staticmethod
    def test_idthres_found():
        """
        Tests if select_protocol finds "IDThres" protocol from a list with various protocols.
        """
        protocols = ["IDThres", "Other", "Test", "Protocols"]
        selected_protocol = select_protocol(protocols)
        assert selected_protocol == "IDThres"

    @staticmethod
    def test_standard_protocols_not_found():
        """
        Tests if select_protocol returns the first protocol if standard protocols are not found.
        """
        protocols = ["FirstProtocol", "Other", "Test", "Protocols", "AnotherOne"]
        selected_protocol = select_protocol(protocols)
        assert selected_protocol == "FirstProtocol"



class TestSelectResponse:

    @staticmethod
    def test_empty_list():
        """
        Tests if selecting a response from an empty list raises NoIcDataFound exception 
        in cases when the input list is empty.
        """
        with pytest.raises(NoIcDataFound):
            select_response([])

    @staticmethod
    def test_select_response():
        """
        Tests if select_response correctly identifies "ic_data_1" from a list containing it
        In cases when the list contains "ic_data_1".
        """
        selected_response = select_response(
            ["this", "ic_data_1", "is", "just", "a", "test"]
        )
        assert selected_response == "ic_data_1"

    @staticmethod
    def test_no_ic_data_found():
        """
        Tests if selecting a response from a list without "ic_data_1" raises NoIcDataFound exception.
        In cases when the list does not contain "ic_data_1".
        """
        data = ["this", "is", "just", "a", "test"]
        with pytest.raises(NoIcDataFound):
            select_response(data)


class TestH5py:
    @staticmethod
    def create_h5file(
        test_file, group: str, key: str | None, value: str | float | None
    ):
        with h5py.File(test_file, "w") as file:
            data_group = file.create_group(group)
            if key is not None and value is not None:
                data_group.attrs[key] = value

    def test_unit_in_file(self, tmp_path):
        """
        Tests if get_unit retrieves the expected value "Unit" from the HDF5 file
        in cases when the HDF5 file contains the 'unit' attribute within the 'data' group.
        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(test_file, group="data", key="unit", value="Unit")

        with h5py.File(test_file, "r") as file:
            unit = get_unit(file)

        assert unit == "Unit"

    def test_unit_not_in_file(self, tmp_path):
        """
        Tests if get_unit raises NoUnitFound exception when the attribute is missing
        in cases when the HDF5 file does not contain the 'unit' attribute within any group.
        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(test_file, group="random_group", key=None, value=None)

        with h5py.File(test_file, "r") as file, pytest.raises(NoUnitFound):
            _ = get_unit(file)

    def test_get_rate(self, tmp_path):
        """
        Tests if get_rate retrieves the expected rate value from the HDF5 file
        in cases when the HDF5 file contains the 'rate' attribute within the 'starting_time' group.
        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(
            test_file, group="starting_time", key="rate", value=3.14159265359
        )

        with h5py.File(test_file, "r") as file:
            rate = get_rate(file)

        assert rate == 3.14159265359

    def test_rate_not_in_file(self, tmp_path):
        """
        Tests if get_rate raises NoRateFound exception in cases when attribute is missing

        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(test_file, group="random_group", key=None, value=None)

        with h5py.File(test_file, "r") as file, pytest.raises(NoRateFound):
            _ = get_rate(file)

    def test_get_conversion(self, tmp_path):
        """
        Tests if get_conversion retrieves the expected conversion value from the HDF5 file.
        In cases when the HDF5 file contains the 'conversion' attribute within the 'data' group,
        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(
            test_file, group="data", key="conversion", value=3.14159265359
        )

        with h5py.File(test_file, "r") as file:
            conversion = get_conversion(file)

        assert conversion == 3.14159265359

    def test_conversion_not_in_file(self, tmp_path):
        """
        Tests if get_conversion raises NoConversionFound exception in cases when attribute is missing
        """
        test_file = tmp_path / "test.h5"

        self.create_h5file(test_file, group="random_group", key=None, value=None)

        with h5py.File(test_file, "r") as file, pytest.raises(NoConversionFound):
            _ = get_conversion(file)

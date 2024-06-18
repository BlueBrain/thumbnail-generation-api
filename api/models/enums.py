"""
Definition of application enums
"""

from enum import Enum


class MetaType(Enum):
    """
    Meta type definition for element selection in trace thumbnail  generation
    """

    CELL = "cell"
    REPETITION = "repetition"
    SWEEP = "sweep"

"""
Model module defining models related to images
"""

from typing import List, Literal, Optional
from fastapi import Query
from pydantic import BaseModel


class ImageGenerationInput(BaseModel):
    """
    The input format for image generation
    """

    content_url: str
    dpi: Optional[int] = Query(None, ge=10, le=600)


PlotType = Literal["stimulus", "simulation"]


class SimulationGenerationInput(BaseModel):
    """
    The input format for image generation
    """

    content_url: str
    type: PlotType
    w: Optional[int] = None
    h: Optional[int] = None


class SingleNeuronModelSimulationConfig(BaseModel):
    celsius: float
    hypamp: float
    vinit: float
    injectTo: str
    recordFrom: List[str]
    stimulus: dict
    synaptome: Optional[dict] = None


class PlotData(BaseModel):
    x: List[float]
    y: List[float]
    type: str
    name: str


class StimulusPlotData(BaseModel):
    id: str
    data: List[PlotData]


class SimulationConfigurationFile(BaseModel):
    stimulus: List[StimulusPlotData]
    simulation: List[PlotData]
    config: SingleNeuronModelSimulationConfig


class ErrorMessage(BaseModel):
    """
    Model of an error message
    """

    detail: str

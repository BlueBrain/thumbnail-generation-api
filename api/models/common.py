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


PlotTarget = Literal["stimulus", "simulation"]


class SimulationGenerationInput(BaseModel):
    """
    The input format for image generation
    """

    content_url: str
    target: PlotTarget
    w: Optional[int] = None
    h: Optional[int] = None


class SimulationRecording(BaseModel):
    """
    Simulation recording section/offset
    """

    section: str
    offset: float


class SimulationCurrentInjection(BaseModel):
    """
    Simulation current injection location
    """

    id: int
    configId: str
    injectTo: str
    stimulus: dict


class SimulationExperimentSetup(BaseModel):
    """
    Simulation experiment setup global config
    """

    celsius: float
    vinit: float
    hypamp: float
    max_time: float


class SingleNeuronModelSimulationConfig(BaseModel):
    """
    Simulation configuration (allow both single neuron and synaptome)
    """

    recordFrom: List[SimulationRecording]
    conditions: SimulationExperimentSetup
    currentInjection: SimulationCurrentInjection
    synaptome: Optional[List[dict]] = None


class PlotData(BaseModel):
    """
    Plotly data format
    """

    x: List[float]
    y: List[float]
    type: str
    name: str
    # recording: Optional[str]


class SimulationConfigurationFile(BaseModel):
    """
    Configuration file content for simulation
    """

    stimulus: List[PlotData]
    simulation: dict[str, List[PlotData]]
    config: SingleNeuronModelSimulationConfig


class ErrorMessage(BaseModel):
    """
    Model of an error message
    """

    detail: str

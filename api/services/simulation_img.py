from typing import List
import plotly.graph_objects as go
import io
import json

from api.models.common import (
    PlotData,
    SimulationConfigurationFile,
    SimulationGenerationInput,
)
from api.services.nexus import fetch_file_content


def generate_simulation_plots(
    access_token: str,
    config: SimulationGenerationInput,
):
    response = fetch_file_content(access_token, config.content_url).decode(encoding="utf-8")
    simulation_config = SimulationConfigurationFile(**json.loads(response))
    data: List[PlotData] = []

    if config.target == "stimulus":
        stimulus_config = simulation_config.stimulus
        # TODO: in the future the stimulus may have different configs
        # TODO: we should agree how the user can specify the stimulus thumb needed
        if len(stimulus_config) > 0:
            data = stimulus_config[0].data
    elif config.target == "simulation":
        data = simulation_config.simulation

    if len(data):
        fig = go.Figure(
            data=[dict(x=pd.x, y=pd.y, type=pd.type, name=pd.name) for pd in data],
            layout={
                "showlegend": False,
                "margin": {"t": 4, "r": 4, "l": 4, "b": 4},
            },
        )
        buffer = io.BytesIO()
        fig.write_image(
            buffer,
            format="png",
            width=config.w,
            height=config.h,
        )
        buffer.seek(0)

        return buffer.getvalue()
    else:
        return None

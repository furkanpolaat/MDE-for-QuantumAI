# Copyright 2024 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This file stores the HTML layout for the app (see ``mvrp.css`` for CSS styling)."""
from __future__ import annotations

from dash import dcc, html

from app_configs import (
    COST_LABEL,
    DESCRIPTION,
    LOCATIONS_LABEL,
    MAIN_HEADER,
    NUM_CLIENT_LOCATIONS,
    NUM_VEHICLES,
    RESOURCES,
    SHOW_COST_COMPARISON,
    SHOW_DQM,
    SOLVER_TIME,
    THEME_COLOR_SECONDARY,
    THUMBNAIL,
    UNITS_IMPERIAL,
    THEME_COLOR,
)
from solver.solver import SamplerType, VehicleType
import os


map_width, map_height = 1000, 600

VEHICLE_TYPES = {VehicleType.TRUCKS: "Trucks", VehicleType.DELIVERY_DRONES: "Delivery Drones"}
SAMPLER_TYPES = {SamplerType.NL: "Quantum Hybrid (NL)", SamplerType.KMEANS: "Classical (K-Means)"}

if SHOW_DQM:
    SAMPLER_TYPES[SamplerType.DQM] = "Quantum Hybrid (DQM)"
def dropdown(label: str, id: str, options: list) -> html.Div:
    """Slider element for value selection."""
    return html.Div(
        children=[
            html.Label(label),
            dcc.Dropdown(
                id=id,
                options=options,
                value=options[0]["value"],
                clearable=False,
                searchable=False,
            ),
        ],
    )

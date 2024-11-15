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

import os
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



from generate_control_card import generate_control_card
from generate_control_card import SAMPLER_TYPES
map_width, map_height = 1000, 600

VEHICLE_TYPES = {VehicleType.TRUCKS: "Trucks", VehicleType.DELIVERY_DRONES: "Delivery Drones"}

if SHOW_DQM:
    SAMPLER_TYPES[SamplerType.DQM] = "Quantum Hybrid (DQM)"


def description_card():
    """A Div containing dashboard title & descriptions."""
    return html.Div(
        id="description-card",
        children=[html.H1(MAIN_HEADER), html.P(DESCRIPTION)],
    )


def set_html(app):
    """Set the application HTML with the control panel on top."""
    app.layout = html.Div(
        id="app-container",
        children=[
            # Temporary storage items for sharing data between callbacks
            dcc.Store(id="stored-results"),  # Temporarily stored results table
            dcc.Store(id="sampler-type"),  # Solver type used for the latest run
            dcc.Store(id="reset-results"),  # Reset the results tables before displaying the latest run
            dcc.Store(id="run-in-progress", data=False),  # Callback blocker to signal run completion
            dcc.Store(id="parameter-hash"),  # Hash string to detect changed parameters
            dcc.Store(id="cost-comparison"),  # Dictionary with solver keys and run values

            # Banner
            html.Div(id="banner", children=[html.Img(src=THUMBNAIL)]),

            # Top control panel
            html.Div(
                id="top-control-panel",
                className="top-control-panel",
                children=[
                    description_card(),
                    generate_control_card(),
                ],
                style={
                    "width": "100%",
                    "padding": "10px 20px",
                    "background-color": "#f9f9f9",
                    "border-bottom": "1px solid #ddd",
                    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                    "margin-bottom": "20px",
                },
            ),

            # Main content: Map and Results Tabs
            html.Div(
                id="columns",
                children=[
                    html.Div(
                        id="right-column",
                        children=[
                            dcc.Tabs(
                                id="tabs",
                                value="map-tab",
                                mobile_breakpoint=0,
                                children=[
                                    dcc.Tab(
                                        label="Map",
                                        id="map-tab",
                                        value="map-tab",  # Used for programmatic switching
                                        className="tab",
                                        children=[
                                            dcc.Loading(
                                                id="loading",
                                                type="circle",
                                                color=THEME_COLOR_SECONDARY,
                                                children=html.Iframe(
                                                    id="solution-map", style={"width": "100%", "height": "600px"}
                                                ),
                                            ),
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Results",
                                        id="results-tab",
                                        className="tab",
                                        disabled=True,
                                        children=[
                                            html.Div(
                                                className="tab-content--results",
                                                children=[
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                className="results-tables",
                                                                children=[
                                                                    html.Div(
                                                                        id="solution-cost-table-div",
                                                                        className="result-table-div",
                                                                        children=[
                                                                            html.H3(
                                                                                className="table-label",
                                                                                children=[
                                                                                    html.Span(id="hybrid-table-label"),
                                                                                    " Results",
                                                                                ],
                                                                            ),
                                                                            html.Div(
                                                                                title="Quantum Hybrid",
                                                                                id="solution-cost-table",
                                                                                children=[],  # Add dynamically using `create_table`
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        id="solution-cost-table-classical-div",
                                                                        className="result-table-div",
                                                                        children=[
                                                                            html.H3(
                                                                                children=["Classical (K-Means) Results"],
                                                                                className="table-label",
                                                                            ),
                                                                            html.Div(
                                                                                title="Classical (K-Means)",
                                                                                id="solution-cost-table-classical",
                                                                                children=[],  # Add dynamically using `create_table`
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            html.H4(
                                                                id="performance-improvement-quantum",
                                                                className=(
                                                                    "" if SHOW_COST_COMPARISON else "display-none"
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Hr(),
                                                            html.Div(
                                                                id={"type": "to-collapse-class", "index": 1},
                                                                className="details-collapse-wrapper collapsed",
                                                                children=[
                                                                    html.Button(
                                                                        id={"type": "collapse-trigger", "index": 1},
                                                                        className="details-collapse",
                                                                        children=[
                                                                            html.H5("Problem Details"),
                                                                            html.Div(className="collapse-arrow"),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="details-to-collapse",
                                                                        children=[
                                                                            html.Table(
                                                                                id="solution-stats-table",
                                                                                children=[
                                                                                    html.Thead(
                                                                                        [
                                                                                            html.Tr(
                                                                                                [
                                                                                                    html.Th(
                                                                                                        colSpan=2,
                                                                                                        children=[
                                                                                                            "Problem Specifics"
                                                                                                        ],
                                                                                                    ),
                                                                                                    html.Th(
                                                                                                        colSpan=2,
                                                                                                        children=[
                                                                                                            "Wall Clock Time"
                                                                                                        ],
                                                                                                    ),
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    ),
                                                                                    html.Tbody(
                                                                                        id="problem-details",
                                                                                        children=[
                                                                                            html.Tr(
                                                                                                [
                                                                                                    html.Td(
                                                                                                        LOCATIONS_LABEL
                                                                                                    ),
                                                                                                    html.Td(
                                                                                                        id="num-locations"
                                                                                                    ),
                                                                                                    html.Td(
                                                                                                        "DWave Quantum Annealing Hybrid"
                                                                                                    ),
                                                                                                    html.Td(
                                                                                                        id="wall-clock-time-quantum"
                                                                                                    ),
                                                                                                ]
                                                                                            ),
                                                                                            html.Tr(
                                                                                                [
                                                                                                    html.Td(
                                                                                                        "Vehicles Deployed"
                                                                                                    ),
                                                                                                    html.Td(
                                                                                                        id="vehicles-deployed"
                                                                                                    ),
                                                                                                    html.Td("Classical"),
                                                                                                    html.Td(
                                                                                                        id="wall-clock-time-classical"
                                                                                                    ),
                                                                                                ]
                                                                                            ),
                                                                                            html.Tr(
                                                                                                [
                                                                                                    html.Td(
                                                                                                        "Problem Size"
                                                                                                    ),
                                                                                                    html.Td(id="problem-size"),
                                                                                                ]
                                                                                            ),
                                                                                            html.Tr(
                                                                                                [
                                                                                                    html.Td(
                                                                                                        "Search Space"
                                                                                                    ),
                                                                                                    html.Td(id="search-space"),
                                                                                                ]
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def create_row_cells(values: list) -> list[html.Td]:
    """List required to execute loop, unpack after to maintain required structure."""
    return [
        html.Td(round(value, 3 if UNITS_IMPERIAL else 0))
        for value in values
    ]


def create_table(values_dicts: dict[int, dict], values_totals: list) -> html.Table:
    """Create a table dynamically.

    Args:
        values_dicts: Dictionary with vehicle id keys and results data as values.
        values_totals: List of total results data (sum of individual vehicle data).
    """

    headers = ["Vehicle ID", COST_LABEL, LOCATIONS_LABEL, *RESOURCES]

    table = html.Table(
        className="results result-table",
        children=[
            html.Thead([html.Tr([html.Th(header) for header in headers])]),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(vehicle),
                            *create_row_cells(
                                list(results.values())
                            ),  # Unpack list to maintain required structure
                        ]
                    )
                    for vehicle, results in values_dicts.items()
                ]
            ),
            html.Tfoot(
                [
                    html.Tr(
                        [
                            html.Td("Total"),
                            *create_row_cells(
                                values_totals
                            ),  # Unpack list to maintain required structure
                        ],
                        className="total-cost-row",
                    )
                ]
            ),
        ],
    )

    return table

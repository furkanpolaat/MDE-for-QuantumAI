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


map_width, map_height = 1000, 600

VEHICLE_TYPES = {VehicleType.TRUCKS: "Trucks", VehicleType.DELIVERY_DRONES: "Delivery Drones"}
SAMPLER_TYPES = {SamplerType.NL: "Quantum Hybrid (NL)", SamplerType.KMEANS: "Classical (K-Means)"}

if SHOW_DQM:
    SAMPLER_TYPES[SamplerType.DQM] = "Quantum Hybrid (DQM)"

def slider(label: str, id: str, config: dict) -> html.Div:
    """Slider element for value selection."""
    return html.Div(
        children=[
            html.Label(label),
            dcc.Slider(
                id=id,
                className="slider",
                **config,
                marks={
                    config["min"]: str(config["min"]),
                    config["max"]: str(config["max"]),
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": True,
                },
            ),
        ],
    )

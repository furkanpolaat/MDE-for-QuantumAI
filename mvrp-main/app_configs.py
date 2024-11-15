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

"""This file stores input parameters for the app."""

# Sets Dash debug which hides and shows Dash debug menu.
# Set to True if developing and False if demoing.
# App should be restarted to see change.
DEBUG = False

# Shows/hides Quantum Hybrid vs Classical cost comparison in the
# results tab when both are run with the same settings.
SHOW_COST_COMPARISON = False

# Units will be in miles if true, meters if false
# If updated, make sure units match COST_LABEL below
UNITS_IMPERIAL = False
COST_LABEL = "Distance (m)"  # Either "Distance (m)" or specific distance cost description

# THEME_COLOR is used for the button, text, and banner and should be dark
# and pass accessibility checks with white: https://webaim.org/resources/contrastchecker/
# THEME_COLOR_SECONDARY can be light or dark and is used for sliders, loading icon, and tabs
THEME_COLOR = "#BE273E"
THEME_COLOR_SECONDARY = "#2A7DE1"  # D-Wave blue default #2A7DE1

# ADDRESS = "Cambridge Ln, Rockhampton QLD 4700, Australia"
# DISTANCE = 1700  # bounding box distance (in meters) around address
# THUMBNAIL = "assets/dwave_logo.svg"

# Replace the existing address with a more specific one
ADDRESS = "Antwerp, Belgium"
DISTANCE = 1000 # Adjust as needed for the bounding box distance around Antwerp
THUMBNAIL = "assets/a-logo.svg"

APP_TITLE = "QauntumTraffic"
MAIN_HEADER = " Routing Calculation with Quantum Computing (City of Antwerp Demo)"
DESCRIPTION = """\
This demo is to optimize routes for the data points from open data of the City of Antwerp. Users can upload their datasets directly through the platform and select from various solver types, including classical and quantum hybrid algorithms.the result section allows the comparisation of the alghoritms efficiency in solving real-world logistics challenges. The demo also allows users to customize settings, enabling them to adjust parameters and tailor the optimization process to their specific requirements."""

DEPOT_LABEL = "Depot"  # Either "Depot" or specific start location
LOCATIONS_LABEL = "Locations"  # Either "Locations" or business specific location type
RESOURCES = ["R1", "R2", "R3"]  # Supports any number of resources

SHOW_DQM = False  # Show/hide DQM drop down option

#######################################
# Sliders, buttons and option entries #
#######################################

# number of vehicles slider (value means default)
NUM_VEHICLES = {
    "min": 1,
    "max": 10,
    "step": 1,
    "value": 1,
}

# number of client locations slider (value means default)
NUM_CLIENT_LOCATIONS = {
    "min": 10,
    "max": 500,
    "step": 1,
    "value": 200,
}

# solver time limits in seconds (value means default)
SOLVER_TIME = {
    "min": 10,
    "max": 300,
    "step": 5,
    "value": 10,
}


# solver time limits in seconds (value means default)
BOUNDING_BOX_DISTANCE = {
    "min": 100,
    "max": 2000,
    "step": 10,
    "value": 1000,
}
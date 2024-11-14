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

from __future__ import annotations

import random
from pathlib import Path
import pandas as pd
import pyproj
import folium
import folium.plugins as plugins
import networkx as nx
import numpy as np
import osmnx as ox
from numpy.typing import NDArray
from scipy.spatial import cKDTree

from app_configs import DEPOT_LABEL, DISTANCE, RESOURCES

from solver.solver import VehicleType

ox.settings.use_cache = True
ox.settings.overpass_rate_limit = False


depot_icon_path = Path(__file__).parent / "assets/depot_location.png"
depot_icon = folium.CustomIcon(str(depot_icon_path), icon_size=(30, 48))

# Define depot coordinates as a constant
DEPOT_LAT = 51.20451936274899
DEPOT_LON = 4.404572523753899

def _get_coordinates(node_index_map: dict) -> NDArray:
    """Returns an array of coordinates for all nodes."""
    coordinates = np.zeros((len(node_index_map), 2))
    for node_index, node in node_index_map.items():
        coordinates[node_index][0] = node[1]["y"]
        coordinates[node_index][1] = node[1]["x"]

    return coordinates



def generate_mapping_information(file_path: str, num_clients: int) -> tuple[nx.MultiDiGraph, int, list, list]:
    """Return `nx.MultiDiGraph with client demand, depot id in graph, client ids in graph.

    Args:
        num_clients: Number of locations to be visited in total.

    Returns:
        map_network: `nx.MultiDiGraph where nodes and edges represent locations and routes.
        depot_id: Node ID of the depot location.
        client_subset: List of client IDs in the map's graph.
        map_bounds: List of lower and upper bound locations for map
    """
    # Load glass container locations from CSV

    client_csv_file_df = pd.read_csv(file_path)

    # Initialize the transformer (from EPSG:3857 to EPSG:4326 for lat/long)
    transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Convert the X and Y coordinates to latitude and longitude
    def convert_coordinates(x, y):
        lon, lat = transformer.transform(x, y)
        return lat, lon

    # Create new Latitude and Longitude columns
    client_csv_file_df['Latitude'] = None
    client_csv_file_df['Longitude'] = None

    for i in range(len(client_csv_file_df)):
        x = client_csv_file_df.loc[i, 'X']
        y = client_csv_file_df.loc[i, 'Y']
        lat, lon = convert_coordinates(x, y)
        client_csv_file_df.at[i, 'Latitude'] = lat
        client_csv_file_df.at[i, 'Longitude'] = lon

    # Use the transformed coordinates for glass client_csv_file
    transformed_client_csv_file = client_csv_file_df[['Latitude', 'Longitude']]

    # Generate graph centered on the depot location using OSMnx
    G = ox.graph_from_point((DEPOT_LAT, DEPOT_LON), dist=DISTANCE, network_type="drive", truncate_by_edge=True)





    # Get largest component (important for road connections)
    map_network = ox.utils_graph.get_largest_component(G, strongly=True)

    # Find the nearest node to the depot in the graph
    depot_node = ox.distance.nearest_nodes(map_network, DEPOT_LON, DEPOT_LAT)

    # Select the glass client_csv_file as client locations
    client_subset = transformed_client_csv_file.values.tolist()[:num_clients]

    # Ensure that client locations have default values for all resources (water, food, etc.)
    for lat, lon in client_subset:
        nearest_node = ox.distance.nearest_nodes(map_network, lon, lat)
        map_network.nodes[nearest_node]["demand"] = 0

        # Assign default values of 1 to each resource
        for i in range(len(RESOURCES)):
            map_network.nodes[nearest_node][f"resource_{i}"] = 1
            map_network.nodes[nearest_node]["demand"] += map_network.nodes[nearest_node][f"resource_{i}"]

    # Get min and max coordinates to determine map bounds
    coordinates = _get_coordinates(dict(enumerate(map_network.nodes(data=True))))
    map_bounds = [coordinates.min(0).tolist(), coordinates.max(0).tolist()]

    return map_network, depot_node, client_subset, map_bounds

def agenerate_mapping_information(file_path: str,bb_distance: int , num_clients: int) -> tuple[nx.MultiDiGraph, int, list, list]:
    """Return `nx.MultiDiGraph with client demand, depot id in graph, client ids in graph.

    Args:
        num_clients: Number of locations to be visited in total.

    Returns:
        map_network: `nx.MultiDiGraph where nodes and edges represent locations and routes.
        depot_id: Node ID of the depot location.
        client_subset: List of client IDs in the map's graph.
        map_bounds: List of lower and upper bound locations for map
    """
    # Load glass container locations from CSV

    client_csv_file_df = pd.read_csv(file_path)

    # Initialize the transformer (from EPSG:3857 to EPSG:4326 for lat/long)
    transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Convert the X and Y coordinates to latitude and longitude
    def convert_coordinates(x, y):
        lon, lat = transformer.transform(x, y)
        return lat, lon

    # Create new Latitude and Longitude columns
    client_csv_file_df['Latitude'] = None
    client_csv_file_df['Longitude'] = None

    for i in range(len(client_csv_file_df)):
        x = client_csv_file_df.loc[i, 'X']
        y = client_csv_file_df.loc[i, 'Y']
        lat, lon = convert_coordinates(x, y)
        client_csv_file_df.at[i, 'Latitude'] = lat
        client_csv_file_df.at[i, 'Longitude'] = lon

    # Use the transformed coordinates for glass client_csv_file
    transformed_client_csv_file = client_csv_file_df[['Latitude', 'Longitude']]

    # Generate graph centered on the depot location using OSMnx
    G = ox.graph_from_point((DEPOT_LAT, DEPOT_LON), dist=DISTANCE, network_type="drive", truncate_by_edge=True)





    # Get largest component (important for road connections)
    map_network = ox.utils_graph.get_largest_component(G, strongly=True)

    # Find the nearest node to the depot in the graph
    depot_node = ox.bb_distance.nearest_nodes(map_network, DEPOT_LON, DEPOT_LAT)

    # Select the glass client_csv_file as client locations
    client_subset = transformed_client_csv_file.values.tolist()[:num_clients]

    # Ensure that client locations have default values for all resources (water, food, etc.)
    for lat, lon in client_subset:
        nearest_node = ox.bb_distance.nearest_nodes(map_network, lon, lat)
        map_network.nodes[nearest_node]["demand"] = 0

        # Assign default values of 1 to each resource
        for i in range(len(RESOURCES)):
            map_network.nodes[nearest_node][f"resource_{i}"] = 1
            map_network.nodes[nearest_node]["demand"] += map_network.nodes[nearest_node][f"resource_{i}"]

    # Get min and max coordinates to determine map bounds
    coordinates = _get_coordinates(dict(enumerate(map_network.nodes(data=True))))
    map_bounds = [coordinates.min(0).tolist(), coordinates.max(0).tolist()]

    return map_network, depot_node, client_subset, map_bounds


def _get_node_info(
    G: nx.Graph, node_id: int, icon_name: str
) -> tuple[folium.CustomIcon, list[int]]:
    """Get node demand values and icons for each client location."""
    icon_path = Path(__file__).parent / f"assets/location_icons/{icon_name}.png"
    location_icon = folium.CustomIcon(str(icon_path), icon_size=(30, 48))
    return location_icon, [G.nodes[node_id][f"resource_{i}"] * 100 for i in range(len(RESOURCES))]


def show_locations_on_initial_map(
    G: nx.MultiDiGraph, depot_id: int, client_subset: list, map_bounds: list[list]
) -> folium.Map:
    """Prepare map to be rendered initially on app screen.

    Args:
        G: ``nx.MultiDiGraph`` to build map from.
        depot_id: Node ID of the depot location.
        client_subset: List of client latitude and longitude pairs.

    Returns:
        folium.Map: Map with depot, client locations, and tooltip popups.
    """
    # create folium map on which to plot depots
    tiles = "cartodb positron"  # folium map theme

    folium_map = ox.graph_to_gdfs(G, nodes=False, node_geometry=False).explore(
        style_kwds={"opacity": 0},  # Change opacity to 1 to see graph edges/roads in blue
        tiles=tiles,
    )

    folium_map.fit_bounds(map_bounds)

    # add marker to the depot location
    folium.Marker(
        location=(G.nodes[depot_id]["y"], G.nodes[depot_id]["x"]),
        tooltip=folium.map.Tooltip(text=DEPOT_LABEL, style="font-size: 1.4rem;"),
        icon=depot_icon,
    ).add_to(folium_map)

    # convert each client latitude/longitude to nearest graph node and add markers
    for lat, lon in client_subset:
        nearest_node = ox.distance.nearest_nodes(G, lon, lat)
        location_icon, nodes = _get_node_info(G, nearest_node, "location_orange")

        folium.Marker(
            location=(G.nodes[nearest_node]["y"], G.nodes[nearest_node]["x"]),
            tooltip=folium.map.Tooltip(
                text=" <br> ".join(
                    [f"{resource}: {nodes[index]}" for index, resource in enumerate(RESOURCES)]
                ),
                style="font-size: 1.4rem;",
            ),
            icon=location_icon,
        ).add_to(folium_map)

    # add fullscreen button to map
    plugins.Fullscreen().add_to(folium_map)
    return folium_map

def plot_solution_routes_on_map(
    folium_map: folium.Map,
    routing_parameters,
    routing_solver,
) -> folium.folium.Map:
    """Generate interactive folium map for drone routes given solution dictionary.

    Args:
        folium_map: Initial folium map to plot solution on.
        routing_parameters: Routing problem parameters.
        routing_solver: Solver class containing the solution (if run).

    Returns:
        `folium.folium.Map` object,  dictionary with solution cost information.

    """
    solution_cost_information = {}
    G = routing_parameters.map_network

    solution = routing_solver.solution
    cost = routing_solver.cost_between_nodes
    paths = routing_solver.paths_and_lengths

    # get colourblind palette from seaborn (10 colours) and expand if more vehicles
    palette = [
        ("location_blue", "#56b4e9"),
        ("location_yellow", "#ece133"),
        ("location_grey", "#949494"),
        ("location_pink", "#fbafe4"),
        ("location_beige", "#ca9161"),
        ("location_purple", "#cc78bc"),
        ("location_orange", "#d55e00"),
        ("location_green", "#029e73"),
        ("location_gold", "#de8f05"),
        ("location_navy", "#0173b2"),
    ] * (len(solution) // 10 + 1)

    locations = {}
    for index, route_network in solution.items():
        vehicle_id = index + 1
        icon_name, route_color = palette.pop()

        solution_cost_information[vehicle_id] = {
            "optimized_cost": 0,
            "serviced": len(route_network.nodes) - 1,
        }
        for i in range(len(RESOURCES)):
            solution_cost_information[vehicle_id][f"resource_{i}"] = 0

        for stop_number, node in enumerate(route_network.nodes):
            locations.update({node: (G.nodes[node]["y"], G.nodes[node]["x"])})

            if node != routing_parameters.depot_id:
                location_icon, nodes = _get_node_info(G, node, icon_name)

                folium.Marker(
                    locations[node],
                    tooltip=folium.map.Tooltip(
                        text=" <br> ".join(
                            [
                                f"{resource}: {nodes[i]}"
                                for i, resource in enumerate(RESOURCES)
                            ]
                        )
                        + f" <br> Vehicle ID: {vehicle_id} <br> Stop: #{stop_number} of {len(route_network.nodes)-1}",
                        style="font-size: 1.4rem;",
                    ),
                    icon=location_icon,
                ).add_to(folium_map)

                for i in range(len(RESOURCES)):
                    solution_cost_information[vehicle_id][f"resource_{i}"] += nodes[i]

        for start, end in route_network.edges:
            # Ensure that start and end nodes exist in the locations dictionary
            if start in locations and end in locations:
                solution_cost_information[vehicle_id]["optimized_cost"] += cost(
                    locations[start], locations[end], start, end
                )

                if routing_parameters.vehicle_type is VehicleType.TRUCKS:
                    route = paths[start][1][end]
                    folium_map = ox.graph_to_gdfs(G.subgraph(route), nodes=False).explore(
                        m=folium_map, color=route_color, style_kwds={"weight": 4}
                    )
                else:  # if vehicle_type is DELIVERY_DRONES
                    folium.PolyLine((locations[start], locations[end]), color=route_color).add_to(
                        folium_map
                    )
            else:
                print(f"Warning: Missing node in locations. Start: {start}, End: {end}")

    return folium_map, solution_cost_information

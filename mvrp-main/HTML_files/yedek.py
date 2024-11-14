
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


def generate_control_card() -> html.Div:
    """
    This function generates the control card for the dashboard, which
    contains the dropdowns for selecting the scenario, model, and solver.

    Returns:
        html.Div: A Div containing the dropdowns for selecting the scenario,
        model, and solver.
    """
    # calculate drop-down options
    vehicle_options = [
        {"label": label, "value": sampler_type.value}
        for sampler_type, label in VEHICLE_TYPES.items()
    ]
    sampler_options = [
        {"label": label, "value": sampler_type.value}
        for sampler_type, label in SAMPLER_TYPES.items()
    ]

    return html.Div(
        id="control-card",
        children=[
            # Settings Button
            html.Button(
                id="settings-button",
                children="Show Settings",
                n_clicks=0,
                style={
                    'margin-bottom': '10px',
                    'padding': '10px',
                    'background-color': THEME_COLOR,  # Use THEME_COLOR
                    'color': 'white',  # White text
                    'border': 'none',
                    'border-radius': '5px',
                    'cursor': 'pointer',
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'width': '100%',
                    'text-align': 'center',
                    'display': 'flex',
                    'align-items': 'center',  # Center vertically
                    'justify-content': 'center',  # Center horizontally
                    'height': '50px'  # Ensure consistent height
                },
            ),

            # Upload Section Button
            html.Button(
                id="upload-section-button",
                children="Show Upload Section",
                n_clicks=0,
                style={
                    'margin-bottom': '10px',
                    'padding': '10px',
                    'background-color': THEME_COLOR,  # Use THEME_COLOR
                    'color': 'white',  # White text
                    'border': 'none',
                    'border-radius': '5px',
                    'cursor': 'pointer',
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'width': '100%',
                    'text-align': 'center',
                    'display': 'flex',
                    'align-items': 'center',  # Center vertically
                    'justify-content': 'center',  # Center horizontally
                    'height': '50px'  # Ensure consistent height
                },
            ),

            # Hidden Div for Upload Section
            html.Div(
                id="upload-section",
                style={"display": "none"},  # Initially hidden
                children=[
                    html.Label("Upload Client Data (CSV):"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select a CSV File')
                        ]),
                        style={
                            'width': '100%',
                            'height': '50px',
                            'lineHeight': '50px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin-bottom': '15px'
                        },
                        multiple=False
                    ),
                    html.Label("Or select a CSV File from assets/CSVs:"),
                    dcc.Dropdown(
                        id='file-selector',
                        options=[
                            {'label': f, 'value': f} for f in
                            os.listdir(os.path.join(os.path.dirname(__file__), 'assets', 'CSVs')) if f.endswith('.csv')
                        ],
                        placeholder="Select a file...",
                        style={'margin-bottom': '15px'}
                    ),
                    html.Div(id='output-data-upload')  # Displays feedback for upload result or selected file
                ]
            ),


            # Hidden Div containing all controls
            html.Div(
                id="settings-section",
                style={"display": "none"},  # Initially hidden
                children=[
                    dropdown(
                        "Vehicle Type",
                        "vehicle-type-select",
                        sorted(vehicle_options, key=lambda op: op["value"]),
                    ),
                    slider(
                        "Vehicles to Deploy",
                        "num-vehicles-select",
                        NUM_VEHICLES,
                    ),
                    slider(
                        LOCATIONS_LABEL,
                        "num-clients-select",
                        NUM_CLIENT_LOCATIONS,
                    ),
                    dropdown(
                        "Solver",
                        "sampler-type-select",
                        sorted(sampler_options, key=lambda op: op["value"]),
                    ),
                    html.Label("Solver Time Limit (seconds)"),
                    dcc.Input(
                        id="solver-time-limit",
                        type="number",
                        **SOLVER_TIME,
                    ),
                    html.Div(
                        id="button-group",
                        children=[
                            html.Button(
                                id="run-button", children="Run Optimization", n_clicks=0, disabled=False
                            ),
                            html.Button(
                                id="cancel-button",
                                children="Cancel Optimization",
                                n_clicks=0,
                                className="display-none",
                            ),
                        ],
                    ),
                ]
            )
        ],
    )


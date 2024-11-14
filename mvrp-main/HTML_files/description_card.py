def description_card():
    """A Div containing dashboard title & descriptions."""
    return html.Div(
        id='description-card',
        children=[
            html.H1(MAIN_HEADER),
            html.P(DESCRIPTION)
        ]
    )

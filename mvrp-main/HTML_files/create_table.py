def create_table(values_dicts: dict[int, dict], values_totals: list) -> html.Table:
    """Create a table dynamically.

    Args:
        values_dicts: Dictionary with vehicle id keys and results data as values.
        values_totals: List of total results data (sum of individual vehicle data).
    """
    headers = ['Vehicle ID', COST_LABEL, LOCATIONS_LABEL, *RESOURCES]
    table = html.Table(className='results result-table', children=[html.Thead([html.Tr([html.Th(header) for header in headers])]), html.Tbody([html.Tr([html.Td(vehicle), *create_row_cells(list(results.values()))]) for vehicle, results in values_dicts.items()]), html.Tfoot([html.Tr([html.Td('Total'), *create_row_cells(values_totals)], className='total-cost-row')])])
    return table
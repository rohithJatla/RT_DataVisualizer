# app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Import pages
from pages import home, overview, graph, console, diagnostics

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='selected-db', storage_type='session'),
    dbc.Row([
        dbc.Col([
            html.H2("Dashboard Navigation"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Overview", href="/overview", active="exact"),
                    dbc.NavLink("Graph", href="/graph", active="exact"),
                    dbc.NavLink("Console", href="/console", active="exact"),
                    dbc.NavLink("Diagnostics", href="/diagnostics", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ], width=2),
        dbc.Col([
            html.Div(id='page-content')
        ], width=10)
    ])
], fluid=True)

@app.callback(
    dash.Output('page-content', 'children'),
    dash.Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return home.layout
    elif pathname == '/overview':
        return overview.layout
    elif pathname == '/graph':
        return graph.layout
    elif pathname == '/console':
        return console.layout
    elif pathname == '/diagnostics':
        return diagnostics.layout
    else:
        return html.H1("404 - Page not found")

# Register callbacks from each page
home.register_callbacks(app)
overview.register_callbacks(app)
graph.register_callbacks(app)
console.register_callbacks(app)
diagnostics.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)

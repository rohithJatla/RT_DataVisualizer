# pages/graph.py
import sqlite3
import pandas as pd
from dash import dcc, html, Input, Output, State

layout = html.Div([
    html.H3("Graph - Time Series Data"),
    dcc.Interval(id='graph-interval', interval=2000, n_intervals=0),
    dcc.Graph(id='time-series-graph')
])


def register_callbacks(app):
    @app.callback(
        Output('time-series-graph', 'figure'),
        Input('graph-interval', 'n_intervals'),
        State('selected-db', 'data')
    )
    def update_graph(n_intervals, selected_db):
        if not selected_db:
            return {}
        try:
            conn = sqlite3.connect(selected_db)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA cache_size=10000;")    
            df = pd.read_sql_query(
                "SELECT timestamp, cpu_percent, memory_percent FROM metrics", conn)
            conn.close()
            if df.empty:
                return {}
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = {
                'data': [
                    {
                        'x': df['timestamp'],
                        'y': df['cpu_percent'],
                        'type': 'line',
                        'name': 'CPU %'
                    },
                    {
                        'x': df['timestamp'],
                        'y': df['memory_percent'],
                        'type': 'line',
                        'name': 'Memory %'
                    }
                ],
                'layout': {
                    'title': 'CPU & Memory Over Time'
                }
            }
            return fig
        except Exception as e:
            return {}

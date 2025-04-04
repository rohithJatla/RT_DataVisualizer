# pages/diagnostics.py
import sqlite3
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Diagnostics"),
    dcc.Interval(id='diagnostics-interval', interval=2000, n_intervals=0),
    html.Div(id='diagnostics-content')
])


def register_callbacks(app):
    @app.callback(
        Output('diagnostics-content', 'children'),
        Input('diagnostics-interval', 'n_intervals'),
        State('selected-db', 'data')
    )
    def update_diagnostics(n_intervals, selected_db):
        if not selected_db:
            return "No database selected."
        try:
            conn = sqlite3.connect(selected_db)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA cache_size=10000;")
            cursor.execute(
                "SELECT cpu_percent FROM metrics ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            if row:
                cpu_percent = row[0]
                if cpu_percent > 90:
                    status = dbc.Alert(
                        "High CPU Usage Detected!", color="danger")
                else:
                    status = dbc.Alert("CPU Usage Normal.", color="success")
                return status
            else:
                return "No data available."
        except Exception as e:
            return f"Error: {str(e)}"

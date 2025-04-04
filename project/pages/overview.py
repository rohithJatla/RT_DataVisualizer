# pages/overview.py
import sqlite3
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Overview - Real-Time Metrics"),
    dcc.Interval(id='overview-interval', interval=2000, n_intervals=0),
    html.Div(id='overview-content')
])


def register_callbacks(app):
    @app.callback(
        Output('overview-content', 'children'),
        Input('overview-interval', 'n_intervals'),
        State('selected-db', 'data')
    )
    def update_overview(n_intervals, selected_db):
        if not selected_db:
            return "No database selected. Please go to Home and start a session."
        try:
            conn = sqlite3.connect(selected_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            if row:
                timestamp = row[1]
                cpu_percent = row[2]
                memory_percent = row[4]
                return html.Div([
                    html.P(f"Timestamp: {timestamp}"),
                    html.P(f"CPU Usage: {cpu_percent}%"),
                    html.P(f"Memory Usage: {memory_percent}%")
                ])
            else:
                return "No data available yet."
        except Exception as e:
            return f"Error retrieving data: {str(e)}"

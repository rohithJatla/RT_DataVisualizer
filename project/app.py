from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import sqlite3
from datetime import datetime
import json

# Initialize the Dash app
app = Dash(__name__)

# Database functions
def init_db():
    conn = sqlite3.connect('data_store.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data_logs
                 (timestamp TEXT, data TEXT, config TEXT)''')
    conn.commit()
    conn.close()

def log_data(data, config):
    conn = sqlite3.connect('data_store.db')
    c = conn.cursor()
    c.execute("INSERT INTO data_logs VALUES (?, ?, ?)",
              (datetime.now().isoformat(), json.dumps(data), json.dumps(config)))
    conn.commit()
    conn.close()

# Layout components
def create_landing_page():
    return html.Div([
        html.H1("Data Logger System", className="text-center mb-4"),
        dcc.Tabs([
            dcc.Tab(label='HOME', children=[
                html.Div([
                    html.H3("System Overview"),
                    html.P("Welcome to the Data Logger System"),
                ], className="p-4")
            ]),
            dcc.Tab(label='DATA VIEW', children=[
                html.Div([
                    html.H3("Data Visualization"),
                    dcc.Graph(id='data-graph'),
                    html.Button('Refresh Data', id='refresh-data', n_clicks=0)
                ], className="p-4")
            ]),
            dcc.Tab(label='SETTINGS', children=[
                html.Div([
                    html.H3("Configuration Settings"),
                    html.Div([
                        html.Label("Logging Interval (seconds)"),
                        dcc.Input(id='logging-interval', type='number', value=60),
                        html.Button('Save Settings', id='save-settings', n_clicks=0)
                    ])
                ], className="p-4")
            ]),
            dcc.Tab(label='CONFIG', children=[
                html.Div([
                    html.H3("System Configuration"),
                    dcc.Dropdown(
                        id='config-selection',
                        options=[
                            {'label': 'CAN Bus', 'value': 'can'},
                            {'label': 'UART', 'value': 'uart'}
                        ],
                        value='can'
                    )
                ], className="p-4")
            ]),
            dcc.Tab(label='DIAGNOSTIC', children=[
                html.Div([
                    html.H3("System Diagnostics"),
                    html.Div(id='system-status'),
                    dcc.Interval(id='diagnostic-interval', interval=5000)
                ], className="p-4")
            ])
        ]),
        # Data Logger Status
        html.Div([
            html.H4("Data Logger Status"),
            html.Div(id='logger-status'),
            dcc.Interval(id='status-interval', interval=1000)
        ], className="mt-4 p-4 border")
    ])

# Main layout
app.layout = create_landing_page()

# Callbacks
@callback(
    Output('data-graph', 'figure'),
    Input('refresh-data', 'n_clicks')
)
def update_graph(n_clicks):
    # Sample data for demonstration
    df = pd.DataFrame({
        'Time': pd.date_range(start='2024-01-01', periods=10, freq='H'),
        'Value': range(10)
    })
    return px.line(df, x='Time', y='Value', title='Data Log Visualization')

@callback(
    Output('logger-status', 'children'),
    Input('status-interval', 'n_intervals')
)
def update_logger_status(n_intervals):
    return html.Div([
        html.P(f"Logger Active: Yes"),
        html.P(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ])

@callback(
    Output('system-status', 'children'),
    Input('diagnostic-interval', 'n_intervals')
)
def update_diagnostics(n_intervals):
    return html.Div([
        html.P("System Status: Operational"),
        html.P("Memory Usage: 45%"),
        html.P("CPU Load: 30%")
    ])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
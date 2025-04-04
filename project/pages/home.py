# pages/home.py
import os
import datetime
import sqlite3
import threading

from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import data_logger  # Import the data logger module

# Global variable to hold the logger thread reference
logger_thread = None

layout = dbc.Card([
    dbc.CardBody([
        html.H3("Home - Select a Database or Start Live Monitoring"),
        html.Label("Select Existing Database:"),
        dcc.Dropdown(
            id='db-dropdown', 
            options=[{'label': db, 'value': db} for db in os.listdir('.') if db.endswith('.db')],
            placeholder="Select a database for Replay Mode"
        ),
        html.Br(),
        dbc.Button("Start", id='start-btn', color="primary", n_clicks=0),
        html.Div(id='start-output', style={'marginTop': '20px'})
    ])
], style={'marginTop': '20px'})

def register_callbacks(app):
    @app.callback(
        [Output('start-output', 'children'),
         Output('selected-db', 'data')],
        [Input('start-btn', 'n_clicks')],
        [State('db-dropdown', 'value')]
    )
    def start_button(n_clicks, selected_value):
        global logger_thread  # Use the global variable to track our thread
        if n_clicks > 0:
            if selected_value:
                # Replay Mode: use the selected database (do not start data logger)
                return f"Replay Mode: Using database {selected_value}", selected_value
            else:
                # Live Mode: Create a new database
                new_db = f"perf_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                # Create the new DB file and table structure
                conn = sqlite3.connect(new_db)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        cpu_percent REAL,
                        cpu_per_core TEXT,
                        memory_percent REAL,
                        disk_io_read REAL,
                        disk_io_write REAL,
                        network_bytes_sent REAL,
                        network_bytes_recv REAL,
                        temperature REAL,
                        process_count INTEGER,
                        battery_status TEXT
                    )
                """)
                conn.commit()
                conn.close()
                # Start the data logger thread if not already running
                if logger_thread is None or not logger_thread.is_alive():
                    logger_thread = threading.Thread(
                        target=data_logger.run_logger, 
                        args=(new_db,),  # Pass the new database name to the logger
                        daemon=True
                    )
                    logger_thread.start()
                    print("Data logger thread started.")
                return f"Live Mode: New database created ({new_db}) and data logger started.", new_db
        return "", None

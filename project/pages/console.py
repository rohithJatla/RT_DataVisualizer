# pages/console.py
import sqlite3
import pandas as pd
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_table

layout = html.Div([
    html.H3("Console - Data Table"),
    dcc.Interval(id='console-interval', interval=2000, n_intervals=0),
    html.Div(id='console-table')
])


def register_callbacks(app):
    @app.callback(
        Output('console-table', 'children'),
        Input('console-interval', 'n_intervals'),
        State('selected-db', 'data')
    )
    def update_console(n_intervals, selected_db):
        if not selected_db:
            return "No database selected."
        try:
            conn = sqlite3.connect(selected_db)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA cache_size=10000;")    
            df = pd.read_sql_query(
                "SELECT * FROM metrics ORDER BY id DESC LIMIT 100", conn)
            conn.close()
            if df.empty:
                return "No data available."
            table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,
                filter_action="native",
                sort_action="native"
            )
            return table
        except Exception as e:
            return f"Error: {str(e)}"

# data_logger.py
import psutil
import time
import datetime
import sqlite3
import json

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    # Enable WAL mode for better concurrency (optional)
    conn.execute("PRAGMA journal_mode=WAL;")
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
    return conn

def log_metrics(conn, interval=1):
    cursor = conn.cursor()
    while True:
        now = datetime.datetime.now()
        timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

        # Gather metrics
        cpu_percent = psutil.cpu_percent(interval=None) * 10
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent * 10
        
        disk_io = psutil.disk_io_counters()
        disk_io_read = disk_io.read_bytes
        disk_io_write = disk_io.write_bytes
        
        net_io = psutil.net_io_counters()
        network_bytes_sent = net_io.bytes_sent
        network_bytes_recv = net_io.bytes_recv
        
        temperature = None
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                sensor_key = list(temps.keys())[0]
                temperature = temps[sensor_key][0].current
        
        process_count = len(psutil.pids())
        
        battery_status = None
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                battery_status = f"{battery.percent}% {'Charging' if battery.power_plugged else 'Not Charging'}"
        
        cursor.execute("""
            INSERT INTO metrics (
                timestamp, cpu_percent, cpu_per_core, memory_percent, disk_io_read,
                disk_io_write, network_bytes_sent, network_bytes_recv, temperature,
                process_count, battery_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp_str,
            cpu_percent,
            json.dumps(cpu_per_core),
            memory_percent,
            disk_io_read,
            disk_io_write,
            network_bytes_sent,
            network_bytes_recv,
            temperature,
            process_count,
            battery_status
        ))
        conn.commit()
        print(f"Logged metrics at {timestamp_str}")
        time.sleep(interval)

def run_logger(db_name=None):
    # If no db_name provided, create one automatically
    if db_name is None:
        db_name = f"perf_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    print(f"Starting data logger with database: {db_name}")
    conn = create_database(db_name)
    log_metrics(conn, interval=1)

# When run directly, allow auto-start (but for our use case we won't call this directly)
if __name__ == "__main__":
    run_logger()

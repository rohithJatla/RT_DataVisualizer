import sqlite3
import pandas as pd

# Create database and sample data
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Create sales table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date DATE NOT NULL
)
''')

# Insert sample data
sample_data = [
    ('Laptop', 'Electronics', 1200, '2023-01-01'),
    ('Phone', 'Electronics', 800, '2023-01-02'),
    ('Desk', 'Furniture', 350, '2023-01-03'),
    ('Chair', 'Furniture', 150, '2023-01-04'),
    ('Tablet', 'Electronics', 500, '2023-02-01'),
    ('Sofa', 'Furniture', 900, '2023-02-02'),
    ('Monitor', 'Electronics', 400, '2023-02-03'),
    ('Bookshelf', 'Furniture', 250, '2023-02-04')
]

cursor.executemany('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()
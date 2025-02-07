import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('waste_management.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bin_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bin_id INTEGER,
                fill_level REAL,
                temperature REAL,
                humidity REAL,
                location_lat REAL,
                location_long REAL,
                waste_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_bin_data(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bin_data (
                bin_id, fill_level, temperature, humidity,
                location_lat, location_long, waste_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['bin_id'], data['fill_level'], data['temperature'],
            data['humidity'], data['location_lat'], data['location_long'],
            data['waste_type']
        ))
        self.conn.commit()

    def get_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as total_records,
                AVG(fill_level) as avg_fill_level,
                COUNT(DISTINCT bin_id) as total_bins
            FROM bin_data
        ''')
        return dict(zip(['total_records', 'avg_fill_level', 'total_bins'], 
                       cursor.fetchone()))
    def get_bin_data(self, bin_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bin_data WHERE bin_id = ?', (bin_id,))
        return cursor.fetchall()

    def get_all_bins(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT bin_id FROM bin_data')
        return [row[0] for row in cursor.fetchall()]

    def get_waste_distribution(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT waste_type, COUNT(*) as count 
            FROM bin_data 
            GROUP BY waste_type
        ''')
        return dict(cursor.fetchall())
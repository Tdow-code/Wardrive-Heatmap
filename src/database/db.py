import sqlite3

def connect_db(db_name='/home/ian/wardriving_data/master_wardriving.db'):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wifi_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ssid TEXT NOT NULL,
            signal_strength INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.commit()

def log_wifi_scan(conn, timestamp, ssid, signal_strength, latitude, longitude):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wifi_scans (timestamp, ssid, signal_strength, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, ssid, signal_strength, latitude, longitude))
    conn.commit()

def fetch_wifi_scans(conn, limit=5000):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wifi_scans LIMIT ?', (limit,))
    return cursor.fetchall()

def fetch_kismet_scans(conn, limit=10000):
    """Fetch scans from Kismet wardriving table"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT CurrentLatitude, CurrentLongitude, RSSI, SSID, Channel
        FROM "Kismet-20260201-02-23-24-1"
        WHERE CurrentLatitude IS NOT NULL 
        AND CurrentLongitude IS NOT NULL
        AND RSSI IS NOT NULL
        LIMIT ?
    ''', (limit,))
    return cursor.fetchall()

def close_db(conn):
    conn.close()
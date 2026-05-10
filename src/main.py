import sqlite3
from src.database.db import create_connection
from src.models.wifi_scan import WifiScan
from src.visualization.heatmap_generator import generate_heatmap

def main():
    # Connect to the SQLite database
    conn = create_connection('/home/ian/wardriving_data/master_wardriving.db')

    # Example of logging a Wi-Fi scan (this would be replaced with actual scan data)
    example_scan = WifiScan(timestamp='2023-10-01 12:00:00', ssid='ExampleSSID', signal_strength=-70, latitude=37.7749, longitude=-122.4194)
    
    # Log the scan data to the database
    log_wifi_scan(conn, example_scan)

    # Generate heatmap from logged data
    generate_heatmap(conn)

    # Close the database connection
    conn.close()

def log_wifi_scan(conn, wifi_scan):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wifi_scans (timestamp, ssid, signal_strength, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (wifi_scan.timestamp, wifi_scan.ssid, wifi_scan.signal_strength, wifi_scan.latitude, wifi_scan.longitude))
    conn.commit()

if __name__ == '__main__':
    main()
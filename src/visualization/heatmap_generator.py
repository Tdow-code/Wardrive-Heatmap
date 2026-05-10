import sqlite3
import folium
from folium.plugins import HeatMap

def fetch_data_from_db(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT latitude, longitude, signal_strength FROM wifi_scans")
    data = cursor.fetchall()
    connection.close()
    return data

def generate_heatmap(data, output_file):
    heatmap_data = [[entry[0], entry[1], entry[2]] for entry in data]
    map_center = [sum(entry[0] for entry in heatmap_data) / len(heatmap_data),
                  sum(entry[1] for entry in heatmap_data) / len(heatmap_data)]
    
    heatmap = folium.Map(location=map_center, zoom_start=13)
    HeatMap(heatmap_data).add_to(heatmap)
    
    heatmap.save(output_file)

def main(db_path, output_file):
    data = fetch_data_from_db(db_path)
    generate_heatmap(data, output_file)
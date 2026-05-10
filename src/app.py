from flask import Flask, render_template, jsonify, request
import sqlite3
import hashlib

app = Flask(__name__, template_folder='../templates', static_folder='../static')
DB_PATH = '/home/ian/wardriving_data/master_wardriving.db'
data_hash = None

@app.route('/')
def index():
    """Serve the heatmap HTML page"""
    return render_template('index.html')

@app.route('/api/wifi-scans')
def get_wifi_scans():
    """Fetch WiFi scans from Kismet database with filtering"""
    
    min_signal = request.args.get('min_signal', default=-100, type=int)
    ssid_filter = request.args.get('ssid', default='', type=str).lower()
    limit = request.args.get('limit', default=5000, type=int)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Detect a Kismet-like table. Prefer any table name containing 'kismet',
    # otherwise fall back to 'packets' which contains lat/lon/signal in many
    # Kismet DB exports.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cursor.fetchall()]

    def find_kismet_table():
        for t in tables:
            if 'kismet' in t.lower():
                # ensure it has expected columns
                cursor.execute(f"PRAGMA table_info('{t}')")
                cols = [c[1].lower() for c in cursor.fetchall()]
                if 'currentlatitude' in cols or 'latitude' in cols or 'lat' in cols:
                    return t
        if 'packets' in tables:
            cursor.execute("PRAGMA table_info('packets')")
            cols = [c[1].lower() for c in cursor.fetchall()]
            if 'lat' in cols and 'lon' in cols and 'signal' in cols:
                return 'packets'
        return None

    src_table = find_kismet_table()
    scans = []
    if not src_table:
        conn.close()
        return jsonify(scans)

    if src_table == 'packets':
        # packets has lat, lon, signal but not SSID; return what we can
        cursor.execute('''
            SELECT lat, lon, signal
            FROM packets
            WHERE lat IS NOT NULL AND lon IS NOT NULL
            AND signal IS NOT NULL AND signal >= ?
            LIMIT ?
        ''', (min_signal, limit))

        for row in cursor.fetchall():
            scans.append({
                'latitude': row[0],
                'longitude': row[1],
                'signal_strength': row[2],
                'ssid': 'Unknown',
                'channel': 0
            })
    else:
        # Generic Kismet-like table: attempt to query expected columns
        q = f'''
            SELECT CurrentLatitude as latitude, CurrentLongitude as longitude, RSSI as signal_strength, SSID as ssid, Channel as channel
            FROM "{src_table}"
            WHERE CurrentLatitude IS NOT NULL AND CurrentLongitude IS NOT NULL
            AND RSSI IS NOT NULL AND RSSI >= ?
            LIMIT ?
        '''
        try:
            cursor.execute(q, (min_signal, limit))
            for row in cursor.fetchall():
                ssid = row[3] or 'Hidden'
                if ssid_filter and ssid_filter not in ssid.lower():
                    continue
                scans.append({
                    'latitude': row[0],
                    'longitude': row[1],
                    'signal_strength': row[2],
                    'ssid': ssid,
                    'channel': row[4] or 0
                })
        except sqlite3.OperationalError:
            # If the table doesn't match the expected schema, return empty
            pass

    conn.close()
    return jsonify(scans)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Initialize database on startup
    conn = connect_db('/home/ian/wardriving_data/master_wardriving.db')
    create_table(conn)
    conn.close()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

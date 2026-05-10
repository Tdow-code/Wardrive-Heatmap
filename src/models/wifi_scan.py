class WifiScan:
    def __init__(self, timestamp, ssid, signal_strength, latitude, longitude):
        self.timestamp = timestamp
        self.ssid = ssid
        self.signal_strength = signal_strength
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"WifiScan(timestamp={self.timestamp}, ssid={self.ssid}, signal_strength={self.signal_strength}, latitude={self.latitude}, longitude={self.longitude})"
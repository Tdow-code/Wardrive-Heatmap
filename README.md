# Wardriving Heatmap Application

This project is a heatmap application designed to log and visualize wardriving data using a SQLite database. The application captures Wi-Fi scan data, including SSID, signal strength, and GPS coordinates, and generates heatmaps based on this data.

## Project Structure

```
wardriving-heatmap
├── src
│   ├── main.py                # Entry point of the application
│   ├── database
│   │   ├── __init__.py        # Database package initializer
│   │   └── db.py              # Database connection and management
│   ├── models
│   │   ├── __init__.py        # Models package initializer
│   │   └── wifi_scan.py       # Wi-Fi scan data model
│   ├── utils
│   │   ├── __init__.py        # Utils package initializer
│   │   └── gps_parser.py      # GPS data parsing utilities
│   └── visualization
│       ├── __init__.py        # Visualization package initializer
│       └── heatmap_generator.py # Heatmap generation functions
├── data
│   └── wardriving.db          # SQLite database for storing wardriving data
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd wardriving-heatmap
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Database Initialization**:
   The application will automatically create the SQLite database (`wardriving.db`) and necessary tables upon first run.

## Usage

To start the application, run the following command:
```
python src/main.py
```

The application will log Wi-Fi scan data and generate heatmaps based on the collected data.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
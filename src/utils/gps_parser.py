def parse_gps_data(gps_string):
    """
    Parses a GPS string in the format "latitude,longitude" and returns a tuple of floats.
    
    Args:
        gps_string (str): A string containing latitude and longitude separated by a comma.
        
    Returns:
        tuple: A tuple containing the latitude and longitude as floats.
        
    Raises:
        ValueError: If the input string is not in the correct format.
    """
    try:
        latitude, longitude = map(float, gps_string.split(','))
        return latitude, longitude
    except ValueError:
        raise ValueError("Invalid GPS format. Expected 'latitude,longitude'.")

def format_gps_coordinates(latitude, longitude):
    """
    Formats GPS coordinates into a string representation.
    
    Args:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.
        
    Returns:
        str: A formatted string of the GPS coordinates.
    """
    return f"{latitude:.6f},{longitude:.6f}"
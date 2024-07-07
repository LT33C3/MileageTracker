import googlemaps
from config import GoogleMapsConfig

class LocationService:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=GoogleMapsConfig.API_KEY)

    def get_current_location(self):
        # For demonstration purposes, return a fixed location
        # In a real app, you'd use the device's GPS
        return "51.5074,-0.1278"  # London coordinates

    def calculate_distance(self, start_location, end_location):
        try:
            directions = self.gmaps.directions(start_location, end_location)
            distance = directions[0]['legs'][0]['distance']['value'] / 1000  # Convert to km
            return round(distance, 2)
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return 0
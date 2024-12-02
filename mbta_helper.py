import json
import math
import os
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Base URLs for API requests
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com"

# MBTA route types
ROUTE_TYPES = {
    "subway": 0,    # Red Line, Blue Line, etc.
    "tram": 0,      # Green Line, Mattapan Line
    "rail": 2,      # Commuter Rail
    "bus": 3,       # Bus
    "ferry": 4      # Ferry
}


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points using the Haversine formula.
    
    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point
        
    Returns:
        float: Distance in miles
    """
    R = 3959.87433  # Earth's radius in miles

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def get_json(url: str) -> Dict:
    """
    Get JSON response from a URL.

    Args:
        url: The URL to request data from

    Returns:
        dict: Decoded JSON response
    """
    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode('utf-8')
        return json.loads(response_text)


def get_lat_lng(place_name: str) -> Tuple[str, str]:
    """
    Get latitude and longitude for a place name using Mapbox API.

    Args:
        place_name: Name or address of a place

    Returns:
        tuple: (latitude, longitude) strings
    """
    # URL encode the place name and construct the API URL
    encoded_place = urllib.parse.quote(place_name)
    url = (f"{MAPBOX_BASE_URL}/{encoded_place}.json?"
           f"access_token={MAPBOX_TOKEN}&types=poi,address")
    
    # Get the response and extract coordinates
    response_data = get_json(url)
    
    # Get the first feature's coordinates (longitude, latitude)
    coordinates = response_data["features"][0]["geometry"]["coordinates"]
    
    # Mapbox returns coordinates as [longitude, latitude]
    # Return as (latitude, longitude) with 6 decimal precision
    return (f"{coordinates[1]:.6f}", f"{coordinates[0]:.6f}")


def get_nearest_stations(latitude: str, longitude: str) -> Dict[str, Dict]:
    """
    Find the nearest subway station and bus stop to given coordinates.

    Args:
        latitude: Latitude string
        longitude: Longitude string

    Returns:
        dict: Dictionary containing nearest subway and bus stop information
    """
    # Get subway stations (route_type=0,1 for subway/light rail)
    subway_url = (f"{MBTA_BASE_URL}/stops?"
                 f"api_key={MBTA_API_KEY}"
                 f"&filter[latitude]={latitude}"
                 f"&filter[longitude]={longitude}"
                 f"&filter[route_type]=0,1"
                 f"&sort=distance"
                 f"&page[limit]=1")
    
    # Get bus stops (route_type=3)
    bus_url = (f"{MBTA_BASE_URL}/stops?"
               f"api_key={MBTA_API_KEY}"
               f"&filter[latitude]={latitude}"
               f"&filter[longitude]={longitude}"
               f"&filter[route_type]=3"
               f"&sort=distance"
               f"&page[limit]=1")
    
    result = {"subway": None, "bus": None}
    
    # Get nearest subway station
    try:
        subway_data = get_json(subway_url)
        if subway_data["data"]:
            stop = subway_data["data"][0]
            station_lat = float(stop["attributes"]["latitude"])
            station_lon = float(stop["attributes"]["longitude"])
            distance = calculate_distance(
                float(latitude),
                float(longitude),
                station_lat,
                station_lon
            )
            
            result["subway"] = {
                "name": stop["attributes"]["name"],
                "wheelchair_accessible": stop["attributes"]["wheelchair_boarding"] == 1,
                "distance": f"{distance:.2f} miles",
                "id": stop["id"]
            }
    except Exception as e:
        print(f"Error getting subway data: {e}")
    
    # Get nearest bus stop
    try:
        bus_data = get_json(bus_url)
        if bus_data["data"]:
            stop = bus_data["data"][0]
            station_lat = float(stop["attributes"]["latitude"])
            station_lon = float(stop["attributes"]["longitude"])
            distance = calculate_distance(
                float(latitude),
                float(longitude),
                station_lat,
                station_lon
            )
            
            result["bus"] = {
                "name": stop["attributes"]["name"],
                "wheelchair_accessible": stop["attributes"]["wheelchair_boarding"] == 1,
                "distance": f"{distance:.2f} miles",
                "id": stop["id"]
            }
    except Exception as e:
        print(f"Error getting bus data: {e}")
    
    return result


def get_arrival_predictions(station_id: str, limit: int = 5) -> List[Dict]:
    """
    Get real-time arrival predictions for a station.

    Args:
        station_id: The MBTA station ID
        limit: Maximum number of predictions to return

    Returns:
        list: List of arrival predictions
    """
    url = (f"{MBTA_BASE_URL}/predictions?"
           f"api_key={MBTA_API_KEY}"
           f"&filter[stop]={station_id}"
           f"&include=trip,route"
           f"&sort=arrival_time"
           f"&page[limit]={limit}")
    
    response_data = get_json(url)
    
    predictions = []
    for pred in response_data["data"]:
        arrival_time = pred["attributes"].get("arrival_time")
        if arrival_time:
            arrival_dt = datetime.fromisoformat(arrival_time.replace("Z", "+00:00"))
            # Get status or default to "On Time" if None
            status = pred["attributes"].get("status")
            status = status if status else "On Time"
            
            predictions.append({
                "route": pred["relationships"]["route"]["data"]["id"],
                "arrival_time": arrival_dt.strftime("%I:%M %p"),
                "status": status
            })
    
    return predictions


def get_weather(lat: str, lng: str) -> Dict:
    """
    Get current weather for a location using OpenWeather API.
    
    Args:
        lat: Latitude string
        lng: Longitude string
        
    Returns:
        dict: Weather information
    """
    url = (f"{OPENWEATHER_BASE_URL}?"
           f"lat={lat}&lon={lng}"
           f"&appid={OPENWEATHER_API_KEY}"
           f"&units=imperial")  # Use Fahrenheit for temperature
    
    try:
        response_data = get_json(url)
        
        weather_data = {
            "temperature": round(response_data["main"]["temp"]),
            "feels_like": round(response_data["main"]["feels_like"]),
            "description": response_data["weather"][0]["description"].capitalize(),
            "humidity": response_data["main"]["humidity"],
            "wind_speed": round(response_data["wind"]["speed"]),
            "icon": response_data["weather"][0]["icon"]
        }
        
        return weather_data
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return None


def find_stop_near(place_name: str) -> Dict[str, Dict]:
    """
    Find the nearest subway station and bus stop to a given place name.

    Args:
        place_name: Name or address of a place

    Returns:
        dict: Dictionary containing nearest subway and bus stop information
        with their upcoming arrivals and weather
    """
    # Get coordinates for the place
    lat, lng = get_lat_lng(place_name)
    
    # Get nearest stations
    stations = get_nearest_stations(lat, lng)
    
    # Get arrival predictions for each station
    for mode, station in stations.items():
        if station:
            station["arrivals"] = get_arrival_predictions(station["id"])
    
    # Add weather information
    stations["weather"] = get_weather(lat, lng)
    
    return stations


def main():
    """Test the MBTA helper functions with a single location."""
    try:
        location = "Fenway Park"
        print(f"\nFinding nearest transit stops to {location}:")
        
        results = find_stop_near(location)
        
        # Show subway results
        if results["subway"]:
            print("\nNearest Subway (T) station:")
            print(f"Name: {results['subway']['name']}")
            print(f"Distance: {results['subway']['distance']}")
            print(f"Wheelchair accessible: {results['subway']['wheelchair_accessible']}")
            
            if results["subway"]["arrivals"]:
                print("Upcoming arrivals:")
                for arrival in results["subway"]["arrivals"]:
                    print(f"  {arrival['route']}: {arrival['arrival_time']}")
            else:
                print("No upcoming arrivals")
        else:
            print("No subway stations found nearby")
        
        # Show bus results
        if results["bus"]:
            print("\nNearest Bus Stop:")
            print(f"Name: {results['bus']['name']}")
            print(f"Distance: {results['bus']['distance']}")
            print(f"Wheelchair accessible: {results['bus']['wheelchair_accessible']}")
            
            if results["bus"]["arrivals"]:
                print("Upcoming arrivals:")
                for arrival in results["bus"]["arrivals"]:
                    print(f"  {arrival['route']}: {arrival['arrival_time']}")
            else:
                print("No upcoming arrivals")
        else:
            print("No bus stops found nearby")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

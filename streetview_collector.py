from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
import pandas as pd
import requests
import os
import time
import ast
import math


# load_dotenv()

# print(os.getenv('API_KEY'))

# Configuration
API_KEY: str = "" # @todo: This needs to be pasted manually, I have no idea why it doesnt work yet.

API_PARAMS: Dict[str, Any] = {
    "size"              : "640x640", # size of the image
    "pitch"             : -10, # camera tilted downwards
    "fov"               : 45, # field of view
    "return_error_code" : "true" # Do not return grey images in case of errors. Not Python True since we are passing to API
}

# Folder structure and file names
INPUT_CSV: str = "routes.csv"
OUTPUT_BASE_DIR: str = "data/street_view_images"
OUTPUT_LOG_CSV: str = "downloaded_images_log.csv"


# Core functions

def get_bearing(start_coord: tuple, end_coord: tuple) -> float:
    """
    Calculates the compass bearing (angle) between two coordinates in degrees.
    Determines the forward direction of the route.

    :param start_coord: (latitude, longitude) for the starting point
    :param end_coord: (latitude, longitude) for the ending point
    :return: The bearing in degrees (0-360), where 0 is North.
    """
    lat1 = math.radians(start_coord[0])
    lon1 = math.radians(start_coord[1])
    lat2 = math.radians(end_coord[0])
    lon2 = math.radians(end_coord[1])

    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    # Corrected: Arguments are swapped to (x, y)
    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def download_image(url: str, filepath: str) -> bool:
    """
    Download an image from a URL.
    :param url:
    :param filepath:
    :return:
    """

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)

        return True

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return False

def process_route(route_data: pd.Series) -> List[Dict[str, Any]]:
    """
    Processes a single route, downloads images, and returns a log of the download status.
    Calculates the heading for each segment to get a precise 'forward' view.
    """
    road_name = route_data['road_name']
    start_intersection = route_data['start_intersection']
    end_intersection = route_data['end_intersection']

    try:
        coordinates = ast.literal_eval(route_data['coordinates'])
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing coordinates for {road_name}: {e}")
        return []

    if len(coordinates) < 2:
        print(f"Skipping route '{road_name}': Requires at least two coordinates.")
        return []

    # Corrected: Define the route folder here
    route_folder = os.path.join(OUTPUT_BASE_DIR, f"{road_name}_{start_intersection}_{end_intersection}")
    if not os.path.exists(route_folder):
        os.makedirs(route_folder)

    log_data: List[Dict[str, Any]] = []

    print(f"\nProcessing route: '{road_name}'")

    # Loop through all coordinates except the very last one
    for i in range(len(coordinates) - 1):
        start_coord = coordinates[i]
        end_coord = coordinates[i+1]

        # Calculate the precise heading for this specific segment of the road
        segment_heading = get_bearing(start_coord, end_coord)

        lat, lon = start_coord

        # Create the full API URL
        params_str = '&'.join([f"{k}={v}" for k, v in API_PARAMS.items()])
        url = (
            f"https://maps.googleapis.com/maps/api/streetview?"
            f"location={lat},{lon}&heading={segment_heading}&key={API_KEY}&{params_str}"
        )

        filename = f"{road_name}_{start_intersection}_{end_intersection}_{i}_{segment_heading:.2f}.jpg"
        filepath = os.path.join(route_folder, filename)

        if download_image(url, filepath):
            status = 'success'
            print(f"  - Downloaded {filename}")
        else:
            status = 'failed'
            print(f"  - Failed to download {filename}")

        log_data.append({
            'image_path': filepath if status == 'success' else '',
            'road_name': road_name,
            'start_intersection': start_intersection,
            'end_intersection': end_intersection,
            'latitude': lat,
            'longitude': lon,
            'heading': segment_heading,
            'status': status
        })
        time.sleep(0.2)

    return log_data

def main():
    """

    :return:
    """
    if not os.path.exists(OUTPUT_BASE_DIR):
        os.makedirs(OUTPUT_BASE_DIR)

    try:
        df_routes = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: The input file '{INPUT_CSV}' was not found.")
        return

    all_log_data: List[Dict[str, Any]] = []

    for _, row in df_routes.iterrows():
        route_log = process_route(row)
        all_log_data.extend(route_log)

    df_log = pd.DataFrame(all_log_data)
    log_path = os.path.join(OUTPUT_BASE_DIR, OUTPUT_LOG_CSV)
    df_log.to_csv(log_path, index=False)

    print(f"\nAll downloads complete. Log saved to '{log_path}'.")

if __name__ == "__main__":
    main()


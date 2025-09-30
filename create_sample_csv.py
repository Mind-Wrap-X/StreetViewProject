import pandas as pd
import os
from typing import Dict, Any


def create_sample_csv(filename: str = 'routes.csv') -> None:
    """
    Creates a sample CSV file with example route data for the Street View collector.

    Args:
        filename (str): The name of the CSV file to create.
    """
    sample_data: Dict[str, Any] = {
        'road_name': [
            'California Ave',
            'El Camino Real',
            'Foothill Blvd'
        ],
        'start_intersection': [
            'Sunnyvale Ave',
            'El Monte Ave',
            'Stevens Creek Blvd'
        ],
        'end_intersection': [
            'Fair Oaks Ave',
            'San Antonio Rd',
            'I-280'
        ],
        'coordinates': [
            "[(37.381191, -122.027311), (37.381200, -122.026809), (37.381191, -122.026467), (37.381139, -122.026296), (37.381111, -122.026125), (37.381074, -122.025936), (37.381022, -122.025718), (37.380999, -122.025494), (37.380952, -122.025305), (37.380881, -122.025004), (37.380816, -122.024579), (37.380732, -122.024292), (37.380584, -122.023474), (37.380456, -122.022905), (37.380328, -122.022347), (37.380251, -122.021993), (37.380123, -122.021381), (37.379996, -122.020813), (37.379927, -122.020384), (37.379808, -122.019955), (37.379808, -122.019955), (37.379638, -122.019150)]",
            "[(37.388836, -122.071745), (37.388555, -122.072225), (37.388274, -122.072705)]",
            "[(37.357591, -122.074382), (37.357301, -122.073998), (37.356956, -122.073491)]"
        ]
    }

    # Create a pandas DataFrame from the sample data
    df = pd.DataFrame(sample_data)

    # Save the DataFrame to a CSV file.
    # index=False prevents pandas from writing the DataFrame index to the CSV.
    try:
        df.to_csv(filename, index=False)
        print(f"Successfully created sample CSV file: '{filename}'")
    except Exception as e:
        print(f"An error occurred while creating the CSV file: {e}")


if __name__ == "__main__":
    create_sample_csv()
import xml.etree.ElementTree as ET


def extract_coordinates_from_kml(kml_filepath):
    """
    Parses a KML file and extracts coordinates from the <coordinates> tag.

    Args:
        kml_filepath (str): The path to the doc.kml file.

    Returns:
        A list of tuples with (latitude, longitude) coordinates.
    """
    try:
        # Use a list to store coordinates as (latitude, longitude) tuples
        coordinates = []

        # Parse the KML file (which is an XML file)
        tree = ET.parse(kml_filepath)
        root = tree.getroot()

        # KML files use a namespace, so we need to find it
        # The common namespace is 'http://www.opengis.net/kml/2.2'
        namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

        # Find all <coordinates> tags in the file
        coord_elements = root.findall('.//kml:coordinates', namespace)

        if not coord_elements:
            print("No <coordinates> tag found in the KML file.")
            return []

        # Process each <coordinates> block
        for elem in coord_elements:
            # The coordinates are a single string of "longitude,latitude,altitude" separated by spaces
            coord_str = elem.text.strip()

            # Split the string by spaces to get individual points
            points = coord_str.split(' ')

            for point in points:
                if point:
                    # Split each point by commas to get longitude, latitude, and altitude
                    lon, lat, _ = point.split(',')
                    coordinates.append((float(lat), float(lon)))

        return coordinates

    except FileNotFoundError:
        print(f"Error: The file '{kml_filepath}' was not found.")
        return []
    except ET.ParseError as e:
        print(f"Error parsing KML file: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def format_coordinates_to_string(coord_list):
    """
    Converts a list of coordinate tuples to a single string
    in the format: '[(lat, lon), (lat, lon), ...]'
    """
    # Convert each tuple to its string representation
    # e.g., (12.34, -56.78) becomes '(12.34, -56.78)'
    tuple_strings = [str(coord) for coord in coord_list]

    # Join all the strings with a comma and a space, and add brackets
    formatted_string = '[' + ', '.join(tuple_strings) + ']'

    return formatted_string

# --- Example Usage ---
if __name__ == "__main__":
    # Make sure to replace 'doc.kml' with the actual path to your unzipped KML file
    file_path = 'data/Mexico.kml'
    route_coordinates = extract_coordinates_from_kml(file_path)

    #if route_coordinates:
    #    print("Extracted Coordinates:")
    #    for coord in route_coordinates:
    #        print(coord)

    if route_coordinates:
        # Format the list into the desired string
        coordinates_as_string = format_coordinates_to_string(route_coordinates)

    print("Done")
    print(coordinates_as_string)
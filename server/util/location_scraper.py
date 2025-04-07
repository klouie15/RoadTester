from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pandas as pd
import re
import requests
import time

URL = "https://www.icbc.com/driver-licensing/visit-dl-office/Book-a-road-test"

LOCATIONS_UL_CLASS = "group/list styled-list mb-4 list-disc pl-6 [&>li>ul]:my-1"
LOCATIONS_UL_POSITION = 1

ADDRESS_STARTS_WITH_EXPLICIT_UNIT_PATTERN = r"^\s*Unit\s+\S+\s+"
ADDRESS_STARTS_WITH_IMPLICIT_UNIT_PATTERN = r"^\s*\S+-"
ADDRESS_ENDS_WITH_EXPLICIT_UNIT_PATTERN = r",\s*Unit\s+\S+$"
ADDRESS_NUMBER_ABBREVIATION_PATTERN = r"\bNo\.\s*"
ADDRESS_NUMBER_SUFFIX_PATTERN = r"(\d\d\d+)(st|nd|rd|th)\b"
ADDRESS_STREET_NAME_ONLY_PATTERN = r'^\d+\s+'

SAVE_PATH = "../../data/locations.json"


def scrape_locations() -> pd.DataFrame:
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    ul_content = soup.find_all("ul", class_=LOCATIONS_UL_CLASS)[LOCATIONS_UL_POSITION]
    p_elems = ul_content.find_all("p")

    locations_dict = {}
    for i, p in enumerate(p_elems):
        locations_dict[i] = p.text.split(",", 1)
        locations_dict[i][1] = locations_dict[i][1].strip()

    locations = (pd.DataFrame.from_dict(locations_dict)
                 .transpose()
                 .rename(columns={0: "location", 1: "address"}))

    return locations


def save_locations(path: str, locations: pd.DataFrame) -> None:
    if path.endswith(".json"):
        locations.to_json(path, orient="records", indent=2)

    elif path.endswith(".csv"):
        locations.set_index("location").to_csv(path)

    print("Saved location data to " + path)


def retrieve_location_coordinates(locations: pd.DataFrame) -> pd.DataFrame:
    nominatim = Nominatim(user_agent="road_tester", timeout=10)
    locations = locations.copy().drop_duplicates(subset=["address"])

    locations["street_name"] = locations["address"].apply(extract_street_name)
    locations["city"] = locations["location"].str.replace(r"\s*\(.*?\)", "", regex=True)

    def try_geocode(query: str, max_retries: int = 3) -> tuple[float, float] | None:
        for attempt in range(max_retries):
            try:
                result = nominatim.geocode(query)
                if result:
                    return result.latitude, result.longitude
            except Exception as e:
                print(f"Geocoding attempt {attempt + 1} failed for query '{query}': {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retrying
        return None

    def generate_queries(row: pd.Series) -> list[str]:
        queries = [
            f"ICBC {row['street_name']}, {row['city']}, British Columbia, Canada",
            f"ICBC {row['address']}, {row['city']}, British Columbia, Canada",
            f"{row['address']}, {row['city']}, British Columbia, Canada",
            f"{row['street_name']}, {row['city']}, British Columbia, Canada"
        ]

        return queries

    def get_coordinates(row: pd.Series) -> tuple[float, float] | None:
        queries = generate_queries(row)
        for query in queries:
            coords = try_geocode(query)
            if coords:
                print(f"Successfully geocoded: {row['location']} using query: {query}")
                return coords

        print(f"Failed to geocode: {row['location']} after trying all queries")
        return None

    locations["coordinates"] = locations.apply(get_coordinates, axis=1)

    # Report any locations that still failed to geocode
    failed_locations = locations[locations["coordinates"].isna()]
    if not failed_locations.empty:
        print("\nFailed to geocode the following locations:")
        for _, row in failed_locations.iterrows():
            print(f"- {row['location']}: {row['address']}")

    return locations.drop(columns=["street_name", "city"])


def extract_street_name(address: str) -> str:
    return re.sub(ADDRESS_STREET_NAME_ONLY_PATTERN, '', address)


def clean_address(address: str) -> str:
    address = re.sub(ADDRESS_STARTS_WITH_EXPLICIT_UNIT_PATTERN, '', address, flags=re.IGNORECASE)

    address = re.sub(ADDRESS_ENDS_WITH_EXPLICIT_UNIT_PATTERN, '', address, flags=re.IGNORECASE)

    address = re.sub(ADDRESS_STARTS_WITH_IMPLICIT_UNIT_PATTERN, '', address)

    address = re.sub(ADDRESS_NUMBER_ABBREVIATION_PATTERN, "Number ", address, flags=re.IGNORECASE)

    address = re.sub(" - ", " ", address)

    address = re.sub(ADDRESS_NUMBER_SUFFIX_PATTERN, r"\1", address, flags=re.IGNORECASE)

    return address


def compile_locations(path: str) -> None:
    locations = scrape_locations()
    locations["address"] = locations["address"].apply(clean_address)
    locations_with_coordinates = retrieve_location_coordinates(locations)
    save_locations(path, locations_with_coordinates)


compile_locations(SAVE_PATH)

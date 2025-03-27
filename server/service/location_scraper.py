from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pandas as pd
import re
import requests


URL = "https://www.icbc.com/driver-licensing/visit-dl-office/Book-a-road-test"
LOCATIONS_UL_CLASS = "group/list styled-list mb-4 list-disc pl-6 [&>li>ul]:my-1"
LOCATIONS_UL_POSITION = 1
ADDRESS_STARTS_WITH_EXPLICIT_UNIT_PATTERN = r'^\s*Unit\s+\S+\s+'
ADDRESS_STARTS_WITH_IMPLICIT_UNIT_PATTERN = r'^\s*\S+-'
ADDRESS_ENDS_WITH_EXPLICIT_UNIT_PATTERN = r',\s*Unit\s+\S+$'
SAVE_PATH = "../data/locations.json"


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
    locations[["latitude", "longitude"]] = (locations["address"]
                                            .apply(geocode)
                                            .apply(pd.Series))
    return locations


def geocode(address: str) -> tuple[str, str] | tuple[None, None]:
    nominatim = Nominatim(user_agent="road_tester", timeout=5)
    result = nominatim.geocode(address)

    if result:
        latitude = result.latitude
        longitude = result.longitude
        return latitude, longitude

    return None, None


def clean_address(address: str) -> str:
    address = re.sub(ADDRESS_STARTS_WITH_EXPLICIT_UNIT_PATTERN, '', address, flags=re.IGNORECASE)

    address = re.sub(ADDRESS_ENDS_WITH_EXPLICIT_UNIT_PATTERN, '', address, flags=re.IGNORECASE)

    address = re.sub(ADDRESS_STARTS_WITH_IMPLICIT_UNIT_PATTERN, '', address)

    return address



def compile_locations(path: str) -> None:
    locations = scrape_locations()
    locations["address"] = locations["address"].apply(clean_address)
    locations_with_coordinates = retrieve_location_coordinates(locations)
    save_locations(path, locations_with_coordinates)


compile_locations(SAVE_PATH)

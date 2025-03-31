from typing import List


def decode_polyline(encoded: str) -> List[List[float]]:
    index = 0
    len_encoded = len(encoded)
    points = []
    lat = 0
    lng = 0

    while index < len_encoded:
        shift = 0
        result = 0
        byte = None

        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break

        dlat = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lat += dlat

        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break

        dlng = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lng += dlng

        points.append([lat / 1e5, lng / 1e5])

    return points

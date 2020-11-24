import random
import math
from geopy.distance import geodesic
left_bottom = (39.979255, 116.344386)
right_top = (39.986275, 116.352862)


def random_float(a: float, b: float) -> float:
    return a + random.random() * (b - a)

def distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d


def generate_points(begint: int, endt: int, delta:int=4):
    result = ""
    t = begint
    pos_lat = random_float(left_bottom[0], right_top[0])
    pos_long = random_float(left_bottom[1], right_top[1])
    total_distance = 0
    while t <= endt:
        if (result != ''):
            result += '@'
        lat_delta = random.random() / 4000
        long_delta = random.random() / 4000
        total_distance += geodesic((pos_lat, pos_long),
                                   (pos_lat + lat_delta, pos_long + long_delta)).meters
        pos_lat += lat_delta
        pos_long += long_delta
        result += "{},{};{};null;null;2.0;null".format(pos_lat, pos_long, t)
        t += delta
    return (result, begint, t - delta, t - delta - begint, total_distance, total_distance / (endt - begint))


if __name__ == "__main__":
    print(generate_points(1605668252, 1605668550, 4))

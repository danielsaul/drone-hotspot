from math import degrees, radians, sin, cos, asin, atan2, sqrt

def displaceLatLon(loc, bearing, distance):
    bearing = radians(bearing)
    dx = distance * sin(bearing)
    dy = distance * cos(bearing)
    delta_lon = dx/(111320*cos(radians(loc['latitude'])))
    delta_lat = dy/110540
    final_loc = {
        'longitude': loc['longitude'] + delta_lon,
        'latitude':  loc['latitude'] + delta_lat
    }
    return final_loc


def distanceBetweenPoints(a, b):
    
    # Convert to radians from decimal degrees
    lat1 = radians(a['latitude'])
    lon1 = radians(a['longitude'])
    lat2 = radians(b['latitude'])
    lon2 = radians(b['longitude'])

    # Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    
    return c * r * 1000

def bearingBetweenPoints(a, b):
 
    # Convert to radians from decimal degrees
    lat1 = radians(a['latitude'])
    lon1 = radians(a['longitude'])
    lat2 = radians(b['latitude'])
    lon2 = radians(b['longitude'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
   
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dlon))
    z = atan2(x, y)

    return (degrees(z) + 360) % 360

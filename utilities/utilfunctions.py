from math import cos, sin, sqrt
from yandex_geocoder import Client
from utilities.ref_data import mkad_perimeter
from utilities.haversine import Haversine

# This is a client for the Yandex Geocoder API created using Python's yandex_geocoder library.
yandex_client = Client('6faa9fd5-ff21-4225-8ac6-54f32b850437')

def ray_casting(point, polygon=mkad_perimeter):
    """
    This function determines whether or not a point is inside a polygon
    using the 'Ray casting algorithm'.
    
    Input:
    point - list of length 2
    polygon - list of lists with at least 3 points
    
    Usage example: ray_casting([45.7864, 32.1235])
    """
    # Assertion checking
    assert(type(point) == list)
    assert(len(point) == 2)
    assert(type(polygon) == list)
    assert(len(polygon) >= 3)

    # First we determine the number of vertices that the polygon has.
    polygon_vertices = len(polygon) # Int

    is_in = False # Boolean
    # Getting the coordinates of the point
    x = point[0] # Float
    y = point[1] # Float

    for i in range(polygon_vertices - 1):
        # Getting the coordiantes of the vertices of side i.
        x1 = polygon[i][0] # Float
        x2 = polygon[i + 1][0] # Float
        y1 = polygon[i][1] # Float
        y2 = polygon[i + 1][1] # Float
        
        # Checking whether the point intercepts the side i.
        # The first condition checks if the y coordinate is between y1 and y2.
        # The second condition checks if the x coordinate is lower than the intersection of the ray with the side i.
        if (y < y1 != y < y2) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            # Since we start from False if the number of interception is odd the point is inside the polygon
            # and if it is even it is outside of it
            is_in = not is_in

    return is_in


def distance_to_polygon(point, polygon=mkad_perimeter):
    '''
    This function calculates the distance from a point to a given polygon, asuming that points are so abundant and closely spaced that making use of the Haversine formula to get the distance from the point to the closest vertix won't generate considerable deviations, which in our specific case seems fair.

    Input:
    point - list of length 2
    polygon - list of lists with at least 3 points
    
    Usage example: distance_to_polygon([45.7864, 32.1235])
    '''
    # Assertion checking
    assert(type(point) == list)
    assert(len(point) == 2)
    assert(type(polygon) == list)
    assert(len(polygon) >= 3)

    min_distance = None # Initialized as None but Float after first iteration

    # Once again we start by getting the length of the array of vertices
    polygon_vertices = len(polygon) # Int

    # We iterate over all the vertices
    for i in range(polygon_vertices):
        new_distance = Haversine(point, polygon[i]).km # Float. Distance from point to vertix i
        if min_distance is not None:
            min_distance = min(new_distance, min_distance) # Float. We keep the shortest distance
        else:
            min_distance = new_distance # Float. in the first iteration we set the current value to the     calculated one
        
    return min_distance





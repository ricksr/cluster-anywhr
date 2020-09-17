from ..db import queries
from .new_hex_loc import*

# boundary_options = [0, 1, 2, 3, 4, 5]

def find_new_hex_loc(boundary_of_origin_hex, origin_hex_name):
    # new_hex_loc = find_new_hex_loc(boundary_of_origin_hex, origin_hex)
    origin_hex_location = queries.get_hex_location_by_name(origin_hex_name)
    print(origin_hex_location)
    coords = origin_hex_location['hexagons'][0].get('location', '')
    if(coords) :
        loc = [
            coords['x1'],
            coords['x2'],
            coords['y1'],
            coords['y2'],
            coords['y3']
        ]
        # return loc
        
        if (boundary_of_origin_hex>=0 and boundary_of_origin_hex<=5):
            if boundary_of_origin_hex == 0:
                new_hex_loc = find_up(loc)
                print(new_hex_loc)
                return new_hex_loc

            if boundary_of_origin_hex == 1:
                new_hex_loc = find_right_north(loc)
                print(new_hex_loc)
                return new_hex_loc

            if boundary_of_origin_hex == 2:
                new_hex_loc = find_right_south(loc)
                print(new_hex_loc)
                return new_hex_loc

            if boundary_of_origin_hex == 3:
                new_hex_loc = find_down(loc)
                print(new_hex_loc)
                return new_hex_loc

            if boundary_of_origin_hex == 4:
                new_hex_loc = find_left_south(loc)
                print(new_hex_loc)
                return new_hex_loc
                
            if boundary_of_origin_hex == 5:
                new_hex_loc = find_left_north(loc)
                print(new_hex_loc)
                return new_hex_loc


    else:
        return None
    

# find_new_hex_loc([1,1,1,1,1,1], 'a')

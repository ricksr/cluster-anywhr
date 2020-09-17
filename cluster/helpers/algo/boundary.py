from ..db import queries


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
        return loc
    else:
        return None
    

# find_new_hex_loc([1,1,1,1,1,1], 'a')

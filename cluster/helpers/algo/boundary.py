from ..db import queries
from .new_hex_loc import*

# boundary_options = [0, 1, 2, 3, 4, 5]


def find_new_hex_loc(boundary_of_origin_hex, origin_hex_name, origin_hex_location):

    coords = origin_hex_location.get('hexagons', [{'location': {}}])[0].get('location', '')
    if(coords):
        loc = [
            coords['q'],
            coords['r'],
            coords['s']
        ]
        # print(f'\n\n coords----{find_up(loc)}-{boundary_of_origin_hex==1}--\n')
        # return find_up(loc)

        if boundary_of_origin_hex == 0:
            return find_up(loc)
                
        elif boundary_of_origin_hex == 1:
            return find_right_north(loc)
            
        elif boundary_of_origin_hex == 2:
            return find_right_south(loc)
            
        elif boundary_of_origin_hex == 3:
            return find_down(loc)
            
        elif boundary_of_origin_hex == 4:
            return find_left_south(loc)
            
        elif boundary_of_origin_hex == 5:
            return find_left_north(loc)
    else:
        return None
            


# find_new_hex_loc([0,0,0], 'a')

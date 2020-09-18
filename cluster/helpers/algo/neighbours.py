from ..db import queries
from .new_hex_loc import*
from ..utils import utils


def find_new_hex_neighbours(loc, boundary_of_origin_hex):
    if (boundary_of_origin_hex>=0 and boundary_of_origin_hex<=5):
        f1 = True and not(boundary_of_origin_hex==0)
        f2 = True and not(boundary_of_origin_hex==1)
        f3 = True and not(boundary_of_origin_hex==2)
        f4 = True and not(boundary_of_origin_hex==3)
        f5 = True and not(boundary_of_origin_hex==4)

        resp = {}

        n1 = find_up(loc)
        n2 = find_right_north(loc)
        n3 = find_right_south(loc)
        n4 = find_down(loc)
        n5 = find_left_south(loc)
        n6 = find_left_north(loc)
        
        resp["n1"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n1[0], n1[1], n1[2])))
        resp["n2"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n2[0], n2[1], n2[2])))
        resp["n3"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n3[0], n3[1], n3[2])))
        resp["n4"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n4[0], n4[1], n4[2])))
        resp["n5"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n5[0], n5[1], n5[2])))
        resp["n6"] = list(map(lambda data: data.get('hexagon_id'), queries.get_hex_id_by_location(n6[0], n6[1], n6[2])))
       
        resp["n1"] = "NO" if len(resp["n1"])==0 else resp["n1"][0]
        resp["n2"] = "NO" if len(resp["n2"])==0 else resp["n2"][0]
        resp["n3"] = "NO" if len(resp["n3"])==0 else resp["n3"][0]
        resp["n4"] = "NO" if len(resp["n4"])==0 else resp["n4"][0]
        resp["n5"] = "NO" if len(resp["n5"])==0 else resp["n5"][0]
        resp["n6"] = "NO" if len(resp["n6"])==0 else resp["n6"][0]
        # resp.pop(utils.user_boundary_choice[boundary_of_origin_hex])
        print(resp)
    return resp
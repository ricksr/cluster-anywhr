from ..db import queries
from .new_hex_loc import*
from ..utils import utils


def find_new_hex_neighbours(loc, boundary_of_origin_hex):

    if (boundary_of_origin_hex >= 0 and boundary_of_origin_hex <= 5):

        resp = {}

        n1 = find_up(loc)
        n2 = find_right_north(loc)
        n3 = find_right_south(loc)
        n4 = find_down(loc)
        n5 = find_left_south(loc)
        n6 = find_left_north(loc)

        borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']

        for border in borders:
            resp[border] = list(map(lambda data: data.get(
                'hexagon_id'), queries.get_hex_id_by_location(border[0], border[1], border[2])))

        for border in borders:
            resp[border] = "NO" if (
                len(resp[border]) == 0 or resp[border] == "NO") else resp[border][0]

        # print(resp)
    return resp

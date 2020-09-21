from helpers.algo import boundary, neighbours
from queue import Queue
# print(algo)
# boundary.find_new_hex_loc(1, 'a')

# neighbours.find_new_hex_neighbours([0,0,0], 0)


def bfs():
    origin_hex = request.args['src']

    if origin_hex:
        try:
            neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
        except:
            return {"err": "error"}

    neighbours_of_origin = neighbours_of_origin[0]

    origin_hex_id = neighbours_of_origin.get(
        "hex", "").get("hexagon_id", "")

    frontier = Queue()
    frontier.put(origin_hex_id)

    reached = set()
    reached.add(origin_hex_id)

    level = 0
    borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']

    while not frontier.empty():
        level = level + 1
        current = frontier.get()
        details_neighbour_hex = queries.get_hex_details_by_id(
            current).get("hexagons", "")

        if len(details_neighbour_hex) > 0:
            details_neighbour_hex = details_neighbour_hex[0]

        for border in borders:
            if details_neighbour_hex.get("hex", "").get(border, "") != "NO":
                neighbour_id = details_neighbour_hex.get(
                    "hex", "").get(border, "")

                if (level > 1):
                    if(neighbour_id == origin_hex_id)

        for next in graph.neighbors(current):
            if next not in reached:
                frontier.put(next)
                reached.add(next)

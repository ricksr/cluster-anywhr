import json
from flask import Flask, request
from flask_cors import CORS
from queue import Queue

from helpers.utils import utils
from helpers.db import queries
from helpers.algo import boundary
from helpers.algo import neighbours
from helpers.algo import degrees_count
from helpers.algo.new_hex_loc import*


app = Flask(__name__)
CORS(app)


def logger(val):
    print("\n{}\n".format(val))


@app.route('/get-hex-by-name', methods=['GET', 'POST'])
# @cross_origin()
def search_hex_byName():
    name = request.args['name']
    logger(name)
    if(name):
        try:
            resp = queries.get_hex_details_by_name(name)
            logger(resp)
            return resp
        except:
            return {"err": "error"}
    else:
        return {"Please enter the name correctly to get all the details"}
    return {'Network Error'}


@app.route('/get-hex-by-id', methods=['GET', 'POST'])
# @cross_origin()
def search_hex_byId():
    id = request.args['id']
    logger(id)
    if(id):
        try:
            resp = queries.get_hex_details_by_id(id)
            logger(resp)
            return resp
        except:
            logger(resp)
            return resp
    else:
        return {"Please enter the id correctly to get all the details"}
    return {"err": 'Network Error'}


@app.route('/get-all-coordinates', methods=['GET', 'POST'])
# @cross_origin()
def get_all_coords():
    try:
        coords = queries.get_all_locations()
        logger(coords)
        return {'body': coords}
    except:
        return {"err": 'Network Error'}


@app.route('/add-hex', methods=['GET', 'POST'])
# @cross_origin()
def add_hex():

    origin_hex = request.args['src']
    new_hex = request.args['new']
    boundary_of_origin_hex = request.args['loc']
    boundary_of_origin_hex = int(boundary_of_origin_hex)

    if(origin_hex and new_hex and (boundary_of_origin_hex >= 0)):
        origin_coordinates_hex = queries.get_hex_location_by_name(origin_hex)

        origin_hex_is_active_or_not = origin_coordinates_hex.get("hexagons")[0].get(
            'is_active', '')

        # checking if the src hex is_active or not
        if origin_hex_is_active_or_not == "FALSE":
            return {"err": "This origin hex is not active"}

        logger('-----here-----get_hex_location_by_name-origin---')
        logger(origin_coordinates_hex)

        origin_existing_neighbours = queries.get_hex_details_by_name(
            origin_hex).get("hexagons", "")[0].get("hex", "")

        if origin_existing_neighbours[utils.user_boundary_choice[boundary_of_origin_hex]] != 'NO':
            return {'err': 'already a hex exists at this boundary'}

        origin_id = origin_coordinates_hex.get("hexagons")[0].get(
            'location', '').get('hexagon_id', '')

        # Find location of the new hex
        # find neighbours around it , if present query their cluster table rows

        new_hex_loc = boundary.find_new_hex_loc(
            boundary_of_origin_hex, origin_hex, origin_coordinates_hex)  # New Hex location

        logger('-----here-----new-hex-loc-using-origin-loc-and-border---')
        logger(new_hex_loc)

        new_hex_neighbours = neighbours.find_new_hex_neighbours(
            new_hex_loc, boundary_of_origin_hex)                       # Neighbours around new hex

        # insertions new hex // fetch id
        logger('-----here-----inserting-new-node---')

        insert_new_hex_resp = queries.insert_new_hex(new_hex)
        new_hexagon_id = list(map(lambda data: data.get(
            'hexagon_id'),  insert_new_hex_resp))[0]

        logger(new_hexagon_id)

        # insert neighbours of new node
        logger('-----here-----inserting-new-node-neighbours---')

        new_hex_neighbours["hexagon_id"] = new_hexagon_id

        logger(new_hex_neighbours)

        column_updates = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'updated_at']
        insert_new_hex_neighbours = queries.insert_hex_neighbours(
            {"data": new_hex_neighbours, "colm": column_updates})          # Inserting New hex Neighs. in cluster

        # insert location of new node

        insert_new_hex_loc = queries.insert_new_hex_loc(
            new_hexagon_id, new_hex_loc[0], new_hex_loc[1], new_hex_loc[2])

        # insert neighbours of origin node

        origin_req = {}
        origin_req[utils.user_boundary_choice[boundary_of_origin_hex]
                   ] = new_hexagon_id
        origin_req["hexagon_id"] = origin_id
        column_updates = [
            utils.user_boundary_choice[boundary_of_origin_hex], 'updated_at']

        logger({"data": origin_req, "colm": column_updates})

        update_origin_hex_neighbour = queries.insert_hex_neighbours(
            {"data": origin_req, "colm": column_updates})
        logger("----moving to update----")
        update_neighbours(new_hex_neighbours)

        return {"statusCode": 200, 'response': update_origin_hex_neighbour}
    else:
        return {'response': 'err'}


def update_neighbours(updating_neighbours):
    # logger(updating_neighbours)
    for border in updating_neighbours:
        if (updating_neighbours[border] != 'NO'):
            hex_id = updating_neighbours[border]
            # logger(hex_id)
            neighbour_location_obj = queries.get_hex_location_by_id(hex_id)

            neighbour_is_active = neighbour_location_obj.get(
                'hexagons', [{'location': {}}])[0].get('is_active', '')

            if neighbour_is_active == 'TRUE':

                neighbour_location_dict = neighbour_location_obj.get(
                    'hexagons', [{'location': {}}])[0].get('location', '')
                # logger(neighbour_location_dict)
                if(neighbour_location_dict):
                    loc = [
                        neighbour_location_dict['q'],
                        neighbour_location_dict['r'],
                        neighbour_location_dict['s']
                    ]
                    updated_neighbours = neighbours.find_new_hex_neighbours(
                        loc, 1)

                    logger(updated_neighbours)

                    updated_neighbours["hexagon_id"] = hex_id
                    # logger(updated_neighbours)
                    column_updates = ['n1', 'n2', 'n3',
                                      'n4', 'n5', 'n6', 'updated_at']
                    insert_updated_neighbours = queries.insert_hex_neighbours(
                        {"data": updated_neighbours, "colm": column_updates})

                    return {"body": insert_updated_neighbours}

    return {"err": "error"}


@app.route('/remove-hex', methods=['GET', 'POST'])
# @cross_origin()
def delete_hex_bfs():
    borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']
    border_map = {'n1': 'n4', 'n2': 'n5', 'n3': 'n6',
                  'n4': 'n1', 'n5': 'n2', 'n6': 'n3'}

    origin_hex = request.args['src']

    if origin_hex:
        try:
            neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
        except:
            return {"err": "error"}

    # The hex is alerady deleted or doesn't exist
    if len(neighbours_of_origin) > 0:
        neighbours_of_origin = neighbours_of_origin[0]
    else:
        return {"err": "error"}

    origin_hex_id = neighbours_of_origin.get("hex", "").get("hexagon_id", "")

    degree = degrees_count.calc_degree(neighbours_of_origin)
    if degree < 2:
        delete_resp = delete_hexagon_final(
            neighbours_of_origin, origin_hex, origin_hex_id, borders, border_map)
        if delete_resp:
            return {"body": "Done!"}
        else:
            return {"err": "error while removing"}

    # starting bfs
    frontier = Queue()
    frontier.put(origin_hex_id)
    # this map for id's
    reached = set()
    reached.add(origin_hex_id)
    # this map for (id, border(n1, n2...n6)) to uniquely identify the path we are using
    # to find it
    reached_border = []

    level = 0

    while not frontier.empty():
        level = level + 1
        current = frontier.get()
        # fetching all the neighbour id's in a level
        details_neighbour_hex = queries.get_hex_details_by_id(
            current).get("hexagons", "")

        if len(details_neighbour_hex) > 0:
            details_neighbour_hex = details_neighbour_hex[0]
        # iterating in all the neighbours of the recent id
        for border in borders:
            if details_neighbour_hex.get("hex", "").get(border, "") != "NO":
                neighbour_id = details_neighbour_hex.get(
                    "hex", "").get(border, "")

                if level == 1:
                    # reached_border.append((current_id, border))
                    reached_border.append((current, border_map[border]))
                    list(set(reached_border))
                # already visited node also traversed through the same path
                if (neighbour_id in reached) and (neighbour_id, border) in reached_border:
                    continue

                if (level > 1):
                    if ((neighbour_id not in reached) or
                            ((neighbour_id in reached) and (neighbour_id, border) not in reached_border)):
                        # the origin hex is found but not from the same path ,
                        # from a different path
                        if(neighbour_id == origin_hex_id):
                            # if the hex is found update its neighs. and itself
                            delete_resp = delete_hexagon_final(
                                neighbours_of_origin, origin_hex, origin_hex_id, borders, border_map)

                            if delete_resp:
                                return {"body": "Done!"}
                            else:
                                return {"err": "error while removing"}
                # mapping the new neighbour and its correspoding border
                # so that we dom't end up seeing that id from the previous path
                frontier.put(neighbour_id)
                reached.add(neighbour_id)
                logger(neighbour_id)
                logger(border)
                # reached_border.append((neighbour_id, border))
                reached_border.append((current, border_map[border]))
                list(set(reached_border))

    return {"err": "Not possible to remove"}


def delete_hexagon_final(neighbours_of_origin, origin_hex, origin_hex_id, borders, border_map):
    for border in borders:
        if neighbours_of_origin.get("hex", "").get(border, "") != "NO":
            neighbour_id = neighbours_of_origin.get(
                "hex", "").get(border, "")
            origin_req = {}
            origin_req["hexagon_id"] = neighbour_id
            origin_req[border_map[border]] = "NO"
            column_updates = [
                border_map[border], "updated_at"]
            insert_updated_neighbours = queries.insert_hex_neighbours(
                {"data": origin_req, "colm": column_updates})
    try:
        deletion_resp = queries.delete_hex(
            origin_hex, origin_hex_id)
        return True
    except:
        return False

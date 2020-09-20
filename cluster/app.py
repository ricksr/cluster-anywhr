import json
from flask import Flask, request
from flask_cors import CORS

from helpers.utils import utils
from helpers.db import queries
from helpers.algo import boundary
from helpers.algo import neighbours
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

            neighbour_location_dict = neighbour_location_obj.get(
                'hexagons', [{'location': {}}])[0].get('location', '')
            # logger(neighbour_location_dict)
            if(neighbour_location_dict):
                loc = [
                    neighbour_location_dict['q'],
                    neighbour_location_dict['r'],
                    neighbour_location_dict['s']
                ]
                updated_neighbours = neighbours.find_new_hex_neighbours(loc, 1)

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
def delete_hex():
    origin_hex = request.args['src']

    if origin_hex:
        try:
            neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
        except:
            return {"err": "error"}

        # Constants

        degrees = 6
        borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']
        border_map = {'n1': 'n4', 'n2': 'n5', 'n3': 'n6',
                      'n4': 'n1', 'n5': 'n2', 'n6': 'n3'}

        neighbours_of_origin = neighbours_of_origin[0]

        origin_hex_id = neighbours_of_origin.get(
            "hex", "").get("hexagon_id", "")

        degrees = calc_degree(neighbours_of_origin)

        logger(degrees)

        if degrees > 2:

            hotspot_or_not = 0

            for border in borders:
                # Level 2
                if neighbours_of_origin.get("hex", "").get(border, "") != "NO":
                    neighbour_id = neighbours_of_origin.get(
                        "hex", "").get(border, "")
                    # level 3
                    # check if the degree of the neighbour >= 2 , i.e hotspot
                    
                    details_neighbour_hex = queries.get_hex_details_by_id(
                        neighbour_id).get("hexagons", "")[0]

                    degrees_level_two = calc_degree(details_neighbour_hex)
                    if degrees_level_two >= 2:
                        hotspot_or_not = hotspot_or_not + 1
            
            # if more than two hot spot exists then it can be removed 
            if hotspot_or_not > 2:
                # border{n1 n2 ... n6} neighbour id
                for border in borders:
                    origin_req = {}
                    origin_req["hexagon_id"] = neighbour_id
                    origin_req[border_map[border]] = "NO"
                    column_updates = [border_map[border], "updated_at"]
                    insert_updated_neighbours = queries.insert_hex_neighbours(
                        {"data": origin_req, "colm": column_updates})

                try:
                    deletion_resp = queries.delete_hex(origin_hex, origin_hex_id)
                    return {"body": deletion_resp}
                except:
                    return {"err": "error"}
            else:
                return {"err": "Not possible to remove"}
        else:
            return {"err": "Not possible to remove"}
    else:
        return {"err": "provide valid name"}


def calc_degree(neighbours_of_origin):
    degrees = 6
    # for border in borders:
    if neighbours_of_origin.get("hex", "").get('n1', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n1', ""))

    if neighbours_of_origin.get("hex", "").get('n2', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n2', ""))

    if neighbours_of_origin.get("hex", "").get('n3', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n3', ""))

    if neighbours_of_origin.get("hex", "").get('n4', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n4', ""))

    if neighbours_of_origin.get("hex", "").get('n5', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n5', ""))

    if neighbours_of_origin.get("hex", "").get('n6', "") == "NO":
        degrees = degrees - 1
        logger(neighbours_of_origin.get("hex", "").get('n6', ""))

    return int(degrees)

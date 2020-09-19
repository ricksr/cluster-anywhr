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
            logger(resp)
            return resp
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
    return {"err":'Network Error'}


@app.route('/get-all-coordinates', methods=['GET', 'POST'])
# @cross_origin()
def get_all_coords():
    try:
        coords = queries.get_all_locations()
        logger(coords)
        return {'body': coords}
    except:
        return {"err":'Network Error'}


@app.route('/add-hex', methods=['GET', 'POST'])
# @cross_origin()
def add_hex():

    origin_hex = request.args['src']
    new_hex = request.args['new']
    boundary_of_origin_hex = request.args['loc']
    boundary_of_origin_hex = int(boundary_of_origin_hex)

    if(origin_hex and new_hex and boundary_of_origin_hex):
        origin_coordinates_hex = queries.get_hex_location_by_name(origin_hex)
        logger('-----here-----get_hex_location_by_name-origin---')
        logger(origin_coordinates_hex)
        origin_id = origin_coordinates_hex.get("hexagons")[0].get(
            'location', '').get('hexagon_id', '')

        # Find location of the new hex
        # find neighbours around it , if present query their cluster table rows

        new_hex_loc = boundary.find_new_hex_loc(
            boundary_of_origin_hex, origin_hex, origin_coordinates_hex)

        logger('-----here-----new-hex-loc-using-origin-loc-and-border---')
        logger(new_hex_loc)
        new_hex_neighbours = neighbours.find_new_hex_neighbours(
            new_hex_loc, boundary_of_origin_hex)

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
            {"data": new_hex_neighbours, "colm": column_updates})

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

        return {"statusCode": 200, 'response': update_origin_hex_neighbour}
    else:
        return {'response': 'err'}


@app.route('/remove-hex', methods=['GET', 'POST'])
# @cross_origin()
def delete_hex():
    origin_hex = request.args['src']

    if origin_hex:
        try:
            neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
        except:
            return {"err":"error"}
        degrees = 6
        neighbours_of_origin = neighbours_of_origin[0]

        if neighbours_of_origin.get("hex","").get("n1","") == "NO":
            degrees = degrees - 1
        if neighbours_of_origin.get("hex","").get("n2","") == "NO":
            degrees = degrees - 1
        if neighbours_of_origin.get("hex","").get("n3","") == "NO":
            degrees = degrees - 1
        if neighbours_of_origin.get("hex","").get("n4","") == "NO":
            degrees = degrees - 1
        if neighbours_of_origin.get("hex","").get("n5","") == "NO":
            degrees = degrees - 1
        if neighbours_of_origin.get("hex","").get("n6","") == "NO":
            degrees = degrees - 1
        
        
        if degrees > 2:
            try:
                deletion_resp = queries.delete_hex(origin_hex)
                return {"body": deletion_resp}
            except:
                return {"err":"error"}
        else:
            return {"err":"Not possible to remove"}
    else:
        return {"err":"provide valid name"}
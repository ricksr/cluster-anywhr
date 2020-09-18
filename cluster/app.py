import json
from flask import Flask, request

from helpers.db import queries
from helpers.algo.boundary import*
from helpers.algo.neighbours import*
from helpers.algo.new_hex_loc import*


app = Flask(__name__)

def logger(val):
	print("\n{}\n".format(val))

@app.route('/get-hex-by-name', methods=['GET', 'POST'])
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
	return {'Network Error'}


@app.route('/add-hex', methods=['GET','POST'])
def add_hex():
	try:
		origin_hex = request.args['src']  
		new_hex = request.args['new'] 
		boundary_of_origin_hex = request.args['loc']

		if(origin_hex and new_hex and boundary_of_origin_hex):
			origin_coordinates_hex = queries.get_hex_location_by_name(origin_hex)  
			# todo
			# Find location of the new hex
			# find neighbours around it , if present query their cluster table rows
			
			new_hex_loc = find_new_hex_loc(boundary_of_origin_hex, origin_hex)
			new_hex_neighbours = find_new_hex_neighbours(new_hex_loc, boundary_of_origin_hex)

			# insertions new hex // fetch id
			
			insert_new_hex_resp = queries.insert_new_hex(new_hex)
			new_hexagon_id = insert_new_hex_resp.get("hexagon_id", "")

			# insert neighbours of new node

			new_hex_neighbours["hexagon_id"] = new_hexagon_id
			column_updates = ['n1','n2','n3','n4','n5','n6', 'updated_at']
			insert_new_hex_neighbours = queries.insert_hex_neighbours(new_hex_neighbours, column_updates)

			# insert location of new node

			insert_new_hex_loc = queries.insert_new_hex_loc(new_hexagon_id, new_hex_loc[0], new_hex_loc[1], new_hex_loc[2])
			
			# insert neighbours of origin node

			origin_req = {}
			origin_req[utils.user_boundary_choice[boundary_of_origin_hex]] = new_hexagon_id
			column_updates = [utils.user_boundary_choice[boundary_of_origin_hex], 'updated_at']
			update_origin_hex_neighbour = queries.insert_hex_neighbours(origin_req, column_updates)

			return {"statusCode": 200, 'response': update_origin_hex_neighbour}
		else:
			return {'response': 'err'}
	except:
		return {'Network Error'}
	
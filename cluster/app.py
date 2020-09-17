import json
from flask import Flask, request
from helpers.db import queries
import utils
from helpers.algo.boundary import*
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
def insertMember():
	try:
		origin_hex = request.args['src']  
		new_hex = request.args['new'] 
		boundary_of_origin_hex = utils.user_boundary_choice[request.args['loc']]

		if(origin_hex and new_hex and boundary_of_origin_hex):
			origin_coordinates_hex = queries.get_hex_location_by_name(origin_hex)  
			# todo
			# Find location of the new hex
			# find neighbours around it , if present query their cluster table rows
			new_hex_loc = find_new_hex_loc(boundary_of_origin_hex, origin_hex)

			resp = queries.insert_member(id, real_name, tz)
			return {"statusCode": 200, 'response': resp}
		else:
			return {'response': 'please insert unique id, real_name , tz'}
	except:
		return {'Network Error'}
	
    

@app.route('/add-member-activity', methods=['GET','POST'])
def insertMemberACtivity():
	try:
		id = request.args['id'] 
		start_time = request.args['start_time'] 
		end_time = request.args['end_time']
		if(id and start_time and end_time):
			resp = queries.insert_member_activity(id, start_time, end_time)
			return {"statusCode": 200, 'response': resp}
		else:
			return {'response': 'please all datas , i.e., id, start_time, end_time'}
	except:
		return {'Network error'}


@app.route('/dummy', methods=['GET'])
def getDummyData():
    return dummy

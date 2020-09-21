# from helpers.algo import boundary, neighbours
# from queue import Queue
# # print(algo)
# # boundary.find_new_hex_loc(1, 'a')

# # neighbours.find_new_hex_neighbours([0,0,0], 0)


# def bfs():
#     origin_hex = request.args['src']

#     if origin_hex:
#         try:
#             neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
#         except:
#             return {"err": "error"}

#     neighbours_of_origin = neighbours_of_origin[0]

#     origin_hex_id = neighbours_of_origin.get(
#         "hex", "").get("hexagon_id", "")

#     frontier = Queue()
#     frontier.put(origin_hex_id)
#     # this map for id's
#     reached = set()
#     reached.add(origin_hex_id)
#     # this map for (id, border(n1, n2...n6)) to uniquely identify the path we are using 
#     # to find it
#     reached_border = []
#     # reached_border.append(origin_hex_id, 'n1')

#     level = 0
#     borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']
#     border_map = {'n1': 'n4', 'n2': 'n5', 'n3': 'n6',
#                   'n4': 'n1', 'n5': 'n2', 'n6': 'n3'}

#     while not frontier.empty():
#         level = level + 1
#         current = frontier.get()
#         # fetching all the neighbour id's in a level 
#         details_neighbour_hex = queries.get_hex_details_by_id(
#             current).get("hexagons", "")

#         if len(details_neighbour_hex) > 0:
#             details_neighbour_hex = details_neighbour_hex[0]
#         # iterating in all the neighbours of the recent id
#         for border in borders:
#             if details_neighbour_hex.get("hex", "").get(border, "") != "NO":
#                 neighbour_id = details_neighbour_hex.get(
#                     "hex", "").get(border, "")

#                 # already visited node also traversed through the same path
#                 if (neighbour_id in reached) and (neighbour_id, border) in reached_border:
#                     continue

#                 if (level > 1):
#                     if ((neighbour_id not in reached) or
#                             ((neighbour_id in reached) and (neighbour_id, border) not in reached_border)):
#                         # the origin hex is found but not from the same path ,
#                         # from a different path
#                         if(neighbour_id == origin_hex_id):
#                             for border in borders:
#                                 if neighbours_of_origin.get("hex", "").get(border, "") != "NO":
#                                     neighbour_id = neighbours_of_origin.get(
#                                         "hex", "").get(border, "")
#                                     origin_req = {}
#                                     origin_req["hexagon_id"] = neighbour_id
#                                     origin_req[border_map[border]] = "NO"
#                                     column_updates = [
#                                         border_map[border], "updated_at"]
#                                     insert_updated_neighbours = queries.insert_hex_neighbours(
#                                         {"data": origin_req, "colm": column_updates})
#                             try:
#                                 deletion_resp = queries.delete_hex(
#                                     origin_hex, origin_hex_id)
#                                 return {"body": deletion_resp}
#                             except:
#                                 return {"err": "error"}
#                 # mapping the new neighbour and its correspoding border
#                 # so that we dom't end up seeing that id from the previous path
#                 frontier.put(neighbour_id)
#                 reached.add(neighbour_id)
#                 reached_border[neighbour_id] = border


# def delete_hex():
#     origin_hex = request.args['src']

#     if origin_hex:
#         try:
#             neighbours_of_origin = queries.find_neighbours_by_name(origin_hex)
#         except:
#             return {"err": "error"}

#         # Constants

#         degrees = 6
#         borders = ['n1', 'n2', 'n3', 'n4', 'n4', 'n5', 'n6']
#         border_map = {'n1': 'n4', 'n2': 'n5', 'n3': 'n6',
#                       'n4': 'n1', 'n5': 'n2', 'n6': 'n3'}

#         neighbours_of_origin = neighbours_of_origin[0]

#         origin_hex_id = neighbours_of_origin.get(
#             "hex", "").get("hexagon_id", "")

#         degrees = calc_degree(neighbours_of_origin)

#         logger(degrees)

#         if degrees > 2:

#             hotspot_or_not = 0

#             for border in borders:
#                 # Level 2
#                 if neighbours_of_origin.get("hex", "").get(border, "") != "NO":
#                     neighbour_id = neighbours_of_origin.get(
#                         "hex", "").get(border, "")
#                     # level 3
#                     # check if the degree of the neighbour >= 2 , i.e hotspot

#                     details_neighbour_hex = queries.get_hex_details_by_id(
#                         neighbour_id).get("hexagons", "")

#                     if len(details_neighbour_hex) > 0:
#                         details_neighbour_hex = details_neighbour_hex[0]
#                         degrees_level_two = calc_degree(details_neighbour_hex)
#                         if degrees_level_two >= 2:
#                             hotspot_or_not = hotspot_or_not + 1

#             # if more than two hot spot exists then it can be removed
#             if hotspot_or_not > 2:
#                 # border{n1 n2 ... n6} neighbour id
#                 for border in borders:
#                     if neighbours_of_origin.get("hex", "").get(border, "") != "NO":
#                         neighbour_id = neighbours_of_origin.get(
#                             "hex", "").get(border, "")
#                         origin_req = {}
#                         origin_req["hexagon_id"] = neighbour_id
#                         origin_req[border_map[border]] = "NO"
#                         column_updates = [border_map[border], "updated_at"]
#                         insert_updated_neighbours = queries.insert_hex_neighbours(
#                             {"data": origin_req, "colm": column_updates})

#                 try:
#                     deletion_resp = queries.delete_hex(
#                         origin_hex, origin_hex_id)
#                     return {"body": deletion_resp}
#                 except:
#                     return {"err": "error"}
#             else:
#                 return {"err": "Not possible to remove"}
#         else:
#             return {"err": "Not possible to remove"}
#     else:
#         return {"err": "provide valid name"}

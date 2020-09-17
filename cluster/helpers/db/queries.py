from  .client import run_query


def insert_member(id, real_name, tz):
    query = '''
        mutation insert_members($id: String, $real_name: String, $tz: String) {
            insert_members(objects: {id: $id, real_name: $real_name, tz: $tz}) {
                returning {
                    id
                }
            }
        }
    '''
    variables = {
        'id': id,
        'real_name': real_name,
        'tz': tz
    }
    response = run_query(query, variables)
    inserted_details = response.get(
        'insert_members', {}).get('returning', [])
    if len(inserted_details) != 1:
        raise RuntimeError('query failed')
    return inserted_details[0]


def insert_member_activity(member_id, start_time, end_time):
    query = '''
        mutation insert_members_activity_periods($member_id: String, $start_time: String, $end_time: String) {
            insert_members_activity_periods(objects: {member_id: $member_id, start_time: $start_time, end_time: $end_time}) {
                returning {
                    id
                }
            }
        }
    '''
    variables = {
        'member_id': member_id,
        'start_time': start_time,
        'end_time': end_time
    }
    response = run_query(query, variables)
    inserted_details = response.get(
        'insert_members_activity_periods', {}).get('returning', [])
    if len(inserted_details) != 1:
        raise RuntimeError('query failed')
    return inserted_details[0]

# ###########################


def get_hex_details_by_name(name):
    query = '''
        query find_hex($name: String!) {
            hexagons(
                where: {
                    name: {_eq: $name}, 
                    is_active: {_eq: "TRUE"}
                }
            ) 
            {
                hex {
                    n1 n2 n3 n4 n5 n6
                }
                name
                is_active
            }
        }

    '''
    variables = {
        "name": name
    }
    response = run_query(query, variables)
    print(response)
    return response

def get_hex_details_by_id(id):
    query = '''
        query find_hex($id: uuid!) {
            hexagons(
                where: {
                    id: {_eq: $id}, 
                    is_active: {_eq: "TRUE"}
                }
            ) 
            {
                hex {
                    n1 n2 n3 n4 n5 n6
                }
                id
                is_active
            }
        }

    '''
    variables = {
        "id": id
    }
    response = run_query(query, variables)
    print(response)
    return response

def get_hex_location_by_name(name):
    query = ''' 
        query hex_location($name: String!) {
            hexagons(
                where: {
                    name: {_eq: $name}
                }
            ) {
                location {
                    hexagon_id x1 x2 y1 y2 y3
                }
            }
        }
    '''
    variables = {
        "name": name
    }
    response = run_query(query, variables)
    print(response)
    return response

from .client import run_query


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
                    hexagon_id q r s
                }
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


def get_hex_location_by_id(id):
    query = ''' 
        query hex_location($id: uuid!) {
            hexagons(
                where: {
                    id: {_eq: $id}
                }
            ) {
                location {
                    hexagon_id q r s
                }
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


def get_hex_id_by_location(q, r, s):
    query = ''' 
        query get_hex_byLoc($q: Int!, $r: Int!, $s: Int!) {
            locations(
                where: {
                    q: {_eq: $q}, 
                    r: {_eq: $r}, 
                    s: {_eq: $s},
                  	hex_name: {
                      is_active: {_eq: "TRUE"}
                    }
                }) { 
                hexagon_id 
            }
        }
    '''
    variables = {
        "q": q,
        "r": r,
        "s": s
    }
    response = run_query(query, variables)
    print(response)
    return response.get("locations", "")


def get_all_locations():
    query = ''' 
        query all_locations {
            locations(
                where: {
                    hex_name: {
                        is_active: {_eq: "TRUE"}
                    }
                }
            ) {
                q r s
                hex_name {
                  name
                }
            }
        }
    '''
    variables = {}
    response = run_query(query, variables)
    print(response)
    return response.get("locations", "")


def insert_new_hex(name):
    query = '''
        mutation insert_hex($name: String!) {
            insert_clusters(
                objects: {
                    hex_id: {
                        data: {name: $name, is_active: "TRUE"}, 
                        on_conflict: {constraint: hexagons_name_key, update_columns: [updated_at, is_active]}
                    }
                }, 
                on_conflict: {
                    constraint: clusters_hexagon_id_key, 
                    update_columns: updated_at
                }
            ) {
                affected_rows
                id: returning {
                    hexagon_id
                }
            }
        }
    '''

    variables = {
        "name": name
    }
    response = run_query(query, variables)
    print(response)
    return response.get("insert_clusters", "").get("id", "")


def insert_hex_neighbours(variables: dict):
    print(variables)
    query = '''
        mutation insert_clusters($data: [clusters_insert_input!]!, $colm: [clusters_update_column!]!) {
            insert_clusters(
                objects: $data , 
                on_conflict: {
                    constraint: clusters_hexagon_id_key, 
                    update_columns: $colm
                }
            ) {
                affected_rows
                returning {
                    hexagon_id
                    n1 n2 n3 n4 n5 n6
                }
            }
        }
    '''
    response = run_query(query, variables)
    print(response)
    return response.get("insert_clusters", "").get("returning", "")


def insert_new_hex_loc(hexagon_id, q, r, s):
    query = '''
            mutation insert_locations(
                $hexagon_id: uuid!,
                $q: Int!,
                $r: Int!,
                $s: Int!
            ) 
            {
                insert_locations(
                    objects: {
                        hexagon_id: $hexagon_id, 
                        q: $q, 
                        r: $r, 
                        s: $s
                    }, 
                    on_conflict: {
                        constraint: location_hexagon_id_key, 
                        update_columns: [q, r, s, updated_at]
                    }
                ) {
                    affected_rows
                    returning {
                        hexagon_id
                        q
                        r
                        s
                    }
                }
            }
        '''
    variables = {
        "hexagon_id": hexagon_id,
        "q": q,
        "r": r,
        "s": s
    }
    response = run_query(query, variables)
    print(response)
    return response.get("insert_locations", "").get("returning", "")


def delete_hex(name, hexagon_id):
    query = '''
        mutation insert_hexagons($name: String!, $hexagon_id: uuid!) {
            insert_hexagons(
                objects: {
                    is_active: "FALSE", 
                    name: $name, 
                    hex: {
                        data: {
                            hexagon_id: $hexagon_id, 
                            n1: "NO", 
                            n2: "NO", 
                            n3: "NO", 
                            n4: "NO", 
                            n5: "NO", 
                            n6: "NO"
                        }, 
                        on_conflict: {
                            constraint: clusters_hexagon_id_key, 
                            update_columns: [n1, n2, n3, n4, n5, n6, updated_at]
                        }
                    }
                }, 
                on_conflict: {constraint: hexagons_name_key, update_columns: is_active}) {
                returning {
                    is_active
                    name
                    id
                }
            }
        }
    '''
    variables = {
        "name": name,
        "hexagon_id": hexagon_id
    }
    response = run_query(query, variables)
    print(response)
    return response.get("insert_hexagons", "").get("returning", "")


def find_neighbours_by_name(name):
    query = '''
        query hexagons($name: String!) {
            hexagons(where: {name: {_eq: $name}, is_active: {_eq: "TRUE"}}) {
                hex {
                    n1
                    n2
                    n3
                    n4
                    n5
                    n6
                    hexagon_id
                }
            }
        }
    '''
    variables = {
        "name": name
    }
    response = run_query(query, variables)
    print(response)
    return response.get("hexagons", "")

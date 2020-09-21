
def logger(statement):
    print(f'\n\n{statement}\n\n')

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

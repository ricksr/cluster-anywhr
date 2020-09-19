def find_up(loc):
    return [loc[0], loc[1]-1, loc[2]+1]


def find_down(loc):
    return [loc[0], loc[1]+1, loc[2]-1]


def find_left_north(loc):
    return [loc[0]-1, loc[1], loc[2]+1]


def find_left_south(loc):
    return [loc[0]-1, loc[1]+1, loc[2]]


def find_right_north(loc):
    return [loc[0]+1, loc[1]-1, loc[2]]


def find_right_south(loc):
    return [loc[0]+1, loc[1], loc[2]-1]

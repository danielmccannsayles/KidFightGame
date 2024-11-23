def read_pos(str):
    poslist = str.split(",")
    return int(poslist[0]), int(poslist[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

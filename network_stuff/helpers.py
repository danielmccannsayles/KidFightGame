# Read position from a string
def read_pos(str_pos: str):
    print("splitting pos: ", str_pos)
    split_pos = str_pos.split(",")
    print("split pos: ", split_pos)
    return int(split_pos[0]), int(split_pos[1])


def make_pos(tup_pos: tuple):
    made_pos = str(tup_pos[0]) + "," + str(tup_pos[1])
    print("made pos ", made_pos)
    return made_pos

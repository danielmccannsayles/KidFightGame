import pygame as pg
import os

# Needed for relative import when developing (mac v. windows paths)
current_dir = os.path.dirname(__file__)


"""
WC: white character
BC:
WB: white base
BB: 
"""


class Piece:
    def __init__(self, size, type):
        match type:
            case "WC":
                img_path = f"{current_dir}/../../imgs/brutal-helm.png"
            case "BC":
                img_path = f"{current_dir}/../../imgs/orc-head.png"
            case "WB":
                img_path = f"{current_dir}/../../imgs/w_rook.png"
            case "BB":
                img_path = f"{current_dir}/../../imgs/b_rook.png"
            case _:
                print("invalid piece type")

        img = pg.image.load(img_path)
        img = pg.transform.scale(img, (size - 20, size - 20))
        self.img = img

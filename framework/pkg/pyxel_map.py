from dataclasses import dataclass
import pyxel
from typing import Callable
import PyxelUniversalFont as puf

from .pyxel_avatar import *
from .utils import *
import os
import shutil

# setting tile_code
TILE_CODE:dict = {
    "b":(25,28),
    "l":(24,28),
    "n":(31,22),
}
TILE_COLLISION:dict = {
    "@":True,
    "b":True,
    "l":False,
    "n":True,
}
TILE_CODE_REVERSE = {"":"@"}
def _hex(x:int) -> str:
    return "{:02X}".format(x)
for k, v in TILE_CODE.items():
    _code = _hex(v[0])+_hex(v[1])
    TILE_CODE[k] = _code
    TILE_CODE_REVERSE[_code] = k
    # print(TILE_CODE_REVERSE)

# initialize map
def _load_map(filename:str=".mymap_0"):
    filepath = get_data_path(f'data/map/{filename}')
    if not os.path.exists(filepath):
        shutil.copy(get_data_path('data/map/.base'), filepath)
    with open(get_data_path(f'data/map/{filename}'), 'r') as file:
        return file.read().split("\n")

def _update_edit_map(_MAP):
    with open(get_data_path(f'data/map/.edit'), 'w') as file:
        _map = "\n".join(_MAP)
        file.write(_map)
        
def _save_map(filename=".mymap_0"):
    shutil.copy(get_data_path('data/map/.edit'), get_data_path(f'data/map/{filename}'))

@dataclass
class RPGWindow:
    WIDTH:int = 16
    HEIGHT:int = 16
    BOTTOM:int = 2
    MAP_EDIT:bool = False
    SOURCE = get_data_path("data/img.pyxres")
    MESSAGE:str = ""
    MAP_ID:int = 0
    HIT:str = ""
    
    pyxel.init(WIDTH*8, (HEIGHT+BOTTOM)*8, title="PyxelRPG")
    # load data
    pyxel.load(SOURCE)
    
    def __init__(self) -> None:
        self.MAP = _load_map(f".mymap_{self.MAP_ID}")
        self._decode_map(self.MAP)
        self.SENSOR = []
    
    def draw(self,slide=(0,0)) -> None:
        pyxel.tilemap(0).set(16,0,self.DECODED_MAP)
        pyxel.bltm(0,0,0,16*8+slide[0],slide[1],self.WIDTH*8,self.HEIGHT*8)
        
    def _decode_map(self, _map):
        _data = []
        for line in _map:
            _line = ""
            for c in line.replace(" ", ""):
                _line += TILE_CODE[c]
            _data.append(_line)
        self.DECODED_MAP = _data
        
    def reload_map(self, map_name:str):
        self.MAP = _load_map(map_name)
        _update_edit_map(self.MAP)
        self._decode_map(self.MAP)
        
    def collision(self, position:list):
        x, y = (position[0]+3)//8, (position[1]+1)//8
        x2, y2 = (position[0]+12)//8, (position[1]+14)//8
        
        hit_count = 0
        self.SENSOR = []
        for _y in range(y,y2+1):
            for _x in range(x*4,x2*4+1,4):
                code = self.DECODED_MAP[_y][_x:_x+4]
                _tile = TILE_CODE_REVERSE[code]
                self.SENSOR.append(_tile)
                hit_count += TILE_COLLISION[_tile]
        return hit_count > 0
    
WINDOW = RPGWindow()
WRITER = puf.Writer("misaki_gothic.ttf")




def _key_to_number() -> int:
    if pyxel.btnp(pyxel.KEY_0):
        return 0
    if pyxel.btnp(pyxel.KEY_1):
        return 1
    if pyxel.btnp(pyxel.KEY_2):
        return 2
    if pyxel.btnp(pyxel.KEY_3):
        return 3
    if pyxel.btnp(pyxel.KEY_4):
        return 4
    if pyxel.btnp(pyxel.KEY_5):
        return 5
    if pyxel.btnp(pyxel.KEY_6):
        return 6
    if pyxel.btnp(pyxel.KEY_7):
        return 7
    if pyxel.btnp(pyxel.KEY_8):
        return 8
    if pyxel.btnp(pyxel.KEY_9):
        return 9
    return -1

# decorators
def map_reset(reset:Callable):
    def wrapper(self, *args, **kwargs) -> None:
        # initialize avatar
        self.avatar = Avatar()
        self.avatar.position = (8,8)
        avatar_editor.position = (16,8)
        reset(self,*args, **kwargs)
    return wrapper
        
def map_update(update:Callable):
    def wrapper(self, *args, **kwargs) -> None:
        if WINDOW.MAP_EDIT:
            if pyxel.btnp(pyxel.KEY_S):
                _save_map(f".mymap_{WINDOW.MAP_ID}")
                WINDOW.MAP_EDIT = False
        else:
            num_input = _key_to_number()
            if num_input >= 0:
                WINDOW.MAP_ID = num_input
                WINDOW.reload_map(f".mymap_{WINDOW.MAP_ID}")
            if WINDOW.collision(self.avatar.key_move()["position"]):
                WINDOW.HIT = [char for char in WINDOW.SENSOR if char != 'l'][0]
                self.avatar.position = self.avatar.preposition
            else:
                WINDOW.HIT = ""
        update(self,*args, **kwargs)
    return wrapper

def _next_tile(tile):
    tile_order = {
        "b": "l",
        "l": "b",
    }
    return tile_order[tile]

def map_draw(draw:Callable):
    def wrapper(self, *args, **kwargs) -> None:
        pyxel.cls(0)
        WINDOW.draw()
        draw(self, *args, **kwargs)
        
        if WINDOW.MAP_EDIT:
            pyxel.mouse(False)
            WINDOW.MESSAGE = "S: 保存 / M: 編集終了"
            hover_x, hover_y = pyxel.mouse_x//8*8, pyxel.mouse_y//8*8
            if hover_x < WINDOW.WIDTH*8 and hover_y < WINDOW.HEIGHT*8:
                pyxel.blt(hover_x,hover_y,0,240,248,8,8,11)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    _line = WINDOW.MAP[hover_y//8]
                    _tile = _line[hover_x//8]
                    WINDOW.MAP[hover_y//8] = _line[:hover_x//8] + _next_tile(_tile) + _line[hover_x//8+1:]
                    _update_edit_map(WINDOW.MAP)
                    WINDOW.reload_map(".edit")
        else:
            # draw avatar
            self.avatar.draw()
        WRITER.draw(4, WINDOW.WIDTH*8+4, WINDOW.MESSAGE, 8, 7)
    return wrapper
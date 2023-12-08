import pyxel
from .utils import *
from .pyxel_map import *
from .pyxel_avatar import *
from dataclasses import dataclass

@dataclass
class Params:
    pass

class App:
    def __init__(self, params:Params) -> None:
        self._reset(params)
        pyxel.run(self._update, self._draw)
    
    # initialize variables
    @map_reset
    def _reset(self, params:Params):
        self.params = params
        WINDOW.reload_map(".sample")
    
    # process
    @avatar_editor_update
    @map_update
    def _update(self):
        hit_info = WINDOW.HIT
        print(hit_info)
        tile, tile_pos = hit_info["tile"], hit_info["position"]
        
        if tile == "":
            WINDOW.MESSAGE = "PyxelRPGの世界へようこそ!"
            # WINDOW.MESSAGE = ""
        elif tile == "b":
            WINDOW.MESSAGE = f"ブロック({tile_pos[0]},{tile_pos[1]})に当たってるよ!"
        elif tile == "t":
            WINDOW.MESSAGE = f"宝箱({tile_pos[0]},{tile_pos[1]})をゲット！"
            WINDOW.change_tile(tile_pos, "l")
        elif tile == "@":
            WINDOW.MESSAGE = "この先は画面外みたい、、"
      
    # visualize
    @avatar_editor_draw
    @map_draw
    def _draw(self):
        pass
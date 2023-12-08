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
        if WINDOW.HIT == "":
            WINDOW.MESSAGE = "PyxelRPGの世界へようこそ!"
            # WINDOW.MESSAGE = ""
        elif WINDOW.HIT == "b":
            WINDOW.MESSAGE = "ブロックに当たってるよ!"
        elif WINDOW.HIT == "@":
            WINDOW.MESSAGE = "この先は画面外みたい、、"
      
    # visualize
    @avatar_editor_draw
    @map_draw
    def _draw(self):
        pass
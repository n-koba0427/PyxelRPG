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
        # initialize variables
        self._reset(params)
        # run app
        pyxel.run(self._update, self._draw)
    
    # initialize variables
    @map_reset
    def _reset(self, params:Params):
        self.params = params
        avatar_editor.position = (16,8)
    
    # process
    @avatar_editor_update
    @map_update
    def _update(self):
        if pyxel.btnp(pyxel.KEY_M):
             WINDOW.MAP_EDIT = not WINDOW.MAP_EDIT
        if pyxel.btnp(pyxel.KEY_R):
             WINDOW.reload_map(".base")
        print(WINDOW.HIT)
      
    # visualize
    @avatar_editor_draw
    @map_draw
    def _draw(self):
        WINDOW.MESSAGE = "E: キャラ編集 / M: マップ編集"
        if avatar_editor.flag:
            WINDOW.MESSAGE = "E: 編集終了"
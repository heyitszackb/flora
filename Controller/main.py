import pyxel
from Model.main import Model
from View.main import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self): # executed each frame
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.model.move_cursor(0,1)
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.model.move_cursor(0,-1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.model.move_cursor(1,0)
        if pyxel.btnp(pyxel.KEY_UP):
            self.model.move_cursor(-1,0)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.model.place_tile_at_cursor()
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.model.delete_tile_at_cursor()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.model.cycle_cursor_tile_type()
        if pyxel.btnp(pyxel.KEY_R):
            self.model.reset_garden()

        # increase the frame
        self.model.frame += 1
        self.model.update()



    def draw(self): # executed each frame
        self.view.render(self.model) # executed each frame
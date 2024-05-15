import pyxel
from Model.main import Model
from View.main import View
from ExportTool.main import ExportTool
from const import TileType

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.export_tool = ExportTool(save_directory="../save_files")

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

        # export functionality
        if pyxel.btnp(pyxel.KEY_E):
            print("exported")
            self.export_tool.export(self.model.garden)

        # load functionality
        if pyxel.btnp(pyxel.KEY_L):
            garden_state = self.export_tool.load()
            self.load_garden(garden_state)

        # increase the frame
        self.model.frame += 1
        self.model.update()

    def draw(self): # executed each frame
        self.view.render(self.model) # executed each frame

    def load_garden(self, garden_state):
        self.model.clear_garden()  # Reset the garden first
        size = garden_state["size"]
        tiles = garden_state["tiles"]
        for row in range(size):
            for col in range(size):
                for height, tile_type_name in enumerate(tiles[row][col]):
                    tile_type = TileType[tile_type_name]
                    self.model.cursor.position.set_position(row, col, height)
                    self.model.cursor.set_current_tile_type(tile_type)
                    self.model.place_tile_at_cursor()
        # self.model.cursor.position.set_position(0, 0, 1)
        self.model.cursor.set_current_tile_type(TileType.GRASS)
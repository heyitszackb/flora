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

    def update(self):
            self.handle_input()
            self.model.update()

    def handle_input(self):
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
        # if pyxel.btnr(pyxel.KEY_RETURN):
        #     print("Key up!")

        if pyxel.btnp(pyxel.KEY_E):
            self.export_tool.export(self.model.garden)
            print("Garden state saved.")

        if pyxel.btnp(pyxel.KEY_L):
            garden_state = self.export_tool.load()
            if garden_state:
                self.load_garden(garden_state)
                print("Saved garden state loaded.")

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
        self.model.cursor.set_current_tile_type(TileType.GRASS)
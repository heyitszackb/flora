import pyxel
from Model.main import Model, Position
from View.main import View
from Model.main import TileContent

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self): # executed each frame
        if pyxel.btnp(pyxel.KEY_RIGHT):
            # Remove the tile at the location of the cursor
            self.model.garden.remove_tile_from_stack(self.model.cursor.position.row,self.model.cursor.position.col)
            # Move the cursor
            self.model.cursor.move_col(1)
            self.model.cursor.move_to_top_of_stack()
            # Add a grass tile at the NEW location of the cursor
            self.model.garden.add_tile_to_stack(TileContent('g', self.model.cursor.position))
        if pyxel.btnp(pyxel.KEY_LEFT):
            # Remove the tile at the location of the cursor
            self.model.garden.remove_tile_from_stack(self.model.cursor.position.row,self.model.cursor.position.col)
            # Move the cursor
            self.model.cursor.move_col(-1)
            self.model.cursor.move_to_top_of_stack()
            # Add a grass tile at the NEW location of the cursor
            self.model.garden.add_tile_to_stack(TileContent('g', self.model.cursor.position))
        if pyxel.btnp(pyxel.KEY_DOWN):
            # Remove the tile at the location of the cursor
            self.model.garden.remove_tile_from_stack(self.model.cursor.position.row,self.model.cursor.position.col)
            # Move the cursor
            self.model.cursor.move_row(1)
            self.model.cursor.move_to_top_of_stack()
            # Add a grass tile at the NEW location of the cursor
            self.model.garden.add_tile_to_stack(TileContent('g', self.model.cursor.position))
        if pyxel.btnp(pyxel.KEY_UP):
            # Remove the tile at the location of the cursor
            self.model.garden.remove_tile_from_stack(self.model.cursor.position.row,self.model.cursor.position.col)
            # Move the cursor
            self.model.cursor.move_row(-1)
            self.model.cursor.move_to_top_of_stack()
            # Add a grass tile at the NEW location of the cursor
            self.model.garden.add_tile_to_stack(TileContent('g', self.model.cursor.position))
        if pyxel.btnp(pyxel.KEY_RETURN):
            # If we are on the top layer, we don't add the tile
            if self.model.cursor.position.height == 5:
                return
            # Move up the cursor
            self.model.cursor.move_height(1)
            # Add a tile at the cursor's new position
            self.model.garden.add_tile_to_stack(TileContent('g', self.model.cursor.position))
            self.model.garden.randomize_garden()
        
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            # If we are on the bottom layer, we don't delete the tile
            if self.model.cursor.position.height == 0:
                return
            # Remove the tile at the location of the cursor
            self.model.garden.remove_tile_from_stack(self.model.cursor.position.row,self.model.cursor.position.col)
            # move the cursor down in height
            self.model.cursor.move_height(-1)

    def draw(self): # executed each frame
        self.view.render(self.model) # executed each frame
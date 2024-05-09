import pyxel

from Model.main import Model
from Model.main import Tile
from Model.main import Cursor
from const import TileType

class View:
    def __init__(self):
        pyxel.init(200, 200)
        pyxel.load("../flora.pyxres")
        self.origin_x = 80
        self.origin_y = 60

        self.tile_height = 10
        self.tile_row_length = 16
        self.tile_col_length = 8

        self.tile_renderers = {
            TileType.GRASS: self.render_grass_tile,
            TileType.DIRT: self.render_dirt_tile,
            TileType.WATER: self.render_water_tile,
        }

    def update(self): # view update doesn't actually render anything, just necessary for INTERNAL VIEW LOGIC
        pass

    def render(self, model: Model): # this is the only function that actually renders things. Renders state based on internal logic of the view code (processed by the view update)
        pyxel.cls(0)
        render_list = self.collect_renderables(model)
        
        render_list.sort(key=lambda item: (item.position.row, item.position.col, item.position.height))

        for element in render_list:
            if isinstance(element, Tile):
                self.render_tile(element)
            elif isinstance(element, Cursor):
                self.render_cursor(element)
    
    def render_tile(self, tile: Tile):
        x, y = self.calc_xy(self.origin_x, self.origin_y,tile.position.row, tile.position.col,tile.position.height)

        render_func = self.tile_renderers.get(tile.get_type(), lambda x, y: None)
        render_func(x, y)
    def render_cursor(self, cursor: Cursor):
        x, y = self.calc_xy(self.origin_x, self.origin_y,cursor.position.row, cursor.position.col,cursor.position.height)
        pyxel.blt(x, y, 0, 64, 0, 32, 32, 8)
    
    # Add every render-able thing to the list
    def collect_renderables(self, model: Model):
        renderables = []
        # Add all tiles
        for row in model.get_garden().get_tiles():
            for stack in row:
                for tile in stack:
                    renderables.append(tile)

        # Add the cursor
        cursor = model.get_cursor()
        renderables.append(cursor)

        return renderables

    def render_grass_tile(self,x,y):
        pyxel.blt(x, y, 0, 0, 0, 32, 32, 8)

    def render_dirt_tile(self,x,y):
        pyxel.blt(x, y, 0, 32, 0, 32, 32, 8)
    
    def render_water_tile(self,x,y):
        pyxel.blt(x, y, 0, 0, 64, 32, 32, 8)

        # Helper to translate row/col/height to x/y for rendering
    def calc_xy(self, origin_x, origin_y, row, col, height):
        '''
        (x,y)
        When row  goes up by 1:
        row_offset_x -= 16
        row_offset_y += 8

        When col goes up by 1:
        col_offset_x += 16
        col_offset_y += 8

        When height goes up by 1:
        height_offset_x += 0
        height_offset_y -= 10
        '''

        row_offset_x = -self.tile_row_length*row
        row_offset_y = self.tile_col_length*row
        col_offset_x = col*self.tile_row_length
        col_offset_y = col*self.tile_col_length
        height_offset_x = 0
        height_offset_y = -self.tile_height*height # 10 is the height. It is not a multiple of 8 so that height layers can be better distinguished

        overall_x = origin_x + row_offset_x + col_offset_x + height_offset_x
        overall_y = origin_y + row_offset_y + col_offset_y + height_offset_y
        return overall_x, overall_y
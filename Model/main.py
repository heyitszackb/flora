import random
from const import TileType

class Position:
    def __init__(self, row=0, col=0,height=0):
        self.row = row
        self.col = col
        self.height = height

    # returns a NEW position object that can be used elsewhere.
    def get_new_position(self):
        return Position(self.row, self.col, self.height)
    
    def get_new_moved_position(self, drow=0, dcol=0, dheight=0):
        return Position(self.row + drow, self.col + dcol, self.height + dheight)

    def move(self, drow, dcol, dheight):
        self.row += drow
        self.col += dcol
        self.height += dheight
    
    def set_position(self, row, col, height):
        self.row = row
        self.col = col
        self.height = height

    #Establishes boundaries for the position
    def clamp(self, max_row, max_col, max_height):
        self.row = max(0, min(max_row, self.row))
        self.col = max(0, min(max_col, self.col))
        self.height = max(0, min(max_height, self.height))

class Tile:
    def __init__(self, position=None, tile_type=TileType.GRASS):
        self.tile_type = tile_type
        self.position = position if position else Position()

    def set_tile_type(self, tile_type: TileType):
        self.tile_type = tile_type
    
    def get_type(self):
        return self.tile_type

    def __str__(self):
        return f"{self.tile_type} at {self.position}"

class Garden:
    def __init__(self, size=5):
        self.tiles = [[[Tile(Position(row, col, 0))] for col in range(size)] for row in range(size)]
        self.size = size
        self.height_limit = 10
        self.depth_limit = 0

    def get_height_limit(self):
        return self.height_limit

    def get_depth_limit(self):
        return self.depth_limit
    
    def add_tile_to_stack(self, tile: Tile):
        self.tiles[tile.position.row][tile.position.col].append(tile)
    
    # takes a position object for simplicity - does nothing with the height information.
    def remove_tile_from_stack(self, position: Position):
        # If there is nothing in the stack, do nothing
        if len(self.tiles[position.row][position.col]) == 0:
            return
        self.tiles[position.row][position.col].pop()

    def get_tile(self, position: Position):
        return self.tiles[position.row][position.col][position.height]
    
    def get_stack(self, row, col):
        return self.tiles[row][col]
    
    def get_row(self, row):
        return self.tiles[row]
    
    def get_tiles(self):
        return self.tiles

    def __str__(self):
        return '\n'.join([' '.join([str(tile) for tile in row]) for row in self.tiles])

    def randomize_garden(self):
        size = len(self.get_tiles())  # Assuming square garden for simplicity
        for row in range(size):
            for col in range(size):
                current_stack_height = len(self.get_stack(row, col))
                # Random number of new grass blocks to add (between 1 and 3)
                num_new_blocks = random.randint(1, 3)
                for _ in range(num_new_blocks):
                    new_type = TileType.DIRT if random.random() < 0.1 else TileType.GRASS  # 10% chance for type 'd'
                    new_tile = Tile(Position(row, col, current_stack_height), new_type)
                    self.add_tile_to_stack(new_tile)
                    current_stack_height += 1
    
    def reset_garden(self):
        # delete all tiles and reset the garden to its original state
        self.tiles = [[[Tile(Position(row, col, 0))] for col in range(self.size)] for row in range(self.size)]

    
class Cursor:
    # garden is the garden to which this cursor is attached
    def __init__(self, garden: Garden, start_row=0, start_col=0, start_height=1):
        self.garden = garden
        self.position = Position(start_row, start_col, start_height)
        self.current_type = TileType.GRASS

    def get_current_tile_type(self):
        return self.current_type
    
    def set_current_tile_type(self, tile_type):
        self.current_type = tile_type

    def cycle_tile_type(self):
        # cycle between g, d, and w
        if self.current_type == TileType.GRASS:
            self.current_type = TileType.WATER
        
        elif self.current_type == TileType.WATER:
            self.current_type = TileType.GRASS

    def move(self, drow, dcol, dheight):
        self.position.move(drow, dcol, dheight)

        max_row = len(self.garden.get_tiles()) - 1
        max_col = len(self.garden.get_tiles()[0]) - 1
        max_height = self.garden.get_height_limit()

        self.position.clamp(max_row, max_col, max_height)
        
    def get_position(self):
        return self.position

    def move_to_top_of_stack(self):
        top = len(self.garden.get_stack(self.position.row, self.position.col))
        self.position.set_position(self.position.row, self.position.col, top)

    def __str__(self):
        return f"Cursor at {self.position}"
    

class Model:
    def __init__(self):
        self.garden = Garden()
        self.cursor = Cursor(self.garden)

    # move the cursor by drow and dcol with the tile that was at the cursor's position
    def move_cursor(self, drow: int, dcol: int):
        self.cursor.move(drow, dcol, 0)
        self.cursor.move_to_top_of_stack()

    # Places a tile a the cursor's position with the cursor's tile type
    def place_tile_at_cursor(self):
        if self.cursor.position.height >= self.garden.get_height_limit():
            return
        
        if self.cursor.get_current_tile_type() == TileType.GRASS and self.cursor.position.height != 0:
            if self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1)).get_type() == TileType.GRASS:
                # change it to dirt
                self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1)).set_tile_type(TileType.DIRT)
            
        # I do not like this line, but I need to create a new position in order to eliminate some awful bugs with shared positions
        self.garden.add_tile_to_stack(Tile(self.cursor.position.get_new_position(), self.cursor.get_current_tile_type()))
        # Move up the cursor
        self.cursor.move(0,0,1)
        
    # Deletes the tile at the cursor's position
    def delete_tile_at_cursor(self):
        # If we are on the bottom layer, we don't delete the tile
        if self.cursor.position.height <= self.garden.depth_limit:
            return
        
         # Remove the tile at the location of the cursor
        self.garden.remove_tile_from_stack(self.cursor.position.get_new_position())

        # move the cursor down in height
        self.cursor.move(0,0,-1)
        
        # When I delete a grass tile, if the tile under the cursor is dirt, it should be changed to grass.
        if self.cursor.position.height != 0:
            if self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1)).get_type() == TileType.DIRT:
                # change it to grass
                self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1)).set_tile_type(TileType.GRASS)


    def cycle_cursor_tile_type(self):
        # Change what the cursor places in the future
        self.cursor.cycle_tile_type()


    def reset_garden(self):
        # Reset the garden
        self.garden.reset_garden()

        # reset the cursor position
        self.cursor.position.set_position(0,0,1)
        # reset the cursor tile type
        self.cursor.set_current_tile_type(TileType.GRASS)


    def get_garden(self):
        return self.garden
    
    def get_cursor(self):
        return self.cursor

    def __str__(self):
        return str(self.garden) + '\n' + str(self.cursor)
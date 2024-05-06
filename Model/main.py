import random

class Position:
    def __init__(self, row=0, col=0,height=0):
        self.row = row
        self.col = col
        self.height = height

    def move(self, drow, dcol, dheight):
        self.row += drow
        self.col += dcol
        self.height += dheight

class TileContent:
    def __init__(self, tile_type='g', position=None):
        self.tile_type = tile_type
        self.position = position if position else Position()
    
    def get_type(self):
        return self.tile_type

    def __str__(self):
        return f"{self.tile_type} at {self.position}"

class Garden:
    def __init__(self, size=5):
        self.tiles = [[[TileContent('g', Position(row, col, 0))] for col in range(size)] for row in range(size)]
        self.height_limit = 5

    def get_height_limit(self):
        return self.height_limit
    
    # Needs to be fixed - the information is duplicated in the tile itself and then in the row/col...
    def add_tile_to_stack(self, tile: TileContent):
        self.tiles[tile.position.row][tile.position.col].append(tile)
    
    def remove_tile_from_stack(self, row, col):
        # If there is nothing in the stack, do nothing
        if len(self.tiles[row][col]) == 0:
            return
        self.tiles[row][col].pop()

    def get_tile(self, row, col, height):
        return self.tiles[row][col][height]
    
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
                    new_type = 'd' if random.random() < 0.1 else 'g'  # 10% chance for type 'd'
                    new_tile = TileContent(new_type, Position(row, col, current_stack_height))
                    self.add_tile_to_stack(new_tile, row, col)
                    current_stack_height += 1
    
class Cursor:
    # garden is the garden to which this cursor is attached
    def __init__(self, garden: Garden, start_row=1, start_col=0, start_height=0):
        self.garden = garden
        self.position = Position(start_row, start_col, start_height)

    # Relative to current position: Positive is up, negative is down
    def move_height(self, num_height_tiles):
        self.set_position(self.position.row, self.position.col, self.position.height + num_height_tiles)

    # Relative to current position: Positive is increasingm rows, negative is decreasing rows
    def move_row(self, num_row_tiles):
        self.set_position(self.position.row + num_row_tiles, self.position.col, self.position.height)

    # Relative to current position: Positive is increasingm cols, negative is decreasing cols
    def move_col(self, num_col_tiles):
        self.set_position(self.position.row, self.position.col + num_col_tiles, self.position.height)

    # Set position is what does all boundary checking for this function
    def set_position(self, row, col, height):
        max_row = len(self.garden.get_tiles()) - 1
        min_row = 0
        max_col = len(self.garden.get_tiles()[0]) - 1
        min_col = 0
        max_height = self.garden.get_height_limit()
        min_height = 0

        clamped_row = max(min_row, min(max_row, row))
        clamped_col = max(min_col, min(max_col, col))
        clamped_height = max(min_height, min(max_height, height))

        self.position = Position(clamped_row, clamped_col, clamped_height)
    
    def get_position(self):
        return self.position

    def move_to_top_of_stack(self):
        top = len(self.garden.get_stack(self.position.row, self.position.col))
        self.set_position(self.position.row, self.position.col, top)

    def __str__(self):
        return f"Cursor at {self.position}"
    

class Model:
    def __init__(self):
        self.garden = Garden()
        self.cursor = Cursor(self.garden)
    
    def place_tile(self, drow, dcol, dheight):
        tile = TileContent('g', Position(drow, dcol, dheight))
        self.garden.add_tile(tile, drow, dcol)

    def move_cursor(self, drow, dcol, dheight):
        self.cursor.move(drow, dcol, dheight)

    def cursor_position(self):
        return self.cursor.get_position()
    
    def get_garden(self):
        return self.garden
    
    def get_cursor(self):
        return self.cursor

    def __str__(self):
        return str(self.garden) + '\n' + str(self.cursor)
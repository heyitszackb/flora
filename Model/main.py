import random
from const import TileType

class Position:
    def __init__(self, row=0, col=0,height=0):
        self.row = row
        self.col = col
        self.height = height

    def get_new_position(self):
        """Returns a new Position object with the same coordinates."""
        return Position(self.row, self.col, self.height)
    
    def get_new_moved_position(self, drow=0, dcol=0, dheight=0):
        """Returns a new Position object moved by the specified deltas."""
        return Position(self.row + drow, self.col + dcol, self.height + dheight)

    def move(self, drow, dcol, dheight):
        self.row += drow
        self.col += dcol
        self.height += dheight
    
    def set_position(self, row, col, height):
        self.row = row
        self.col = col
        self.height = height

    def clamp(self, max_row, max_col, max_height):
        """Clamps the position within the specified boundaries."""
        self.row = max(0, min(max_row, self.row))
        self.col = max(0, min(max_col, self.col))
        self.height = max(0, min(max_height, self.height))

class Tile:
    def __init__(self, position=None, tile_type=TileType.GRASS):
        self.tile_type = tile_type
        self.position = position if position else Position()
        self.left_waterfall_height = 0 # the higher the number, the larger the waterfall on that side.
        self.right_waterfall_height = 0 # the higher the number, the larger the waterfall on that side.
        self.waterfall_height = 0 # The number of water tiles in this stack, including this one.

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

    # executed each frame
    def update(self):
        pass
    
    def update_waterfalls(self):
        for row in range(self.size):
            for col in range(self.size):
                stack = self.get_stack(row, col)

                for height in range(len(stack)):
                    
                    tile: Tile = stack[height]

                    tile.right_waterfall_height = 0  
                    tile.left_waterfall_height = 0

                    if tile.get_type() == TileType.WATER:
                        tile.waterfall_height = self.calculate_waterfall_height(row, col, height)
                        tile.left_waterfall_height = self.calculate_left_waterfall_height(row, col, height)
                        tile.right_waterfall_height = self.calculate_right_waterfall_height(row, col, height)

        

    def calculate_right_waterfall_height(self, row, col, height):
        # Update right waterfall
        final_height = 0
        num = 1
        loop = True
        while loop:
            # Ensure we're within bounds and not wrapping around
            if row - 1 >= 0 and len(self.get_stack(row - 1, col)) > height + num:
                if height < self.height_limit - 1 and self.get_tile(Position(row - 1, col, height + num)).get_type() == TileType.WATER:
                    final_height = num
                    num += 1
                else:
                    loop = False
            else:
                loop = False
        return final_height


    def calculate_left_waterfall_height(self,row, col, height):
         # Update left waterfall
        final_height = 0
        num = 1
        loop = True
        while loop:
            # Ensure we're within bounds and not wrapping around
            if col - 1 >= 0 and len(self.get_stack(row, col - 1)) > height + num:
                if height < self.height_limit - 1 and self.get_tile(Position(row, col - 1, height + num)).get_type() == TileType.WATER:
                    final_height = num
                    num += 1
                else:
                    loop = False
            else:
                loop = False
        return final_height


    def calculate_waterfall_height(self, row, col, start_height):
        stack = self.get_stack(row, col)
        height = 0
        for tile in stack[start_height:]:
            if tile.get_type() == TileType.WATER:
                height += 1
            else:
                break
        return height
                                
                    
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
        # delete all tiles and reset the garden to its original state (grass on bottom)
        self.tiles = [[[Tile(Position(row, col, 0))] for col in range(self.size)] for row in range(self.size)]

    def clear_garden(self):
        # clear all tiles, even grass on the bottom
        self.tiles = [[[] for _ in range(self.size)] for _ in range(self.size)]

    
class Cursor:
    # garden is the garden to which this cursor is attached
    def __init__(self, garden: Garden, start_row=0, start_col=0, start_height=1):
        self.garden = garden
        self.position = Position(start_row, start_col, start_height)
        self.current_type = TileType.GRASS
        self.current_num_frames_in_error_state = 0
        self.total_error_state_frames = 30
        self.in_error_state = False

    # update methods are called every frame
    def update(self):
        if self.in_error_state:
            self.current_num_frames_in_error_state += 1
            if self.current_num_frames_in_error_state >= self.total_error_state_frames:
                self.current_num_frames_in_error_state = 0
                self.set_error_state(False)
        

    def set_error_state(self, error_state):
        self.in_error_state = error_state

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
        self.frame = 0
    
    # runs each frame, is responsible for handling frame-by-frame model updates
    def update(self):
        self.frame += 1
        self.cursor.update()
        self.garden.update()


    # move the cursor by drow and dcol with the tile that was at the cursor's position
    def move_cursor(self, drow: int, dcol: int):
        self.cursor.move(drow, dcol, 0)
        self.cursor.move_to_top_of_stack()

    # Places a tile a the cursor's position with the cursor's tile type
    def place_tile_at_cursor(self):
        if self._is_tile_placement_valid():
            # change grass to dirt if placing grass on grass
            self._change_grass_to_dirt()
            new_tile = Tile(self.cursor.position.get_new_position(), self.cursor.get_current_tile_type())
            self.garden.add_tile_to_stack(new_tile)
            self.cursor.move(0, 0, 1)
            # Update the waterfall data
            self.garden.update_waterfalls()
        else:
            self.cursor.set_error_state(True)

    def _is_tile_placement_valid(self) -> bool:
        # We can't build outside of the garden
        if self.cursor.position.height >= self.garden.get_height_limit():
            return False
        # We can't place a grass tile on top of a water tile if we aren't placing water too
        if self.cursor.get_current_tile_type() != TileType.WATER and self.cursor.position.height != 0:
            below_tile_type = self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1)).get_type()
            if below_tile_type == TileType.WATER:
                return False
        return True

    def _change_grass_to_dirt(self):
        # if we are placing on grass and we are not on the bottom layer, change the tile under it to dirt
        if self.cursor.get_current_tile_type() == TileType.GRASS and self.cursor.position.height != 0:
            below_tile = self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1))
            if below_tile.get_type() == TileType.GRASS:
                below_tile.set_tile_type(TileType.DIRT)
        

    def delete_tile_at_cursor(self):
        if self._is_deletion_valid():
            # Delete the tile at the cursor position
            self.garden.remove_tile_from_stack(self.cursor.position.get_new_position())
            # Move cursor down
            self.cursor.move(0, 0, -1)
            # if there is dirt exposed now, change it to grass
            self._change_dirt_to_grass()
            # update data
            self.garden.update_waterfalls()
        else:
            self.cursor.set_error_state(True)

    # conditions that need to be met for tile deletion to be valid
    def _is_deletion_valid(self):
        return self.cursor.position.height > self.garden.depth_limit

    def _change_dirt_to_grass(self):
        if self.cursor.position.height != 0:
            below_tile = self.garden.get_tile(self.cursor.position.get_new_moved_position(dheight=-1))
            if below_tile.get_type() == TileType.DIRT:
                below_tile.set_tile_type(TileType.GRASS)

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

    # TODO: maybe make this function a modified reset_garden with a clear=True flag...?
    def clear_garden(self):
        # Clear the garden
        self.garden.clear_garden()

        # reset the cursor position
        self.cursor.position.set_position(0,0,0)
        # reset the cursor tile type
        self.cursor.set_current_tile_type(TileType.GRASS)


    def get_garden(self):
        return self.garden
    
    def get_cursor(self):
        return self.cursor

    def __str__(self):
        return str(self.garden) + '\n' + str(self.cursor)
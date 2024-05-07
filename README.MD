# The boundaries of the garden need to only be in the garden (not the cursor too, as it currently is...)

# Check to make sure each class actually has things that only that class needs and nothing else

# TODO: Position move function doesn't really do anything...but should probably handle position related logic.

# Add "r" to reset the garden

# TODO: Understand how the render_list sorting works. Can I modify to understand it better?

# TODO: Refactor the moving and carrying the tile accross the board logic in this file

# Add undo action stack

# TODO: Check cursor movement bounds.

# TODO: Block about to be placed should probably be some greyscale version of the real one?

# TODO: Add rotation of the entire table

# Terminology

drow is row difference
dcol is col difference
dheight is height difference
dx is x difference
xy is y difference

MOVE implies relative
e.g. move_cursor_with_tile
SET implies placing at coords, regardless of current position
e.g. set_cursor_with_tile

Another example:
def move_col(self, dcol):
self.set_position(self.position.row, self.position.col + dcol, self.position.height)

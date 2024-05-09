# FIX the position logic and move to Position - should NOT be in cursor at all.

# Think about data structure that is holding the tiles. I could potentially refactor it to make expanding better. But also, it is nice to have it simple.

# Check to make sure each class actually has things that only that class needs and nothing else

# TODO: Position move function doesn't really do anything...but should probably handle position related logic.

# Add "r" to reset the garden

# TODO: Understand how the render_list sorting works. Can I modify to understand it better?

# Add undo action stack

# TODO: Block about to be placed should probably be some greyscale version of the real one?

# TODO: Add rotation of the entire table

# Terminology

drow is row difference
dcol is col difference
dheight is height difference
dx is x difference
xy is y difference

MOVE implies relative
SET implies placing at coords, regardless of current position

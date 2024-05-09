# Thought: Switch to a 16x16 tile design for simplicity and cuteness?

# I really need a way to save and load past creations

# Add waterfall animation for water blocks

# New goals:

# Add grass growing slowly over time, randomly, to simulate an evolving environment.

# Swap tileset.

# Add frames to the model and try to add one thing of animation to the view.

# Think about data structure that is holding the tiles. I could potentially refactor it to make expanding better. But also, it is nice to have it simple.

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

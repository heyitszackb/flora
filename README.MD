# Core thing:

The experience should be incredibly intuitive, and incredibly EASY to operate. (like, only 1, MAYBE 2 buttons total)
The experience should be incredibly beautiful at every single frame (i.e. no complicated graphics of metrics/numbers or clutter).
Every frame should be a peice of art from beginning to end.

Thoughts: Focus on core mechanics and build out from there. I shouldn't spend my time doing random things all the time trying to make things work.

# NEXT UP

Review following changes for clean code refactor:
(TODO: need to clear if tile is placed on top of them)
strawberry patch
lily pads

cursor error state

update function in model

place_tile_at_cursor additions

# Currently, all time-based things are based on frames (error checking, etc).

I feel like this could be a problem because if something is computationally intensive, it might slow everything down...

# Add view for current tile that is being placed from the cursor

# Add houses, tents, etc

# Multi-player functionality?

This could be done by having one player responsible for things like flora, and the other for

Done

# I really need a way to save and load past creations

# Each frame, there is a tiny tiny chance that one of the grass tiles grows a strawberry patch.

# if there is a 3+ block high waterfall, there should be a splash animation!

# starberry patches only form on lower levels of ground?

# strawberry patches should form in clusters

# Only allow 1 or 2 lilypads in an area at a time.

# Add seasons??

# Lily pads might grow on water in ponds

# Clouds scrolling past

# Birds

# Stone under the dirt like minecraft at a certain depth

# New goals:

# Add grass growing slowly over time, randomly, to simulate an evolving environment.

# Swap tileset.

# Add frames to the model and try to add one thing of animation to the view.

# Think about data structure that is holding the tiles. I could potentially refactor it to make expanding better. But also, it is nice to have it simple.

# TODO: Understand how the render_list sorting works. Can I modify to understand it better?

# Add undo action stack

# TODO: Block about to be placed should probably be some greyscale version of the real one?

# Add sounds/music

# TODO: Add rotation of the entire table

# Have a tutorial

# Far future: City version

# Perhaps should primarily be an art/zen/relaxation/creative outlet. Can add other game modes on top for fun.

# Can have an arcade mode where two people are trying to be the most creative with the given prompt

# Terminology

drow is row difference
dcol is col difference
dheight is height difference
dx is x difference
xy is y difference

MOVE implies relative
SET implies placing at coords, regardless of current position

# Design Document

## Core Philosophy

-   **Simple**: The experience should be incredibly easy to operate, ideally using only 1 or maybe 2 main buttons in total.
-   **Beautiful**: Every frame should be beautiful, serving as a standalone piece of art from beginning to end without cluttered graphics, metrics, or numbers.
-   **User control**: The user should be able to control as much as possible about the scene they are creating (i.e. reduce randomness)

An ideal feature addition is a feature that increases simplicity, beauty, or user control without detracting from the other two.

## Current Tasks

-   Remove gridlines from water (increase beauty)
-   Add splash animation for water (increase beauty)

## Future Ideas / Backlog

### Environment and Animations

-   **Dynamic Environment**:
    -   Consider adding seasons to change the environment dynamically.
    -   Implement slow grass growth to simulate an evolving landscape.
    -   Add animals
    -   Add time of day
-   **Animations**:
    -   Implement splash animations for waterfalls that are 3+ blocks high.
    -   Make water less grid-like
    -   Add moving clouds, flying birds, and other ambient animations to enrich the environment.
    -   Using pget and pset, perhaps add some type of shadows based on time of day or clouds passing overhead or even more advanced shadow calculations based on flora or animals.

### Game Modes

-   **Single Player**
    -   Level system where users have a limited number of blocks to build a scene and as they progress they get access to more and more to build beautiful things
    -   Timed challenges where users have x amount of time to build a scene from a given prompt (i.e. "Twin waterfall", "hidden marsh", "secret valley", etc)
    -   Have a tutorial flow to introduce users to the game mechanics, showing examples, and showing small 3x3 plots to get basic point across slowly.
    -   Art/Zen/Relaxation Mode: Focus on creative expression and relaxation.
-   **Multiplayer**
    -   One player manages flora and another manages different aspects, enhancing cooperative gameplay.
    -   Race mode where players are side by side competing in a timed match
    -   Create Together - There are two cursors in the same map and players can build together on once project
    -   Art/Zen/Relaxation Mode: Focus on creative expression and relaxation.

### Other Features

-   Undo action stack to allow players to revert changes.
-   Rotate entire screen to shift tiles
-   Transition from frame-based timing to potentially time-based checks to avoid slowdowns in computationally intensive scenarios.
-   Add Houses/tents/castles? Not sure how to make this 'simple' for users.

### User Interface

-   Add a view to show the current tile being placed from the cursor.
-   Indicate errors through the cursor’s error state more effectively (sound/blinking?)

### Sound and Music

-   Integrate sounds and music to enhance the immersive experience of the game.

## Terminology In Codebase

-   **Movement Terms**:
    -   `drow`, `dcol`, `dheight`: Denote differences in row, column, and height respectively. All are ints
    -   `row`, `col`, `height`: Denote a row, column, and height. All are ints.
    -   `dx`, `dy`: Used to denote differences in x and y coordinates. All are ints.
    -   `MOVE`: Implies relative movement.
    -   `SET`: Indicates placing at specific coordinates, regardless of current position.
    -   `update()`: Each class' update method will, by convention of the codebase, be executed each frame.

---

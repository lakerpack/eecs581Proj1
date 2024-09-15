# Battleship Game Code Documentation

## Overview
The Battleship game is a two-player strategy game implemented in Python using the pygame library. The objective is to guess the locations of your opponent's ships on a 10x10 grid. Players take turns placing their ships and then attempt to sink the opponent's fleet by guessing their positions.

Key Features:
- Player vs. Player gameplay
- Interactive ship placement with rotation and validation checks
- Turn-based grid-based guessing system

## Code Structure

### 1. `Player` Class
- **Purpose:** Represents a player in the game, handling their board setup and guesses.
- **Attributes:**
  - `num`: Player number (1 or 2).
  - `board`: A 10x10 grid representing the player's ship placement.
  - `guesses`: A 10x10 grid representing the player's guesses on the opponent's board.
  - `ships`: dict of ships that the player has placed. Also holds # of times each of their ships have been hit
  - `sunk_ships`: dict of the player's own ships that have been sunk. Ships are marked `True` if sunk or `False` if not sunk
- **Methods:**
  - `place_ship(x, y, size, direction)`: Places a ship on the board based on the given coordinates, size, and direction. Returns `True` if successful, `False` otherwise.
  - `check_hit(self, enemy, x, y)`: checks for a hit on the enemy ship. Also checks for if a ship is sunk. Calls function `mark_ship_as_sunk(self, currentPlayer, ship_size)`: if a ship is sunk. Otherwise will mark a ship as a hit or miss, returning `True` or `False` as well as changing some counts depending on a hit or miss.
  - `mark_ship_as_sunk(self, currentPlayer, ship_size)`: if a ship has been sunk, update the enemy's list of their own ships that have been sunk, as well as marking the current player's guesses to be `sunk` instead of `hit`

### 2. `getCount(screen)`
- **Purpose:** Displays the initial screen where players select the number of ships (1-5).
- **Details:** Renders text prompts and handles input for selecting the number of ships. Uses arrow keys for adjustment and Enter to confirm.

### 3. `drawLabels(screen, xOffset, yOffset)`
- **Purpose:** Draws grid labels (A-J for columns, 1-10 for rows) on the screen.
- **Details:** Centers labels along the X and Y axes relative to the grid placement.

### 4. `startBoard(screen, count, player)`
- **Purpose:** Manages the ship placement phase for the specified player.
- **Details:** Allows the player to position ships on the grid, highlighting potential placements and enforcing boundary constraints.

### 5. `drawBoard(screen, player)`
- **Purpose:** Draws the current state of both the player's board and their guesses on the opponent's board as well as hits, misses, and ships sunk on their own board.
- **Details:** Displays hits, misses, ships sunk, and ship placements using color-coded squares.

### 6. `handlePlayerTurn(screen, currentPlayer, enemy)`
- **Purpose:** Handles a player's turn, updating the game state based on their actions.
- **Details:** Allows the current player to make a guess on the opponent's grid and updates the display.

### 7. `check_for_win(player)`
- **Purpose:** Checks to see if the current player has won based on if all of the enemy's ships have been sunk
- **Details:** Allows for a player to win and for the game to be ended once all of their opponent's ships have been sunk

### 8. `main()`
- **Purpose:** Main game loop that initializes the game, manages turns, and handles game state transitions.
- **Details:** Sets up the game screen, initializes player objects, and runs the gameplay loop.

## Game Flow

1. **Initialization:** The `main()` function initializes the Pygame screen, sets up the players, and begins the ship placement phase.
2. **Ship Placement:** Each player takes turns placing their ships using the `startBoard()` function, which checks for valid placements.
3. **Gameplay Loop:** Players alternate turns managed by `handlePlayerTurn()`, making guesses on the opponent’s grid.
4. **Display Updates:** After each action, `drawBoard()` updates the screen to reflect the current game state, showing hits and misses, as well as ships being sunk.
5. **End Game:** The game continues until one player sinks all of the opponent's ships. The code does not yet include an explicit end-game state, but this can be added as a future improvement.

"""
Name: Battleship
Description: An implmentation of battleship that follows the guidelines outlined in the rubric. 
Players will determine how many ships at the start, and will guess ships on the enemy's board, switching after each guess.
Inputs: Number of battleships, Rotation/Alignment of ship placement, Where to hit a ship
Output: A functional battleship game that ends after all ships of one side has been sunk. 
Other Sources: N/A (edit this if you have any Nathan)
Author(s): Anil Thapa, Michelle Chen, Nathan Bui
Creation Date: 09/13/2024
"""

import sys
import pygame # (A) module that provides a GUI library we use as the primary runner of the game

FPS = 30 # (A) global var to determine refresh rate of the game 
ROWS, COLS = 10, 10 # (A) how many blocks in the rows and cols will be used to calculate positionings (10x10 is standard battleship)
BLOCKHEIGHT, BLOCKWIDTH = 30, 30 # (A) height of each block for the board 
GAMEHEIGHT, GAMEWIDTH = 700, 600 # (A) height/width of the actual game window 

SHIPCOLORS = {1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255), 4: (255, 255, 100), 5: (255, 100, 255)} # (A) global colors for different type of ships

class Player: # stores the data for each player so we can alternate easily with each turn based on the Player data
    def __init__(self, num): # (A) initialization
        self.num = num # (A) player num to keep track of who's who  without anything fancy 
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)] # (A) initialize player's matrix based on game board to reflect ship states
        self.guesses = [[0 for _ in range(COLS)] for _ in range(ROWS)] # (A) similarly, a matrix to reflect guesses on the enemy that are accurate/misses
        self.ships = {} #n
        self.sunk_ships = {} #n
    
    def place_ship(self, x, y, size, direction): # (A) return if valid placement based on player's board 
        if direction == 0: # (A) refers to the current direction being used in the start screen that was passed through (0 is to the right)
            if x + size > COLS: # (A) too large for the board
                return False # (A) not a valid move
            for i in range(size): # (A) now if not too large, we must calculate if there are any collisions with other placements
                if self.board[y][x + i] != 0: # (A) if not 0 so not free in the path of placement...
                    return False # (A) then this is not a valid move 
            for i in range(size): # (A) otherwise, replace the path with ships of size
                self.board[y][x + i] = size # (A) important to set nodes in the path to 'size' because that will distinguish different ships 
        elif direction == 1: # (A) similarly, refer to the above; direction == 1 means it is a path pointing down 
            if y + size > ROWS: 
                return False
            for i in range(size):
                if self.board[y + i][x] != 0:
                    return False
            for i in range(size):
                self.board[y + i][x] = size
        elif direction == 2: # (A) refer to above, direction == 2 means it is a path pointing to the left
            if x - size + 1 < 0: # (A) distinction between this conditinoal and the above is that 0 can be valid, but ROWS/COLS cannot hence the + 1 
                return False
            for i in range(size):
                if self.board[y][x - i] != 0:
                    return False
            for i in range(size):
                self.board[y][x - i] = size
        elif direction == 3: # (A) refer to above, direction == 3 means it is a path pointing to the top 
            if y - size + 1 < 0: # (A) same explanation as direction == 2 for this conditional
                return False
            for i in range(size):
                if self.board[y - i][x] != 0:
                    return False
            for i in range(size):
                self.board[y - i][x] = size

        if size not in self.ships: #n
            self.ships[size] = 0
            self.sunk_ships[size] = False
        return True

    def check_hit(self, enemy, x, y):  # n
        if enemy.board[y][x] > 0:
            ship_size = enemy.board[y][x]
            self.guesses[y][x] = 'hit'
            enemy.ships[ship_size] += 1
            if enemy.ships[ship_size] == ship_size and not enemy.sunk_ships[ship_size]:
                enemy.mark_ship_as_sunk(self, ship_size)
            return True
        else:
            self.guesses[y][x] = 'miss'
            return False

    def mark_ship_as_sunk(self, currentPlayer, ship_size): #n
        self.sunk_ships[ship_size] = True
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x] == ship_size:
                    currentPlayer.guesses[y][x] = 'sunk'


def getCount(screen): # (M) initial screen that determines how many ships the players will deal with
    font = pygame.font.Font(None, 36) # (M) setting the font is an initialization of pygame.font.Font(file, size) where file is if there's already a font type, and size is just the Size
    titleFont = pygame.font.Font(None, 48) # (M) need to initialize different fonts if we want different sizes for readaability 
    smallFont = pygame.font.Font(None, 24) # (M) as above, these fonts will be used for different words/phrases and the size reflects that
    
    title = titleFont.render("Battleship", True, (5, 5, 5)) # (M) titleFont refers to the font initialized earlier
    prompt = font.render("How many ships would you like? (1-5)", True, (5, 5, 5)) # (M) font.render(phrase, antialiasing, color, background) is self explanatory (background is not mandatory)
    startText = font.render("Press ENTER to start", True, (5, 5, 5)) # (M) by rendering, it's drawing these texts on the surface or "screen" we passed in earlier 
    disclaimer = smallFont.render("Use the up and down arrows to adjust the # of ships", True, (5, 5, 5))

    ship_count = 1 # (M) minimum number of ships we can play with is one
    running = True # (M) conditional for the game loop to continue 
    
    while running: # (M) this loop is necessary so the player can input their decisions without it going straight to the next screen
        screen.fill("skyblue") # (M) fill the background with skyblue
        
        screen.blit(title, (GAMEWIDTH//2 - title.get_width()//2, 100)) # (M) place a rendered object on top of the screen, in this case our texts
        screen.blit(prompt, (GAMEWIDTH//2 - prompt.get_width()//2, 200)) # (M) this will make the texts visible, and takes in x, y parameters 
        screen.blit(startText, (GAMEWIDTH//2 - startText.get_width()//2, 400)) # (M) GAMEWIDTH // 2 - text.get_width() // 2 helps center in the horizontal plane
        screen.blit(startText, (GAMEWIDTH//2 - startText.get_width()//2, 400)) # (M) vertical placement is subjective, so we just pick whatever looks appealing
        screen.blit(disclaimer, (GAMEWIDTH//2 - disclaimer.get_width()//2, 450)) # (M) placing another text onto the screen

        count_text = font.render(str(ship_count), True, (5, 5, 5)) # (M) new text to render inside the loop because it's dependent on the count of what the user has chosen
        screen.blit(count_text, (GAMEWIDTH//2 - count_text.get_width()//2, 300)) # (M) we will still need to place this to the top of the screen
                
        pygame.display.flip() # (M) pygame.display.flip() will update the screen with the newly placed objects
        
        for event in pygame.event.get(): # (M) gameplay loop for listening to inputs within the game
            if event.type == pygame.QUIT: # (M) if you close out, this is a pygame.QUIT event and ends the screen/game 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # (M) keydown refers to the act of pushing any key down, not just the down key 
                if event.key == pygame.K_UP: # (M) if this is going up, then user wants more ships
                    ship_count = min(ship_count + 1, 5) # (M) however, max count is 5, so if the user wants more than 5, just take the 5 which will be the min
                elif event.key == pygame.K_DOWN: # (M) likewise if this goes down, the user wants less ships
                    ship_count = max(ship_count - 1, 1) # (M) but ship count is lower bound by 1 
                elif event.key == pygame.K_RETURN: # (M) if user presses enter, then we are good to send the ship count back
                    return ship_count # (M) this allows for the shipcount to be sent back to main() and get used by game for selection and gameplay
    
    return ship_count # (M) if the running is broken in any way, default is 1


def drawLabels(screen, xOffset, yOffset): # (M) function to just draw labels on the board as required by the rubric, offsets are so it does not collide with board
    font = pygame.font.Font(None, 26) # (M) font object initialization, with a None reference to any existing font, and 26 as the size 
    for i in range(COLS): # (M) for every column...
        label = font.render(chr(65 + i), True, (5, 5, 5)) # (M) have a font render itself on the screen, starting with chr(65+i) which starts as A
        screen.blit(label, (xOffset + i * BLOCKWIDTH + BLOCKWIDTH // 2 - label.get_width() // 2, yOffset - 25)) # (M) push this rendered font to the top of the screen, and space it out on the side with i * BLOCKWIDTH
    
    for i in range(ROWS): # (M) for every row... 
        label = font.render(str(i + 1), True, (5, 5, 5)) # (M) have the font render itself, this time just str() to convert the numbers into a string
        screen.blit(label, (xOffset - 25, yOffset + i * BLOCKHEIGHT + BLOCKHEIGHT // 2 - label.get_height() // 2)) # (M) push again to the to pof the screen with blit and space it out with i * BLOCKHEIGHT


def startBoard(screen, count, player): # (A) startboard will have the user (current player) set up their board based on the count given
    lineColor = (255, 255, 255) # (A) color for the grid/matrix lines; should be (255, 255, 255) or white
    yOffset = 150 # (A) offset to place the board in the middle of the game screen
    xOffset = 150 # (A) same offset but x-direction

    font = pygame.font.Font(None, 36) # (A) create a font object with 36 size font
    smallFont = pygame.font.Font(None, 16) # (A) create another font object but with 16 for small disclaimers
    title = font.render(f"Place Your Ships Player {player.num}", True, (5, 5, 5)) # (A) render the title, note it uses the player.num we initialized Player() with
    instruction = smallFont.render("Press R to rotate your placement. Click to place a ship.", True, (5, 5, 5)) # (A) disclaimer on how to rotate and place ships

    ships = [val + 1 for val in range(count)] # (A) rubric outlines each ship has a val of their count equivalent so [1,2,3.. etc.]
    currentShip = ships.pop() # (A) we pop the last ship or highest value to start placements with
    direction = 0 # (A) direction by default is 0 which is right-facing

    waiting = True # (A) function loop conditional so it doesn't instantly move away from this screen
    while waiting: # (A) will wait for inputs
        screen.fill("skyblue") # (A) background will be skyblue 
        screen.blit(title, (GAMEWIDTH // 2 - title.get_width() // 2, yOffset - 75)) # (A) push the rendered title to the top of the screen with screen.blit()
        screen.blit(instruction, (GAMEWIDTH // 2 - instruction.get_width() // 2, yOffset + 315)) # (A) same with the disclaimer, GAMEWIDTH // 2 - instruction.get_width() // 2 will just center the text

        drawLabels(screen, xOffset, yOffset) # (A) draw labels on the board as well for clarity, provide offsets to account for different scenarios

        mouseX, mouseY = pygame.mouse.get_pos() # (A) pygame.mosue.get_pos() returns (x, y) of the mouse position
        hoverX = (mouseX - xOffset) // BLOCKWIDTH # (A) we disregard the part that the offset adds, then divide by WIDTH to take the board position (1-10)
        hoverY = (mouseY - yOffset) // BLOCKHEIGHT # (A) similar to above, we take the Y position that is normalized

        for x in range(COLS): # (A) iterate through each column
            for y in range(ROWS): # (A) iterate through each row as well to work with specific blocks of the matrix
                pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + yOffset, BLOCKWIDTH, BLOCKHEIGHT) # (A) rectangle tuple that replaces a rectangle object with (x, y, width, height)
                
                should_highlight = False # (A) variable to determine if we should highlight the current square in the loop
                if 0 <= hoverX < COLS and 0 <= hoverY < ROWS: # (A) for one, it is mandatory to be within the board to even highlight
                    if direction == 0 and hoverY == y and hoverX <= x < hoverX + currentShip and hoverX + currentShip <= COLS: # (A) now we figure out based on the direction (0 = right), is the currentNode covered by the path starting from the block the mouse points at
                        should_highlight = True # (A) if direction == 0, then if node falls within the bounds of the path, (hoverX <= x < hoverX + currentShip) and also not out of bound (hoverX + currentShip <= COLS)
                    elif direction == 1 and hoverX == x and hoverY <= y < hoverY + currentShip and hoverY + currentShip <= ROWS:
                        should_highlight = True # (A) similar logic to above, but direction == 1 is down, so check if y falls under that y path while not going out of bound
                    elif direction == 2 and hoverY == y and hoverX - currentShip < x <= hoverX and hoverX - currentShip + 1 >= 0: # (A) similar logic to above, direction 2 == left
                        should_highlight = True # (A) one thing to note is that hoverY == y just means same row or same col depending on the direction of the path (if right, then col should be same)
                    elif direction == 3 and hoverX == x and hoverY - currentShip < y <= hoverY and hoverY - currentShip + 1 >= 0: # (A) similar logic to above, direction 3 == top
                        should_highlight = True

                if should_highlight: # (A) if we should highlight this block
                    pygame.draw.rect(screen, (155, 155, 155), pyRect) # (A) then instead of a normal color we draw a gray block, but has a pink tone thanks to the background
                elif player.board[y][x] != 0: # (A) if the block isn't even empty, e.g. it has a ship
                    ship_size = player.board[y][x] # (A) find the type of ship/ship size by checking the player's board 
                    ship_color = SHIPCOLORS.get(ship_size, (0, 255, 0)) # (A) get the color corresponding to the type of ship
                    pygame.draw.rect(screen, ship_color, pyRect) # (A) draw the block with the ship's color
                
                pygame.draw.rect(screen, lineColor, pyRect, 1) # (A) this draws the grid, the extra parameter at the end determines if it's 'hollow' and has a border strength

        # print(hoverX, hoverY)
        pygame.display.flip() # (A) then update the display so all the little color changes happen simutaneously

        for event in pygame.event.get(): # (A) listen for events in the game
            if event.type == pygame.QUIT: # (A) if quit (x out) then quit the game
                pygame.quit()
            elif event.type == pygame.KEYDOWN: # (A) pygame.KEYDOWN means that the user pressed down a key, nothing specific here
                if event.key == pygame.K_r: # (A) specifically, if it is the R key (pygame.K_r) then rotate the ship by changing the direction
                    direction = (direction + 1) % 4 # (A) this will just cycle within the (0-3) range by using modulo 4
            elif event.type == pygame.MOUSEBUTTONDOWN: # (A) if the mouse was clicked
                if event.button == 1: # (A) and the mouse click was the left click
                    if 0 <= hoverX < COLS and 0 <= hoverY < ROWS: # (A) first check the bounds of the click to make sure it was valid
                        if player.place_ship(hoverX, hoverY, currentShip, direction): # (A) then see if you can place the ship within the player object's matrix
                            if ships: # (A) if there are more ships to place
                                currentShip = ships.pop() # (A) pop the next ship and repeat the loop
                            else:
                                waiting = False # (A) break the loop otherwise


def drawBoard(screen, player, enemy): # (M) function that draws the board in the main game loop
    lineColor = (255, 255, 255) # (M) color of the lines 
    topOffset = 30 # (M) offset we add so the column labels don't go off the screen for the top board 
    bottomOffset = 400 # (M) bottom offset to push the bottom board down 
    xOffset = 150 # (M) horizontal offset to center the boards

    drawLabels(screen, xOffset, topOffset) # (M) draw labels on the top board
    for x in range(COLS): # (M) iterate through each column
        for y in range(ROWS): # (M) iterate through each row
            pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + topOffset, BLOCKWIDTH, BLOCKHEIGHT) # (M) create a tuple for the rectangle object (x, y, width, height)
            pygame.draw.rect(screen, lineColor, pyRect, 1) # (M) at the same time, we draw the grids for the board 
            if player.guesses[y][x] != 0: # (M) if the guess board does not have 0 at the guess matrix, it has one of 3 conditions
                if player.guesses[y][x] == 'hit': # (M) the guess was a hit
                    pygame.draw.rect(screen, (255, 0, 0), pyRect) # (M) draw red on the spot for a hit
                elif player.guesses[y][x] == 'miss': # (M) the guess was a miss
                    pygame.draw.rect(screen, (0, 0, 255), pyRect) # (M) draw blue on the spot for a miss
                elif player.guesses[y][x] == 'sunk':  # n
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)

    drawLabels(screen, xOffset, bottomOffset) # (M) now draw the labels but on the bottom board, so we use bottom offset
    for x in range(COLS): # (M) iterate through all the columns and rows again
        for y in range(ROWS):
            pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + bottomOffset, BLOCKWIDTH, BLOCKHEIGHT) # (M) same as above, we create a tuple for the rectangle (x, y, width, height)
            pygame.draw.rect(screen, lineColor, pyRect, 1) # (M) and just like with the top board, draw the grids for the board
            if player.board[y][x] != 0: # (M) since this is the player's board, we check the matrix to see if there are any ships at the spot
                ship_size = player.board[y][x] # (M) get the type of ship from the player's board
                ship_color = SHIPCOLORS.get(ship_size, (0, 255, 0)) # (M) get the type of color from matching it to the global colors
                pygame.draw.rect(screen, ship_color, pyRect) # (M) draw the colored square onto the board
            if enemy.guesses[y][x] != 0:
                if enemy.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)
                elif enemy.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif enemy.guesses[y][x] == 'sunk': #n
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)


def handlePlayerTurn(screen, currentPlayer, enemy): # (N)
    waiting_for_input = True # (A) wait for input so the screen doesn't instantly move
    x_offset = 150 #n
    y_offset = 30
    font = pygame.font.Font(None, 36)
    while waiting_for_input: # (A) input waiting loop
        drawBoard(screen, currentPlayer, enemy) # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        pygame.display.flip() # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None, None 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    #n
                    mouseX, mouseY = pygame.mouse.get_pos()

                    gridX = (mouseX - x_offset) // BLOCKWIDTH
                    gridY = (mouseY - y_offset) // BLOCKHEIGHT

                    if 0 <= gridX < COLS and 0 <= gridY < ROWS:
                        if currentPlayer.guesses[gridY][gridX] == 0:
                            if currentPlayer.check_hit(enemy, gridX, gridY):
                                hit_text = font.render(f"Hit", True, (255, 0, 0))
                                screen.fill("skyblue")
                                screen.blit(hit_text, (GAMEWIDTH // 2 - hit_text.get_width() // 2, GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            else:
                                miss_text = font.render(f"Miss", True, (0, 0, 255))
                                screen.fill("skyblue")
                                screen.blit(miss_text, (GAMEWIDTH // 2 - miss_text.get_width() // 2, GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            drawBoard(screen, currentPlayer, enemy)
                            if check_for_win(enemy):
                                font = pygame.font.Font(None, 48)
                                winner_text = font.render(f"Player {currentPlayer.num} Wins!", True, (255, 0, 0))
                                screen.fill("skyblue")
                                screen.blit(winner_text, (GAMEWIDTH // 2 - winner_text.get_width() // 2, GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(3000)
                                return False, currentPlayer, enemy
                            waiting_for_input = False
                        waiting_for_input = False

    return True, currentPlayer, enemy

def check_for_win(player): #n
    return all(player.sunk_ships.get(ship_size, False) for ship_size in player.ships)

def main(): # (A) main function that starts the game
    pygame.init() # (A) initialize the pygame engine so it can listen for inputs/handle screens
    pygame.display.set_caption("battleship") # (A) set up the title of the game
    game = True # (A) game conditional loop

    screen = pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT)) # (A) the main screen that gets passed around, initialized with a display of GAMEWIDTH and GAMEHEIGHT
    clock = pygame.time.Clock() # (A) clock that keeps track of how many times the screen is updated
    count = getCount(screen) # (A) initial getCount() will be the default starting screen to find how many ships to play with
    setUp = True # (A) check that'll only run the startBoard() once for ships

    playerOne = Player(1) # (A) initialize playerOne, with a Player(num)-- num marker of 1 to differentiate
    playerTwo = Player(2) # (A) playertwo with player.num = 2
    # print(playerOne.board)

    currentPlayer = playerOne # (A) game will start with playerOne, so currentPlayer is initialized
    enemy = playerTwo # (A) enemy for now is playerTwo, but these roles will be swapped every game loop

    while game: # (A) while the game is running
        screen.fill("skyblue") # (A) fill the background with skyblue
        if setUp: # (A) conditional met with first time run of the loop
            startBoard(screen, count, playerOne) # (A) create the matrix for playerOne with ship selection
            startBoard(screen, count, playerTwo) # (A) do the same for playerTwo
            setUp = False # (A) set condition to false, won't run again for remainder of the game
        else: # (A) when the boards have been set up
            font = pygame.font.Font(None, 28) # (A) font object with no font type and 28 font size
            turn_text = font.render(f"Player {currentPlayer.num}'s Turn", True, (5, 5, 5)) # (A) render the text 
            screen.blit(turn_text, (GAMEWIDTH // 2 - turn_text.get_width() // 2, 350)) # (A) push the rendered text to the top of the screen, placed horizontal and in the middle vertically
            
            game, currentPlayer, enemy = handlePlayerTurn(screen, currentPlayer, enemy) # (A) handle the player turn, will swap players (curr/enemy) after each successful playerturn
            if game: # (A) if the game is still going on... may be a redundant conditional in hindsight
                currentPlayer, enemy = enemy, currentPlayer # (A) then swap the two players

        pygame.display.flip() # (A) flip to update the display as needed
        for event in pygame.event.get(): # (A) listen to events
            if event.type == pygame.QUIT: # (A) if user exits out
                game = False # (A) game is over
        clock.tick(FPS) # (A) FPS (initialized at the start of the code) will determine refresh rate for the game


if __name__ == "__main__": # (A) basic name=main check so it doesn't automatically run if called in a module
    main() # (A) if intended, then now run main()
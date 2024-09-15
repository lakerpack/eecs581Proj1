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


def drawLabels(screen, xOffset, yOffset):
    font = pygame.font.Font(None, 26)
    for i in range(COLS):
        label = font.render(chr(65 + i), True, (5, 5, 5))
        screen.blit(label, (xOffset + i * BLOCKWIDTH + BLOCKWIDTH // 2 - label.get_width() // 2, yOffset - 25))
    
    for i in range(ROWS):
        label = font.render(str(i + 1), True, (5, 5, 5))
        screen.blit(label, (xOffset - 25, yOffset + i * BLOCKHEIGHT + BLOCKHEIGHT // 2 - label.get_height() // 2))


def startBoard(screen, count, player):
    lineColor = (255, 255, 255)
    yOffset = 150
    xOffset = 150

    font = pygame.font.Font(None, 36)
    smallFont = pygame.font.Font(None, 16)
    title = font.render(f"Place Your Ships Player {player.num}", True, (5, 5, 5))
    instruction = smallFont.render("Press R to rotate your placement. Click to place a ship.", True, (5, 5, 5))

    ships = [val + 1 for val in range(count)]
    currentShip = ships.pop()
    direction = 0

    waiting = True
    while waiting:
        screen.fill("skyblue")
        screen.blit(title, (GAMEWIDTH // 2 - title.get_width() // 2, yOffset - 75))
        screen.blit(instruction, (GAMEWIDTH // 2 - instruction.get_width() // 2, yOffset + 315))

        drawLabels(screen, xOffset, yOffset)

        mouseX, mouseY = pygame.mouse.get_pos()
        hoverX = (mouseX - xOffset) // BLOCKWIDTH
        hoverY = (mouseY - yOffset) // BLOCKHEIGHT

        for x in range(COLS):
            for y in range(ROWS):
                pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + yOffset, BLOCKWIDTH, BLOCKHEIGHT)
                
                should_highlight = False
                if 0 <= hoverX < COLS and 0 <= hoverY < ROWS:
                    if direction == 0 and hoverY == y and hoverX <= x < hoverX + currentShip and hoverX + currentShip <= COLS:
                        should_highlight = True
                    elif direction == 1 and hoverX == x and hoverY <= y < hoverY + currentShip and hoverY + currentShip <= ROWS:
                        should_highlight = True
                    elif direction == 2 and hoverY == y and hoverX - currentShip < x <= hoverX and hoverX - currentShip + 1 >= 0:
                        should_highlight = True
                    elif direction == 3 and hoverX == x and hoverY - currentShip < y <= hoverY and hoverY - currentShip + 1 >= 0:
                        should_highlight = True

                if should_highlight:
                    pygame.draw.rect(screen, (155, 155, 155), pyRect)
                elif player.board[y][x] != 0:
                    ship_size = player.board[y][x]
                    ship_color = SHIPCOLORS.get(ship_size, (0, 255, 0))
                    pygame.draw.rect(screen, ship_color, pyRect)
                
                pygame.draw.rect(screen, lineColor, pyRect, 1)

        # print(hoverX, hoverY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    direction = (direction + 1) % 4
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 0 <= hoverX < COLS and 0 <= hoverY < ROWS:
                        if player.place_ship(hoverX, hoverY, currentShip, direction):
                            if ships:
                                currentShip = ships.pop()
                            else:
                                waiting = False


def drawBoard(screen, player, enemy):
    lineColor = (255, 255, 255)
    topOffset = 30
    bottomOffset = 400
    xOffset = 150

    drawLabels(screen, xOffset, topOffset)
    for x in range(COLS):
        for y in range(ROWS):
            pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + topOffset, BLOCKWIDTH, BLOCKHEIGHT)
            pygame.draw.rect(screen, lineColor, pyRect, 1)
            if player.guesses[y][x] != 0:
                if player.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)
                elif player.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif player.guesses[y][x] == 'sunk':  # n
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)

    drawLabels(screen, xOffset, bottomOffset)
    for x in range(COLS):
        for y in range(ROWS):
            pyRect = (x * BLOCKWIDTH + xOffset, y * BLOCKHEIGHT + bottomOffset, BLOCKWIDTH, BLOCKHEIGHT)
            pygame.draw.rect(screen, lineColor, pyRect, 1)
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]
                ship_color = SHIPCOLORS.get(ship_size, (0, 255, 0))
                pygame.draw.rect(screen, ship_color, pyRect)
            if enemy.guesses[y][x] != 0:
                if enemy.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)
                elif enemy.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif enemy.guesses[y][x] == 'sunk': #n
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)

def handlePlayerTurn(screen, currentPlayer, enemy):
    waiting_for_input = True
    x_offset = 150 #n
    y_offset = 30
    font = pygame.font.Font(None, 36)
    while waiting_for_input:
        drawBoard(screen, currentPlayer, enemy)
        pygame.display.flip()

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

def main():
    pygame.init()
    pygame.display.set_caption("battleship")
    game = True

    screen = pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT))
    clock = pygame.time.Clock()
    count = getCount(screen)
    setUp = True

    playerOne = Player(1)
    playerTwo = Player(2)
    # print(playerOne.board)

    currentPlayer = playerOne
    enemy = playerTwo

    while game:
        screen.fill("skyblue")
        if setUp:
            startBoard(screen, count, playerOne)
            startBoard(screen, count, playerTwo)
            setUp = False
        else:
            font = pygame.font.Font(None, 28)
            turn_text = font.render(f"Player {currentPlayer.num}'s Turn", True, (5, 5, 5))
            screen.blit(turn_text, (GAMEWIDTH // 2 - turn_text.get_width() // 2, 350))
            
            game, currentPlayer, enemy = handlePlayerTurn(screen, currentPlayer, enemy)
            if game:
                currentPlayer, enemy = enemy, currentPlayer

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        clock.tick(FPS)


if __name__ == "__main__":
    main()
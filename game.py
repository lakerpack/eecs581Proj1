import sys
import pygame

FPS = 30
ROWS, COLS = 10, 10
BLOCKHEIGHT, BLOCKWIDTH = 30, 30
GAMEHEIGHT, GAMEWIDTH = 700, 600

SHIPCOLORS = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (255, 255, 0), 5: (255, 0, 255)}

class Player:
    def __init__(self, num):
        self.num = num
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.guesses = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    def place_ship(self, x, y, size, direction):
        if direction == 0: 
            if x + size > COLS:
                return False
            for i in range(size):
                if self.board[y][x + i] != 0:
                    return False
            for i in range(size):
                self.board[y][x + i] = size
        elif direction == 1: 
            if y + size > ROWS:
                return False
            for i in range(size):
                if self.board[y + i][x] != 0:
                    return False
            for i in range(size):
                self.board[y + i][x] = size
        elif direction == 2: 
            if x - size + 1 < 0:
                return False
            for i in range(size):
                if self.board[y][x - i] != 0:
                    return False
            for i in range(size):
                self.board[y][x - i] = size
        elif direction == 3: 
            if y - size + 1 < 0:
                return False
            for i in range(size):
                if self.board[y - i][x] != 0:
                    return False
            for i in range(size):
                self.board[y - i][x] = size
        return True

def getCount(screen):
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    
    title = title_font.render("Battleship", True, (5, 5, 5))
    prompt = font.render("How many ships would you like? (1-5)", True, (5, 5, 5))
    start_text = font.render("Press ENTER to start", True, (5, 5, 5))

    ship_count = 1
    running = True
    
    while running:
        screen.fill("skyblue")
        
        screen.blit(title, (GAMEWIDTH//2 - title.get_width()//2, 100))
        screen.blit(prompt, (GAMEWIDTH//2 - prompt.get_width()//2, 200))
        screen.blit(start_text, (GAMEWIDTH//2 - start_text.get_width()//2, 400))

        count_text = font.render(str(ship_count), True, (5, 5, 5))
        screen.blit(count_text, (GAMEWIDTH//2 - count_text.get_width()//2, 300))
                
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship_count = min(ship_count + 1, 5)
                elif event.key == pygame.K_DOWN:
                    ship_count = max(ship_count - 1, 1)
                elif event.key == pygame.K_RETURN:
                    return ship_count
    
    return ship_count


def drawLabels(screen, xOffset, yOffset):
    font = pygame.font.Font(None, 24)
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


def drawBoard(screen, user):
    lineColor = (255, 255, 255)
    boardWidth = BLOCKWIDTH * COLS
    boardHeight = BLOCKHEIGHT * ROWS
    yOffset = 30
    xOffset = 150

    if user == "Enemey":
        yOffset = 400

    drawLabels(screen, xOffset, yOffset)

    for x in range(0, boardWidth, BLOCKWIDTH):
        for y in range(0, boardHeight, BLOCKHEIGHT):
            pyRect = (x + xOffset, y + yOffset, BLOCKWIDTH, BLOCKHEIGHT)
            pygame.draw.rect(screen, lineColor, pyRect, 1)


def main():
    pygame.init()
    game = True

    screen = pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT))
    clock = pygame.time.Clock()
    count = getCount(screen)
    setUp = True

    playerOne = Player(1)
    playerTwo = Player(2)
    # print(playerOne.board)

    while game:
        screen.fill("skyblue")
        if setUp:
            startBoard(screen, count, playerOne)
            startBoard(screen, count, playerTwo)
            setUp = False

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        clock.tick(FPS)


if __name__ == "__main__":
    main()
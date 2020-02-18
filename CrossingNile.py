import pygame
import random
from datetime import datetime
import configparser
pygame.init()

clock = pygame.time.Clock()
# For seeding the random generator with current time
random.seed(datetime.now())
# Setting up configuration parser
configParser = configparser.RawConfigParser()
configParser.read("config.cfg")
# Setting up game window
gameName = configParser.get("info", "name")
gameWidth = configParser.getint("info", "width")
gameHeight = configParser.getint("info", "height")
win = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption(gameName)
# Setting up images
loc = configParser.get("imageLoc", "bg")
bg = pygame.image.load(loc)
loc = configParser.get("imageLoc", "log")
log = pygame.image.load(loc)
log = pygame.transform.scale(log, (1024, 40))
loc = configParser.get("imageLoc", "scorpion")
scorpion = pygame.image.load(loc)
scorpion = pygame.transform.scale(scorpion, (50, 35))
loc = configParser.get("imageLoc", "snake")
snake = pygame.image.load(loc)
snake = pygame.transform.scale(snake, (50, 35))
loc = configParser.get("imageLoc", "crocLeft")
crocLeft = pygame.image.load(loc)
crocLeft = pygame.transform.scale(crocLeft, (250, 50))
loc = configParser.get("imageLoc", "crocRight")
crocRight = pygame.image.load(loc)
crocRight = pygame.transform.scale(crocRight, (250, 50))
loc = configParser.get("imageLoc", "sharkLeft")
sharkLeft = pygame.image.load(loc)
loc = configParser.get("imageLoc", "sharkRight")
sharkRight = pygame.image.load(loc)
# Setting up font
defFont = configParser.get("font", "font")
font = pygame.font.SysFont(defFont, 30, True, False)
font1 = pygame.font.SysFont(defFont, 100, True, False)
# Setting up background music
loc = configParser.get("music", "music")
music = pygame.mixer.music.load(loc)
pygame.mixer.music.play(-1)
# Setting up colors
colTuple = []
colStr = str(configParser.get("color", "red")).split(',')
for val in colStr:
    colTuple.append(int(val))
col = tuple(colTuple)
red = col
colTuple.clear()
colStr = str(configParser.get("color", "green")).split(',')
for val in colStr:
    colTuple.append(int(val))
col = tuple(colTuple)
green = col
colTuple.clear()
colStr = str(configParser.get("color", "blue")).split(',')
for val in colStr:
    colTuple.append(int(val))
col = tuple(colTuple)
blue = col
colTuple.clear()
colStr = str(configParser.get("color", "black")).split(',')
for val in colStr:
    colTuple.append(int(val))
col = tuple(colTuple)
black = col
colTuple.clear()
colStr = str(configParser.get("color", "white")).split(',')
for val in colStr:
    colTuple.append(int(val))
col = tuple(colTuple)
white = col
# Setting up messages
success = font1.render("SUCCESS!", 1, green)
fail = font1.render("WASTED!", 1, red)
# Global Variables
run = True
level = [1, 1]
order = 0
p1Points = []
p2Points = []
score = 0


class Player(object):
    """ Make Objects for Player Character"""

    def __init__(self, x, y):
        """ Construct Player Object """
        self.x = x          # x-Coordinate
        self.y = y          # y-Coordinate
        self.height = 64    # Height
        self.width = 64     # Weight
        vel = configParser.getint("character", "vel")
        self.vel = vel      # Velocity
        # Sprite Sheet
        self.walkLeft = [
            pygame.image.load("./Images/" + str(order + 1) + "left (1).png"),
            pygame.image.load("./Images/" + str(order + 1) + "left (2).png"),
            pygame.image.load("./Images/" + str(order + 1) + "left (2).png")]
        self.walkRight = [
            pygame.image.load("./Images/" + str(order + 1) + "right (1).png"),
            pygame.image.load("./Images/" + str(order + 1) + "right (2).png"),
            pygame.image.load("./Images/" + str(order + 1) + "right (3).png")]
        self.walkUp = [
            pygame.image.load("./Images/" + str(order + 1) + "up (1).png"),
            pygame.image.load("./Images/" + str(order + 1) + "up (2).png"),
            pygame.image.load("./Images/" + str(order + 1) + "up (3).png")]
        self.walkDown = [
            pygame.image.load("./Images/" + str(order + 1) + "down (1).png"),
            pygame.image.load("./Images/" + str(order + 1) + "down (2).png"),
            pygame.image.load("./Images/" + str(order + 1) + "down (3).png")]
        # Active Direction
        self.left = False
        self.right = False
        if order:
            self.up = False
            self.down = True
        else:
            self.up = True
            self.down = False
        # Movement Variables
        self.walkCount = 0
        self.standing = True
        # Hitbox
        self.hitbox = (self.x - 2, self.y - 2, 64, 64)

    def draw(self, win):
        """ Draw the Player on the Screen """
        if self.walkCount + 1 >= 15:
            self.walkCount %= 15
        if not self.standing:
            if self.right:
                win.blit(self.walkRight[(self.walkCount % 15) // 5],
                         (self.x, self.y))
                self.walkCount += 1
            elif self.left:
                win.blit(self.walkLeft[(self.walkCount % 15) // 5],
                         (self.x, self.y))
                self.walkCount += 1
            elif self.up:
                win.blit(self.walkUp[(self.walkCount % 15) // 5],
                         (self.x, self.y))
                self.walkCount += 1
            elif self.down:
                win.blit(self.walkDown[(self.walkCount % 15) // 5],
                         (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[(self.walkCount % 15) // 5],
                         (self.x, self.y))
            elif self.left:
                win.blit(self.walkLeft[(self.walkCount % 15) // 5],
                         (self.x, self.y))
            elif self.up:
                win.blit(self.walkUp[(self.walkCount % 15) // 5],
                         (self.x, self.y))
            elif self.down:
                win.blit(self.walkDown[(self.walkCount % 15) // 5],
                         (self.x, self.y))
        self.hitbox = (self.x - 2, self.y - 2, 64, 64)

    def move(self, keys):
        """ Move Player - Change Active Direction and Movement Variables """
        # Left Arrow Key Press
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.standing = False
        # Right Arrow Key Press
        elif keys[pygame.K_RIGHT] and self.x < 1024 - self.width - self.vel:
            self.x += self.vel
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.standing = False
        # Up Arrow Key Press
        elif keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.standing = False
        # Down Arrow Key Press
        elif keys[pygame.K_DOWN] and self.y < 768 - self.height - self.vel:
            self.y += self.vel
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.standing = False
        # No Key Press
        else:
            self.standing = True
            self.walkCount = 0


class Enemy(object):
    """ Make Objects for Enemy Character """

    def __init__(self, x, y, diff):
        """ Construct Enemy Object """
        self.x = x              # x-coordinate
        self.y = y              # y-coordinate
        self.path = [10, 760]   # Path endpoints
        vel = configParser.getint("character", "vel")
        self.vel = vel + (vel * (diff - 1) / 2)     # Velocity
        self.i = random.randrange(2)                # Random - Croc vs Shark
        # Sprite Sheet and Hitbox
        if self.i:
            self.walkLeft = sharkLeft
            self.walkRight = sharkRight
            self.hitbox = (self.x - 2, self.y - 2, 120, 80)
        else:
            self.walkLeft = crocLeft
            self.walkRight = crocRight
            self.hitbox = (self.x - 2, self.y - 2, 250, 50)

    def draw(self, win):
        """ Draw Enemy Character on the Screen """
        self.move()
        if self.vel > 0:
            win.blit(self.walkRight, (self.x, self.y))
        else:
            win.blit(self.walkLeft, (self.x, self.y))
        if self.i:
            self.hitbox = (self.x - 2, self.y - 2, 120, 80)
        else:
            self.hitbox = (self.x - 2, self.y - 2, 250, 50)

    def move(self):
        """ Move Enemy Character on the Screen """
        # 1/100 Chance to reverse direction
        if not random.randrange(100):
            self.vel *= -1
        # Move Right
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
        # Move Left
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1


def redrawBackground():
    """ Redraw Background """
    win.blit(bg, (0, 0))
    pygame.display.update()


def landingPage():
    """ Landing Page """
    global run
    redrawBackground()
    h1 = font1.render("Crossing The Nile", 1, black)
    win.blit(h1, (150, 300))
    p = font.render("~> Press ENTER to Play!", 1, red)
    win.blit(p, (100, 400))
    p = font.render("~> Use Arrow keys to move", 1, white)
    win.blit(p, (100, 450))
    p = font.render("~> Dodge obstacles and reach the other bank", 1, white)
    win.blit(p, (100, 480))
    p = font.render("~> Progress thorugh rounds to WIN", 1, white)
    win.blit(p, (100, 510))
    p = font.render("SCORING:", 1, green)
    win.blit(p, (100, 550))
    p = font.render("> Crossing Moving Obstacles: 10 Points", 1, white)
    win.blit(p, (150, 580))
    p = font.render("> Crossing Fixed Obstacles: 5 Points", 1, white)
    win.blit(p, (150, 610))
    p = font.render("> Time Penalty: -1 point every second", 1, white)
    win.blit(p, (150, 640))
    p = font.render("> Level Bonus", 1, white)
    win.blit(p, (150, 670))
    pygame.display.update()
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if keys[pygame.K_RETURN]:
            gameInit()
            break


def roundBreak():
    """ Break Between Rounds """
    global run
    redrawBackground()
    h1 = font1.render("Crossing The Nile", 1, black)
    win.blit(h1, (150, 300))
    p = font.render("~> Press SPACE to Play!", 1, red)
    win.blit(p, (100, 400))
    p = font.render("~> Press ESC to End Game and See Result", 1, white)
    win.blit(p, (100, 450))
    pygame.display.update()
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if keys[pygame.K_SPACE]:
            gameInit()
            break
        if keys[pygame.K_ESCAPE]:
            result()
            break


def result():
    """ Result of Game played """
    global run
    global p1Points
    global p2Points
    # Player points variables
    p1 = 0
    p2 = 0
    redrawBackground()
    h1 = font1.render("Crossing The Nile", 1, black)
    win.blit(h1, (150, 300))
    pygame.display.update()
    # Player 1 Points
    for i in p1Points:
        p1 += i
        redrawBackground()
        win.blit(h1, (150, 300))
        p = font.render("~> Player 1: " + str(p1), 1, white)
        win.blit(p, (100, 400))
        pygame.display.update()
        pygame.time.delay(300)
    # Player 2 Points
    for i in p2Points:
        p2 += i
        redrawBackground()
        win.blit(h1, (150, 300))
        p = font.render("~> Player 1: " + str(p1), 1, white)
        win.blit(p, (100, 400))
        p = font.render("~> Player 2: " + str(p2), 1, white)
        win.blit(p, (100, 430))
        pygame.display.update()
        pygame.time.delay(300)
    # Decide Winner
    if p1 > p2:
        p = font1.render("Player 1 Wins", 1, red)
    elif p1 < p2:
        p = font1.render("Player 2 Wins", 1, red)
    else:
        p = font1.render("STALEMATE!", 1, red)
    win.blit(p, (150, 480))
    p = font.render("~> Press SPACE to Start New Game", 1, white)
    win.blit(p, (100, 600))
    pygame.display.update()
    # Clear Points
    p1Points.clear()
    p2Points.clear()
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if keys[pygame.K_SPACE]:
            break


def redrawGameWindow(obsx, obsy, movObs, play):
    """ Redraw Game Window """
    win.blit(bg, (0, 0))
    i = 0
    # Draw partitions and obstacles
    while i < 5:
        win.blit(log, (0, obsy[i]))
        if i % 2:
            win.blit(snake, (obsx[i], obsy[i]))
        else:
            win.blit(scorpion, (obsx[i], obsy[i]))
        movObs[i].draw(win)
        i += 1
    play.draw(win)  # Draw player character
    text = font.render("Level: " + str(level[order]), 1, black)
    win.blit(text, (850, 10))
    text = font.render("Score: " + str(score), 1, black)
    win.blit(text, (850, 730))
    pygame.display.update()


def gameInit():
    """ Game Function Decorator """
    global run
    global order
    redrawBackground()
    h1 = font1.render("Crossing The Nile", 1, black)
    win.blit(h1, (150, 300))
    p = font.render("Player " + str(order + 1) + "'s Turn", 1, red)
    win.blit(p, (400, 400))
    pygame.display.update()
    pygame.time.delay(1000)
    game()
    if not run:
        return
    order = (order + 1) % 2
    redrawBackground()
    h1 = font1.render("Crossing The Nile", 1, black)
    win.blit(h1, (150, 300))
    p = font.render("Player " + str(order + 1) + "'s Turn", 1, red)
    win.blit(p, (400, 400))
    pygame.display.update()
    pygame.time.delay(1000)
    game()
    if not run:
        return
    roundBreak()
    if not run:
        return


def game():
    """ Game Function """
    global run
    global score
    global level
    global p1Points
    global p2Points
    score = 0   # Current score
    run2 = True
    # Obstacles
    obsx = []
    obsy = []
    movObs = []
    obsPass = [0, 0, 0, 0, 0]
    movPass = [0, 0, 0, 0, 0]
    i = 0
    j = 768 // 5 - 80
    while i < 5:
        obsx.append(random.randrange(50, 700))
        obsy.append(j)
        j += 768 // 6
        movObs.append(Enemy(obsx[i], (obsy[i] + j) // 2 - 20, level[order]))
        i += 1
    # Create player object
    if order:
        play = Player(450, 10)
    else:
        play = Player(450, 720)
    start_ticks = pygame.time.get_ticks()
    while run and run2:
        clock.tick(60)
        # Time bonus
        ticks = pygame.time.get_ticks()
        dsec = (ticks - start_ticks) // 500
        if dsec > 0:
            score -= dsec * 0.5
            start_ticks = ticks
            dsec = 0
        redrawGameWindow(obsx, obsy, movObs, play)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Collision Detection
        for obs in movObs:
            if play.hitbox[1] < obs.hitbox[1] + obs.hitbox[3] - 10 \
               and play.hitbox[1] + play.hitbox[3] > obs.hitbox[1] + 10:
                if play.hitbox[0] + play.hitbox[2] > obs.hitbox[0] + 10 \
                   and play.hitbox[0] < obs.hitbox[0] + obs.hitbox[2] - 10:
                    win.blit(fail, (300, 300))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    run2 = False
                    break
        i = 0
        while i < 5:
            if play.hitbox[1] < obsy[i] + 30 \
               and play.hitbox[1] + play.hitbox[3] > obsy[i] + 10:
                if play.hitbox[0] + play.hitbox[2] > obsx[i] + 10 \
                   and play.hitbox[0] < obsx[i] + 40:
                    win.blit(fail, (300, 300))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    run2 = False
                    break
            i += 1
        # Score increment and success detection
        if order:
            i = 0
            while i < 5:
                if play.hitbox[1] > \
                   movObs[i].hitbox[1] + movObs[i].hitbox[3] - 15:
                    if not movPass[i]:
                        score += 10 * (1 + (level[order] - 1) * 0.5)
                        movPass[i] = 1
                if play.hitbox[1] > obsy[i] - 5:
                    if not obsPass[i]:
                        score += 5 * (1 + (level[order] - 1) * 0.5)
                        obsPass[i] = 1
                i += 1
            if play.hitbox[1] > movObs[4].hitbox[1] + movObs[4].hitbox[3] - 10:
                level[order] += 1
                win.blit(success, (300, 300))
                pygame.display.update()
                pygame.time.delay(1000)
                run2 = False
        else:
            i = 0
            while i < 5:
                if play.hitbox[1] + play.hitbox[3] < movObs[i].hitbox[1] + 15:
                    if not movPass[i]:
                        score += 10 * (1 + (level[order] - 1) * 0.5)
                        movPass[i] = 1
                if play.hitbox[1] + play.hitbox[3] < obsy[i] + 5:
                    if not obsPass[i]:
                        score += 5 * (1 + (level[order] - 1) * 0.5)
                        obsPass[i] = 1
                i += 1
            if play.hitbox[1] + play.hitbox[3] < obsy[0]:
                level[order] += 1
                win.blit(success, (300, 300))
                pygame.display.update()
                pygame.time.delay(1000)
                run2 = False
        play.move(keys)
    del play    # Delete player object
    # Append current score
    if order:
        p2Points.append(score)
    else:
        p1Points.append(score)


while run:
    """ Interface loop """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Initialization
    level = [1, 1]
    order = 0
    p1Points.clear
    p2Points.clear
    landingPage()
pygame.quit()

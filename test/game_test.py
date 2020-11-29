import pygame
import numpy as np
import operator
import random

# define dimensions
HEIGHT = 40
WIDTH = 60
SIZE = 15
screen_width = WIDTH * SIZE
screen_height = HEIGHT * SIZE

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# show text on screen (this probs is not the best way to do this...)
def draw_text(text, font, text_col, x, y, screen):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# fun background for later
# bg = pygame.image.load('img/space.jpg')

DIR = {
    'u' : (0, -1), # north is -y
    'd' : (0, 1),
    'l' : (-1,0),
    'r' : (1,0)
    }

# drawing game surface
def draw_grid(surface, walls):
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
            if (x, y) in walls:
               color = (255,255,255)
            else:
               color = (0,0,0)
            pygame.draw.rect(surface, color, r)

# moving obstacle class
class Obstacle():
    def __init__(self, x, y, vel):
        self.vel = vel
        self.position = (x, y)

    def update(self):
        self.position = tuple(map(operator.add, self.position, (self.vel, 0)))
        if self.position[0] > 40 or self.position[0] < 20:
            self.vel = -self.vel

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
        pygame.draw.rect(surface, green, r)

    def get_position(self):
        return self.position

# player class
class Player():

    def __init__(self, x, y):
        self.position = (x, y)
        pass

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = (x, y)

    def move(self, dir):
        self.position = tuple(map(operator.add, self.position, DIR[dir]))

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
        pygame.draw.rect(surface, red, r)

# goal class
class Goal():
    def __init__ (self, x, y):
        self.position = (x, y)

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
        pygame.draw.rect(surface, blue, r)

    def get_position(self):
        return self.position

# ai agent class
class Agent():
    def __init__(self, x, y):
        self.player = Player(x,y);

    def move(self):
        i = random.randint(0, 4)
        if i == 0:
            self.player.move('l')
        elif i == 1:
            self.player.move('r')
        elif i == 2:
            self.player.move('u')
        else:
            self.player.move('d')

    def get_position(self):
        return self.player.get_position()

    def draw(self, surface):
        self.player.draw(surface)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 20

    walls = []

    for x in range(WIDTH):
        walls.append((x, 0))
        walls.append((x, HEIGHT-1))

    for x in range(HEIGHT):
        walls.append((0, x))
        walls.append((WIDTH-1, x))

    for x in range(HEIGHT-10):
        walls.append((18, x))

    for x in range(10, HEIGHT):
        walls.append((42, x))

    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Worlds Hardest Game')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface, walls)

    #player = Player(5, 5)
    player = Agent(5,10)
    goal = Goal(55, 35)

    vel_left = 1
    vel_right = -1

    obstacles = [
        Obstacle(31, 11, vel_left),
        Obstacle(32, 12, vel_left),
        Obstacle(33, 13, vel_left),
        Obstacle(34, 14, vel_right),
        Obstacle(35, 15, vel_right),
        Obstacle(36, 16, vel_right),
    ]

    # define font
    font = pygame.font.SysFont('Bauhaus 93', 60)

    # .Rect(x-coord, y-coord, width, height)
    #player = pygame.Rect(50, 50, 30, 30)
    #goal = pygame.Rect(1100, 50, 50, 50)

    run = True
    alive = True
    win = False

    while run:
        clock.tick(fps)

        #draw background
        # screen.blit(bg, (0,0))

        #delay start of game by 10ms
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move player using arrow keys
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT] and player.get_position()[0] > 0:
        #    player.move('l')
        #if keys[pygame.K_RIGHT] and player.get_position()[0] < WIDTH - 1:
        #    player.move('r')
        #if keys[pygame.K_UP] and player.get_position()[1] > 0:
        #    player.move('u')
        #if keys[pygame.K_DOWN] and player.get_position()[1] < HEIGHT - 1:
        #    player.move('d')

        ## collision with obstacle
        for obstacle in obstacles:
            obstacle.update()
            if player.get_position() == obstacle.get_position():
                alive = False

        # collision with wall
        for wall in walls:
            if player.get_position() == wall:
                alive = False

        if player.get_position() == goal.get_position():
            win = True

        if alive == True and win == False:
            player.move()
            print(player.get_position())

            draw_grid(surface, walls)
            player.draw(surface)
            goal.draw(surface)

            for obstacle in obstacles:
                obstacle.draw(surface)

            screen.blit(surface, (0,0))

        else:
            if win:
                draw_text("You Win!", font, white, 500, 20, screen)
            else:
                draw_text("Game Over", font, white, 500, 20, screen)

        pygame.display.update()
        if not run:
            pygame.quit()

#if __name__ == "__main__":
#    main()
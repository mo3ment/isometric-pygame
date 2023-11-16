import pygame, sys
from pygame.locals import *


#=====================================================
#===================== FUNCTIONS =====================
#=====================================================

COLLISION_TILE = 9
FPS = 60
MAP_RATE = 20
PLAYER_AXIS_RATE = FPS/MAP_RATE
PLAYER_DIAG_RATE = PLAYER_AXIS_RATE/3
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)


#=====================================================
#=================== GAME WINDOW =====================
#=====================================================

pygame.init()
game_clock = pygame.time.Clock()
pygame.display.set_caption('LIBERATION')
screen = pygame.display.set_mode((900, 900),0,32)
display = pygame.Surface((300, 300))


#=====================================================
#===================== FUNCTIONS =====================
#=====================================================


def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions
 
def move(rect,movement,tiles):
    rect.x += movement[0]
    collisions = collision_test(rect,tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
        if movement[0] < 0:
            rect.left = tile.right

    rect.y += movement[1]
    collisions = collision_test(rect,tiles)
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.top
        if movement[1] < 0:
            rect.top = tile.bottom

    return rect


#=====================================================
#================== INSTANTIATIONS ===================
#=====================================================


f = open('map.txt')
map_data = [[int(c) for c in row] for row in f.read().split('\n')]
f.close()

player_rect = pygame.Rect(12*MAP_RATE,4*MAP_RATE,1*MAP_RATE,1*MAP_RATE)
right, left, up, down = (False, False, False, False)


#=====================================================
#==================== GAME-LOOP ======================
#=====================================================

while True:
    # clear display #
    boundary_tiles = []
    screen.fill(BLACK)

    for y_pos, row in enumerate(map_data):
        for x_pos, tile in enumerate(row):
            if tile:
                if tile == COLLISION_TILE:
                    boundary_tiles.append(pygame.Rect(x_pos*MAP_RATE, y_pos*MAP_RATE, 1*MAP_RATE, 1*MAP_RATE))
                    pygame.draw.rect(screen, RED, boundary_tiles[-1])


#=====================================================
#================= PLAYER-MOVEMENT ===================
#=====================================================

    player_movement = [0,0]
    if left == True and up == True:
        player_movement[0] += PLAYER_DIAG_RATE
        player_movement[1] += PLAYER_DIAG_RATE
    elif right == True and up == True:
        player_movement[0] -= PLAYER_DIAG_RATE
        player_movement[1] += PLAYER_DIAG_RATE
    elif left == True and down == True:
        player_movement[0] += PLAYER_DIAG_RATE
        player_movement[1] -= PLAYER_DIAG_RATE
    elif right == True and down == True:
        player_movement[0] -= PLAYER_DIAG_RATE
        player_movement[1] -= PLAYER_DIAG_RATE
    if right == True:
        player_movement[0] += PLAYER_AXIS_RATE
    if left == True:
        player_movement[0] -= PLAYER_AXIS_RATE
    if up == True:
        player_movement[1] -= PLAYER_AXIS_RATE
    if down == True:
        player_movement[1] += PLAYER_AXIS_RATE
 
    player = move(player_rect,player_movement,boundary_tiles)
    pygame.draw.rect(screen, WHITE, player)
    
    # event handling #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_UP:
                up = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_DOWN:
                down = False
            if event.key == K_UP:
                up = False
    
    # update display #
    pygame.display.update()
    game_clock.tick(FPS)
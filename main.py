import pygame, sys
import numpy as np
from pygame.locals import *


#=====================================================
#==================== FUNCTIONS ======================
#=====================================================

UPSCALE = 2

COLLISION_TILE = 9
FPS = 40
MAP_RATE = 7
#PLAYER_AXIS_RATE = 3
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)


#=====================================================
#=================== GAME WINDOW =====================
#=====================================================

pygame.init()
game_clock = pygame.time.Clock()
pygame.display.set_caption('LIBERATION')
screen = pygame.display.set_mode((960, 720),0,32)
display = pygame.Surface((400, 300))


#=====================================================
#===================== FUNCTIONS =====================
#=====================================================


def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
            return collisions
    return collisions
 
def check_collision_x(map_rect,iso_rect,tiles,left,right,up,down):
    corner_case = False
    
    if (up and left) or (up and right):
        corner_case = True
        map_rect.x -= 1*up
        iso_rect.x -= 2*up
        iso_rect.y -= 1*up

    elif (left and down) or (right and down):
        corner_case = True
        map_rect.x += 1*down
        iso_rect.x += 2*down
        iso_rect.y += 1*down

    else:
        map_rect.x -= 2*(up - down)
        iso_rect.x -= 4*(up - down)
        iso_rect.y -= 2*(up - down)
    collisions = collision_test(map_rect,tiles)

    for tile in collisions:
        if down:
            if corner_case:
                map_rect.x -= 1
                iso_rect.x -= 2
                iso_rect.y -= 1 
            else:
                map_rect.x -= 2
                iso_rect.x -= 4
                iso_rect.y -= 2
        elif up:
            if corner_case:
                map_rect.x += 1
                iso_rect.x += 2
                iso_rect.y += 1 
            else:
                map_rect.x += 2
                iso_rect.x += 4
                iso_rect.y += 2
    return map_rect, iso_rect

def check_collision_y(map_rect,iso_rect,tiles,left,right,up,down):
    corner_case = False

    if (left and up) or (right and up) or (left and down) or (right and down):
        corner_case = True
        map_rect.y -= 1*(right - left)
        iso_rect.x += 2*(right - left)
        iso_rect.y -= 1*(right - left)

    else:
        map_rect.y -= 2*(right - left)
        iso_rect.x += 4*(right - left)
        iso_rect.y -= 2*(right - left)
    collisions = collision_test(map_rect,tiles)

    for tile in collisions:
        if left:
            if corner_case:
                map_rect.y -= 1
                iso_rect.x += 2
                iso_rect.y -= 1
            else:
                map_rect.y -= 2
                iso_rect.x += 4
                iso_rect.y -= 2
        elif right:
            if corner_case:
                map_rect.y += 1
                iso_rect.x -= 2
                iso_rect.y += 1
            else:
                map_rect.y += 2
                iso_rect.x -= 4
                iso_rect.y += 2
    return map_rect, iso_rect

#=====================================================
#==================== INITIATIONS ====================
#=====================================================

f = open('map.txt')
map_data = np.array([[int(c) for c in row] for row in f.read().split('\n')], dtype=np.int32)
f.close()

player_map_rect = pygame.Rect((12*MAP_RATE+1)*UPSCALE,(4*MAP_RATE+1)*UPSCALE,(1*MAP_RATE-2)*UPSCALE,(1*MAP_RATE-2)*UPSCALE)
right, left, up, down = (False, False, False, False)

floor_sprite = pygame.image.load('floor-tile-middle-upscaled.png')
floor_sprite.set_colorkey(RED)

player_shadow_sprite = pygame.image.load('player-shadow-upscaled.png')
player_shadow_sprite.set_colorkey(RED)
player_shadow_rect = pygame.Rect((player_map_rect.x/MAP_RATE-player_map_rect.y/MAP_RATE)*(16-2)+7*UPSCALE-1, (player_map_rect.y/MAP_RATE+player_map_rect.x/MAP_RATE)*(8-1)+1*UPSCALE,player_shadow_sprite.get_width(),player_shadow_sprite.get_height())

true_camera = [0,0]

#=====================================================
#==================== GAME-LOOP ======================
#=====================================================

while True:
    # clear display #
    boundary_tiles = []
    display.fill(WHITE)

    true_camera[0] += (player_shadow_rect.centerx-true_camera[0]-100*UPSCALE)/10
    true_camera[1] += (player_shadow_rect.centery-true_camera[1]-75*UPSCALE)/10
    camera = true_camera.copy()
    camera[0] = int(camera[0])
    camera[1] = int(camera[1])

    for y_pos, row in enumerate(map_data):
        for x_pos, tile in enumerate(row):
            if tile:
                if tile == COLLISION_TILE:
                    boundary_tiles.append(pygame.Rect(x_pos*MAP_RATE*UPSCALE, y_pos*MAP_RATE*UPSCALE, 1*MAP_RATE*UPSCALE, 1*MAP_RATE*UPSCALE))
                    #pygame.draw.rect(display, RED, boundary_tiles[-1])
                if tile == 1:
                    display.blit(floor_sprite, ((x_pos-y_pos)*(16-2)*UPSCALE-camera[0], (y_pos+x_pos)*(8-1)*UPSCALE-camera[1]))

#=====================================================
#================= PLAYER-MOVEMENT ===================
#=====================================================

    player_velocity = np.array([0,0], dtype=np.int8)

    if right == True:
        player_map_rect, player_shadow_rect = check_collision_y(player_map_rect,player_shadow_rect,boundary_tiles,left,right,up,down)
    if left == True:
        player_map_rect, player_shadow_rect = check_collision_y(player_map_rect,player_shadow_rect,boundary_tiles,left,right,up,down)
    if up == True:
        player_map_rect, player_shadow_rect = check_collision_x(player_map_rect,player_shadow_rect,boundary_tiles,left,right,up,down)
    if down == True:
        player_map_rect, player_shadow_rect = check_collision_x(player_map_rect,player_shadow_rect,boundary_tiles,left,right,up,down)
        

    
    #pygame.draw.rect(display,WHITE,player_map_rect)
    #pygame.draw.rect(display,RED,player_shadow_rect)
    display.blit(player_shadow_sprite, (player_shadow_rect.x-camera[0],player_shadow_rect.y-camera[1]))

    # event handling #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
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
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    game_clock.tick(FPS)
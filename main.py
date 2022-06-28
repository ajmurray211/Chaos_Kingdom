
from configparser import MissingSectionHeaderError
from syslog import LOG_USER
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# set border 
# import font
main_font = pygame.font.SysFont('comicsans', 30)

# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size
PLAYER_W, PLAYER_H = 70, 70
BULLET_W, BULLET_H = 10, 10

## Import pictures and set colors ##
# player 1
BLUE_PLAYER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player.png')), (PLAYER_W, PLAYER_H))
# player 2
YELLOW_PLAYER= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yellow_player.png')), (PLAYER_W, PLAYER_H))
# Bullet
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bullet.png')), (PLAYER_W, PLAYER_H))
BARB_WIRE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'barb_wire.png')), (40, HEIGHT))
# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu_bg.jpeg')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG, '3':BATTLEMAP_BG}

# color
color_dict = {'white':(255,255,255), 'yellow':(0,255,255), 'blue':(0,255,0), 'black':(0,0,0)}
text_dict = { 
    '1': {
        "title": "Chaos Kingdom",
        "prompt": "Press any key to start",
        'size': 50
    },
    '2':{
        'title': 'Game Board',
        'size': 100
    },
    '3':{   
        'title': "Battle map",
        'blue':{
            'ammo': 5,
            'structures': 3,
            'health': 100
        },
        'yellow':{
            'ammo': 5,
            'structures': 3,
            'health': 100
        }
    }
}

## Battlemap gameplay ##

# player class
    # def to shoot
    # def to move bullets
    # def for being hit 
    # def to draw
    # def for healthbar

# class for bullet
    # def for moving
    # def for draw
    # def for collision
    # def for offscreen

# def to draw the winner text

# def to draw main_menu
def draw_main_menu(input):
    title = main_font.render(input['title'], 1, color_dict['white'])
    prompt = main_font.render(input['prompt'], 1, color_dict['white'])
    WIN.blit(title, (WIDTH/2 - title.get_width()/2,10))
    WIN.blit(prompt, (WIDTH/2 - prompt.get_width()/2 ,HEIGHT/2))
# def to draw main_menu
def draw_gameboard(input):
    main_text = main_font.render(input['title'], 1, (255,255,255))
    WIN.blit(main_text, (10,10))
# def to draw main_menu
def draw_battlemap(input):
    main_text = main_font.render(input['title'], 1, (255,255,255))
    WIN.blit(main_text, (50,50))
    WIN.blit(YELLOW_PLAYER, (10, HEIGHT - YELLOW_PLAYER.get_height() - 10))
    WIN.blit(BLUE_PLAYER, (WIDTH - BLUE_PLAYER.get_width() - 10, 10))
    WIN.blit(BARB_WIRE, (WIDTH/2 - BARB_WIRE.get_width()/2, 10))

# def to draw the window
def draw_window(background, curr_index):
    """This method updates the window"""
    WIN.blit(background, (0,0))

    # filter what to display 
    if curr_index == 1:
        draw_main_menu(text_dict['1'])
    if curr_index == 2:
        draw_gameboard(text_dict['2'])
    if curr_index == 3:
        draw_battlemap(text_dict['3'])

    pygame.display.update()

### This is the process for filtering multiple screens ###
def main():
    """This will handle the main events of the game"""
    # define instance of player for player 1 
    # define instance of player for player 2
    current_bg_index = 1
    run = True
    while run:
        # draw main menu background
        draw_window(BG_DICT[str(current_bg_index)], current_bg_index)
        # default quit function in loop
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_9] or event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_g] or event.type == pygame.KEYDOWN:
                current_bg_index = 2
                if keys[pygame.K_RETURN]:
                    current_bg_index = 3
                if keys[pygame.K_g]:
                    current_bg_index = 2
                if keys[pygame.K_y]:
                    current_bg_index = 1
main()
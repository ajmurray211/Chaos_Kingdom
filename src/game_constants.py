import pygame, os

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# import font 
main_font = pygame.font.Font('assets/IMMORTAL.ttf', 30)
city_font = pygame.font.Font('assets/IMMORTAL.ttf', 20)
ammo_count_font = pygame.font.Font('assets/IMMORTAL.ttf', 60)
winner_font = pygame.font.Font('assets/IMMORTAL.ttf', 100)

# set FPS and Vel for arrows and player movement
FPS = 60

# set W adn H for player size
PLAYER_W, PLAYER_H = 70, 70
ARROW_W, ARROW_H = 40, 10

## Import pictures and set colors ##
NEUTRAL_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_flag.png')), (50, 40))

# player 1 - red
RED_PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_player.png')), (PLAYER_W, PLAYER_H))
UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_flag.png')), (50, 40))
ACTIVE_UNIT1_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_red.png')), (50, 40))

# player 2 - green
GREEN_PLAYER_IMG= pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_player.png')), (PLAYER_W, PLAYER_H))
UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'green_flag.png')), (50, 40))
ACTIVE_UNIT2_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'active_green.png')), (50, 40))

# arrows and barriers
ARROW1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'arrow1.png')), (ARROW_W, ARROW_H))
BOLDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bolder.png')), (90, 70))

# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'title_bg5.png')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg1.jpeg')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG}#, '3':BATTLEMAP_BG

# color
color_dict = {'white':(255,255,255), 'yellow':(255,255,0), 'blue':(0,0,255), 'black':(0,0,0), 'green': (0,255,0), 'red':(255,0,0)}
text_dict = { 
    '1': {
        "title": "Chaos Kingdom",
        "prompt1": "Press the spacebar to start",
        "prompt2": "Press h to view game description",
        "prompt3": "Press a to view about game maker",
        "prompt4": "Press c to view controls",
    },
    '2':{
        'title': 'How to play',
        'prompt': 'This is a turn based conquest game. The goal of the game is to take over every city. You will be prompted to move your active token to a city if that city is neutral (blue) you will automatically get it but if that city is the opposing players color you will automatically be launched into a battlemap. The winner of that match will determine who gets the city. Once you select a direction to move press the spacebar to end your turn.'
    },
    '3':{   
        'title': "Battle map",
        'red':{
            'ammo': 15,
            'structures': 3,
            'health': 100
        },
        'green':{
            'ammo': 15,
            'structures': 3,
            'health': 100
        }
    },
    '4':{
        'title': 'About maker',
        'prompt': 'This game was inspired from starwars battlefront 2 a game that my brother and I used to play growing up. The structure is based off of battlefront but the theme of the game stems from my love of Skyrim and fantasy RPGs. This is the first game that I have ever built and I had a blast, hopefully you enjoy playing!'
    },
    '5':{
        'title': 'Battle map controls',
        'prompt1': '--- Player 1 --- UP-w, DOWN-s, LEFT-a, RIGHT-d, SHOOT-c, BUILD-v. ',
        'prompt2': '--- Player 2 --- UP-arrow up, DOWN - arrow down, LEFT - left arrow, RIGHT - right arrow, SHOOT - n, BUILD - m'
    }
}
city_dict = {
    "Utrila": {        
        'x_cord': 836,
        'y_cord': 220,
        'city_num': 1,
        'bg': 'lava_bg',
        'linked_cities': ['Yido', 'Ipria']
        },
    "Gishire": {
        'x_cord': 95,
        'y_cord': 300,
        'city_num': 2,
        'bg': 'mountain_bg1',
        'linked_cities': ['Tetgas', 'Sheaford']
        },
    "Tetgas": {        
        'x_cord': 320,
        'y_cord': 212,
        'city_num': 3,
        'bg': 'mountain_bg1',
        'linked_cities': ['Gishire', 'Oreledo', 'Plecdiff']
        },
    "Oreledo": {
        'x_cord': 395,
        'y_cord': 300,
        'city_num': 4,
        'bg': 'mountain_bg1',
        'linked_cities': ['Tetgas', 'Inphis', 'Strinta']
        },
    "Plecdiff": {
        'x_cord': 460,
        'y_cord': 185,
        'city_num': 5,
        'bg': 'mountain_bg1',
        'linked_cities': ['Tetgas', 'Strinta']
        },
    "Strinta": {
        'x_cord': 518,
        'y_cord': 242,
        'city_num': 6,
        'bg': 'mountain_bg1',
        'linked_cities': ['Plecdiff', 'Ipria', 'Yido', 'Oreledo']    
        },
    "Yido": {
        'x_cord': 830,
        'y_cord': 100,
        'city_num': 7,
        'bg': 'winter_bg',
        'linked_cities': ['Strinta', 'Utrila']    
        },
    "Ipria": {
        'x_cord': 627,
        'y_cord': 343,
        'city_num': 8,
        'bg': 'desert_bg1',
        'linked_cities': ['Utrila', 'Strinta', 'Zhento']    
        },
    "Zhento": {
        'x_cord': 765,
        'y_cord': 450,
        'city_num': 9,
        'bg': 'desert_bg1',
        'linked_cities': ['Ipria', 'Uleron']
        },
    "Uleron": {
        'x_cord': 374,
        'y_cord': 478,
        'city_num': 10,
        'bg': 'winter_bg',
        'linked_cities': ['Inphis', 'Zhento']
    },
    "Inphis": {
        'x_cord': 334,
        'y_cord': 347,
        'city_num': 11,
        'bg': 'mountain_bg1',
        'linked_cities': ['Oreledo', 'Uleron', 'Glavine']
    },
    "Glavine": {
        'x_cord': 295,
        'y_cord': 317,
        'city_num': 12,
        'bg': 'mountain_bg1',
        'linked_cities': ['Inphis','Sheaford']
    },
    "Sheaford": {
        'x_cord': 205,
        'y_cord': 400,
        'city_num': 13,
        'bg': 'mountain_bg1',
        'linked_cities': ['Gishire','Glavine']
    }
}
 
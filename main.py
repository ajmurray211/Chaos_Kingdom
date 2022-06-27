
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# set border 
# import font
main_font = pygame.font.SysFont('comicsans', 50)

# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size
PLAYER_W, PLAYER_H = 50, 50
BULLET_W, BULLET_H = 10, 10

## Import pictures and set colors ##
# player 1
BLUE_1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player.png')), (PLAYER_W, PLAYER_H))
# player 2
YELLOW_2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yellow_player.png')), (PLAYER_W, PLAYER_H))
# Bullet
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bullet.png')), (PLAYER_W, PLAYER_H))
# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu_bg.jpeg')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
BG_DICT = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG, '3':BATTLEMAP_BG}

# color
color_dict = {'white':(255,255,255), 'yellow':(0,255,255), 'blue':(0,255,0), 'black':(0,0,0)}

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
test = 'test text'
# def to draw main_menu
def draw_main_menu(test):
    main_text = main_font.render(test, 1, (255,255,255))
    WIN.blit(main_text, (10,10))

# def to draw the window
def draw_window(background, curr_index):
    """This method updates the window"""
    WIN.blit(background, (0,0))
    # filter what to run 
    if curr_index == 1:
        draw_main_menu(test)
    # if curr_index == 2:
    # if curr_index == 3:

    pygame.display.update()

## This is the process for filtering multiple screens ###
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
                
    # def for main menu
    #     filter clicks to launch different screens
    #         closing the app
    #         directions
    #         controls
    #         running the gameboard

    # def for gameboard
    #     filter clicks to launch different screens
    #         closing to the main menu 
    #         opening the battle map

    # def for battlemap
    #     filter for the end of game or quit that returns to game board 
    #         game ends or close launches gameboard
      
# call main menu to run the app 
main()
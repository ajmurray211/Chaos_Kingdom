
import pygame, os, random, time
pygame.font.init()

# set a window
WIDTH , HEIGHT  = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chaos Kingdom!")

# set border 
# set FPS and Vel for bullets and player movement
FPS = 60
# set W adn H for player size

# Import pictures and set colors
# player 1
# player 2
# Bullet
# Background 
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'main_menu_bg.jpeg')), (WIDTH,HEIGHT))
GAME_BOARD_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'game_board_bg.jpeg')), (WIDTH,HEIGHT))
BATTLEMAP_BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'battlemap_bg.png')), (WIDTH,HEIGHT))
BG_KEYS = { '1': MAIN_MENU_BG, '2':GAME_BOARD_BG, '3':BATTLEMAP_BG}

# color dict

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

# def to draw the window
def draw_window(background):
    """This method updates the window"""
    WIN.blit(background, (0,0))
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
        draw_window(BG_KEYS[str(current_bg_index)])
        # default quit function in loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                current_bg_index = 2
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    current_bg_index = 3
                if keys[pygame.K_ESCAPE]:
                    current_bg_index = 2         
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